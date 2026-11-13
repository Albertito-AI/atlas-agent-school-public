"""Evaluate closed first-order formulae in one explicit finite structure.

This is a bounded model evaluator, not a decision procedure for general
first-order validity. Predicate extensions are declared complete: a tuple not
in an extension is false *in the supplied structure*. Missing real-world
evidence does not thereby become false.

Structure example::

    {"domain": ["a", "b"], "constants": {"c": "a"},
     "predicates": {"R": {"arity": 2, "extension": [["a", "b"]]}}}

Terms are ``{"var": "x"}`` and ``{"const": "c"}``. Formulae are predicate
applications ``{"pred": "R", "args": [term, term]}``, equality
``{"eq": [term, term]}``, Boolean literals ``{"const": True}``, connectives
``{"op": "and", "args": [formula, formula]}``, and quantifiers
``{"op": "forall", "var": "x", "body": formula}``. Quantifiers also include
``exists``; other connectives are ``not``, inclusive ``or``, material ``implies``
and ``iff``. Functions and free variables are outside the accepted fragment.

All syntax, symbol use, scope and evaluation cost are checked before evaluation.
Every branch and every quantified assignment is then evaluated. Resource limits
therefore apply independently of truth-functional or quantifier short-circuiting.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


MAX_DOMAIN_SIZE = 8
MAX_SYMBOLS = 64  # Per declared symbol category.
MAX_ARITY = 4
MAX_EXTENSION_TUPLES = 4096  # Across the complete supplied structure.
MAX_AST_NODES = 512  # Formula nodes and term occurrences together.
MAX_AST_DEPTH = 32
MAX_EVALUATION_STEPS = 100_000
_IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9_]{0,63}\Z", re.ASCII)
_DOMAIN_LABEL = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.:-]{0,63}\Z", re.ASCII)
_BINARY = frozenset({"and", "or", "implies", "iff"})
_QUANTIFIERS = frozenset({"forall", "exists"})


class FiniteLogicError(ValueError):
    """The model or formula is malformed or exceeds an explicit resource limit."""


@dataclass(frozen=True)
class _Predicate:
    arity: int
    extension: frozenset[tuple[str, ...]]


@dataclass(frozen=True)
class _Structure:
    domain: tuple[str, ...]
    constants: dict[str, str]
    predicates: dict[str, _Predicate]


def _identifier(value, label: str) -> str:
    if type(value) is not str or _IDENTIFIER.fullmatch(value) is None:
        raise FiniteLogicError(f"{label} must be an ASCII identifier of 1-64 characters")
    return value


def _structure(value: dict) -> _Structure:
    if type(value) is not dict or value.keys() != {"domain", "constants", "predicates"}:
        raise FiniteLogicError("A structure requires exactly domain, constants and predicates")
    domain = value["domain"]
    if type(domain) is not list or not 1 <= len(domain) <= MAX_DOMAIN_SIZE:
        raise FiniteLogicError(f"The domain must contain 1-{MAX_DOMAIN_SIZE} distinct labels")
    if any(type(item) is not str or _DOMAIN_LABEL.fullmatch(item) is None for item in domain):
        raise FiniteLogicError("Domain labels must be bounded ASCII names")
    members = frozenset(domain)
    if len(members) != len(domain):
        raise FiniteLogicError("Domain labels must be distinct")

    constants = value["constants"]
    if type(constants) is not dict or len(constants) > MAX_SYMBOLS:
        raise FiniteLogicError(f"Declare at most {MAX_SYMBOLS} constants in a JSON object")
    for name, denotation in constants.items():
        _identifier(name, "Constant name")
        if type(denotation) is not str or denotation not in members:
            raise FiniteLogicError("Every constant must denote a domain member")

    predicates = value["predicates"]
    if type(predicates) is not dict or len(predicates) > MAX_SYMBOLS:
        raise FiniteLogicError(f"Declare at most {MAX_SYMBOLS} predicates in a JSON object")
    compiled_predicates = {}
    total_rows = 0
    for name, declaration in predicates.items():
        _identifier(name, "Predicate name")
        if type(declaration) is not dict or declaration.keys() != {"arity", "extension"}:
            raise FiniteLogicError("A predicate declaration requires exactly arity and extension")
        arity, extension = declaration["arity"], declaration["extension"]
        if type(arity) is not int or not 0 <= arity <= MAX_ARITY:
            raise FiniteLogicError(f"Predicate arity must be an integer from 0 to {MAX_ARITY}")
        if type(extension) is not list:
            raise FiniteLogicError("A predicate extension must be a JSON array of rows")
        total_rows += len(extension)
        if total_rows > MAX_EXTENSION_TUPLES:
            raise FiniteLogicError("The structure exceeds its predicate-extension row budget")
        rows = set()
        for row in extension:
            if type(row) is not list or len(row) != arity:
                raise FiniteLogicError("Each extension row must match the declared predicate arity")
            if any(type(item) is not str or item not in members for item in row):
                raise FiniteLogicError("Predicate rows may contain only domain members")
            converted = tuple(row)
            if converted in rows:
                raise FiniteLogicError("Duplicate predicate-extension rows are not accepted")
            rows.add(converted)
        compiled_predicates[name] = _Predicate(arity, frozenset(rows))
    return _Structure(tuple(domain), constants.copy(), compiled_predicates)


@dataclass
class _Compiler:
    structure: _Structure
    max_steps: int
    nodes: int = 0

    def node(self, value, depth: int) -> None:
        self.nodes += 1
        if self.nodes > MAX_AST_NODES:
            raise FiniteLogicError("Formula and term occurrences exceed the AST node budget")
        if depth > MAX_AST_DEPTH:
            raise FiniteLogicError("The formula exceeds its AST nesting limit")
        if type(value) is not dict:
            raise FiniteLogicError("Every formula and term must be a JSON object")

    def cost(self, value: int) -> int:
        if value > self.max_steps:
            raise FiniteLogicError(
                f"Exhaustive evaluation requires more than the {self.max_steps}-step budget"
            )
        return value

    def term(self, value: dict, bound: tuple[str, ...], depth: int) -> tuple:
        self.node(value, depth)
        if value.keys() == {"var"}:
            name = _identifier(value["var"], "Variable name")
            if name not in bound:
                raise FiniteLogicError(f"Free variable is not permitted: {name}")
            # An index from the innermost binder preserves lexical shadowing.
            return ("var", bound[::-1].index(name))
        if value.keys() == {"const"}:
            name = _identifier(value["const"], "Constant name")
            if name not in self.structure.constants:
                raise FiniteLogicError(f"Undeclared constant: {name}")
            return ("const", self.structure.constants[name])
        raise FiniteLogicError("A term requires exactly one var or const key")

    def formula(self, value: dict, bound: tuple[str, ...] = (), depth: int = 1) -> tuple:
        self.node(value, depth)
        keys = value.keys()
        if keys == {"const"}:
            if type(value["const"]) is not bool:
                raise FiniteLogicError("A formula constant must be a JSON boolean")
            return ("bool", value["const"]), self.cost(1)
        if keys == {"pred", "args"}:
            name = _identifier(value["pred"], "Predicate name")
            if name not in self.structure.predicates:
                raise FiniteLogicError(f"Undeclared predicate: {name}")
            args = value["args"]
            if type(args) is not list or len(args) != self.structure.predicates[name].arity:
                raise FiniteLogicError("Predicate application does not match its declared arity")
            terms = tuple(self.term(arg, bound, depth + 1) for arg in args)
            return ("pred", name, terms), self.cost(1 + len(terms))
        if keys == {"eq"}:
            args = value["eq"]
            if type(args) is not list or len(args) != 2:
                raise FiniteLogicError("Equality requires exactly two terms")
            terms = tuple(self.term(arg, bound, depth + 1) for arg in args)
            return ("eq", *terms), self.cost(3)
        if keys == {"op", "var", "body"}:
            operator = value["op"]
            if type(operator) is not str or operator not in _QUANTIFIERS:
                raise FiniteLogicError("A quantified formula requires forall or exists")
            name = _identifier(value["var"], "Bound variable")
            body, body_cost = self.formula(value["body"], bound + (name,), depth + 1)
            cost = self.cost(1 + len(self.structure.domain) * body_cost)
            return (operator, name, body), cost
        if keys == {"op", "args"}:
            operator, args = value["op"], value["args"]
            if type(operator) is not str or operator not in _BINARY | {"not"}:
                raise FiniteLogicError("Unsupported connective")
            arity = 1 if operator == "not" else 2
            if type(args) is not list or len(args) != arity:
                raise FiniteLogicError("Connective argument count does not match its arity")
            # Compile every child before evaluating any branch.
            children = [self.formula(arg, bound, depth + 1) for arg in args]
            cost = self.cost(1 + sum(child_cost for _, child_cost in children))
            return (operator, *(child for child, _ in children)), cost
        raise FiniteLogicError("Unrecognised formula shape or extra AST keys")


@dataclass
class _Evaluator:
    structure: _Structure
    max_steps: int
    steps: int = 0

    def step(self) -> None:
        self.steps += 1
        if self.steps > self.max_steps:
            raise FiniteLogicError("Evaluation exceeded its step budget")

    def term(self, expression: tuple, environment: tuple[str, ...]) -> str:
        self.step()
        if expression[0] == "const":
            return expression[1]
        return environment[-1 - expression[1]]

    def formula(self, expression: tuple, environment: tuple[str, ...] = (), root_cases=None) -> bool:
        self.step()
        operator = expression[0]
        if operator == "bool":
            return expression[1]
        if operator == "pred":
            row = tuple(self.term(term, environment) for term in expression[2])
            return row in self.structure.predicates[expression[1]].extension
        if operator == "eq":
            return self.term(expression[1], environment) == self.term(expression[2], environment)
        if operator in _QUANTIFIERS:
            values = []
            for member in self.structure.domain:
                result = self.formula(expression[2], environment + (member,))
                values.append(result)
                if root_cases is not None:
                    root_cases.append({"binding": {expression[1]: member}, "body_value": result})
            # Both functions inspect a fully evaluated list, not a lazy iterator.
            return all(values) if operator == "forall" else any(values)
        left = self.formula(expression[1], environment)
        if operator == "not":
            return not left
        right = self.formula(expression[2], environment)
        if operator == "and":
            return left and right
        if operator == "or":
            return left or right
        if operator == "implies":
            return (not left) or right
        return left == right  # Only a validated iff remains.


def evaluate_in_structure(formula: dict, structure: dict, *, max_steps: int = MAX_EVALUATION_STEPS) -> dict:
    """Return truth in one supplied finite structure, with bounded evidence.

    ``required_steps`` counts expanded formula and term evaluations. The cost is
    computed before evaluation, including all branches and all quantifier cases.
    ``max_steps`` may lower, but never exceed, the hard 100,000-step ceiling.

    Root quantifiers expose each domain binding and its body's truth value. A
    true existential supplies one witness; a false universal supplies one
    counterexample. These are witnesses in this structure, not validity proofs.
    """
    if type(max_steps) is not int or not 1 <= max_steps <= MAX_EVALUATION_STEPS:
        raise FiniteLogicError(f"max_steps must be an integer from 1 to {MAX_EVALUATION_STEPS}")
    checked_structure = _structure(structure)
    compiler = _Compiler(checked_structure, max_steps)
    expression, required_steps = compiler.formula(formula)
    evaluator = _Evaluator(checked_structure, max_steps)
    cases = []
    value = evaluator.formula(expression, root_cases=cases)
    evidence = None
    if expression[0] == "exists" and value:
        case = next(case for case in cases if case["body_value"])
        evidence = {"kind": "existential_witness", "binding": case["binding"]}
    elif expression[0] == "forall" and not value:
        case = next(case for case in cases if not case["body_value"])
        evidence = {"kind": "universal_counterexample", "binding": case["binding"]}
    return {
        "value": value,
        "claim_scope": "truth_in_one_supplied_finite_structure",
        "domain_size": len(checked_structure.domain),
        "ast_nodes": compiler.nodes,
        "required_steps": required_steps,
        "steps_used": evaluator.steps,
        "root_quantifier_cases": cases,
        "evidence": evidence,
    }
