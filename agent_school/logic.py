"""Bounded, exhaustive checks for classical propositional arguments.

The input is a JSON abstract syntax tree, never executable source code. A result
concerns only the supplied formalisation. It does not verify that its premises
are true, that the formalisation is faithful, or that an action is authorised.

Accepted formulae::

    {"var": "P"}
    {"const": True}
    {"op": "not", "args": [{"var": "P"}]}
    {"op": "implies", "args": [{"var": "P"}, {"var": "Q"}]}

Binary operators are ``and``, ``or`` (inclusive), ``implies`` (material), and
``iff``. Bounds deliberately keep a complete truth table small enough to audit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
import re


MAX_VARIABLES = 8
MAX_DEPTH = 32
MAX_NODES = 512
_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_]{0,63}\Z", re.ASCII)
_BINARY = frozenset({"and", "or", "implies", "iff"})


class FormulaError(ValueError):
    """The requested check is malformed or exceeds the supported fragment."""


@dataclass
class _Budget:
    nodes: int = 0
    variables: set[str] = field(default_factory=set)


def _compile(node: dict, budget: _Budget, depth: int = 1) -> tuple:
    """Validate and copy an AST into a small immutable internal expression."""
    budget.nodes += 1
    if budget.nodes > MAX_NODES:
        raise FormulaError(f"An argument may contain at most {MAX_NODES} AST nodes")
    if depth > MAX_DEPTH:
        raise FormulaError(f"Formula nesting may not exceed {MAX_DEPTH} nodes")
    if type(node) is not dict:
        raise FormulaError("Each formula must be a JSON object")

    if node.keys() == {"var"}:
        name = node["var"]
        if type(name) is not str or _NAME.fullmatch(name) is None:
            raise FormulaError("Variable names must be ASCII identifiers of 1-64 characters")
        budget.variables.add(name)
        if len(budget.variables) > MAX_VARIABLES:
            raise FormulaError(f"An argument may use at most {MAX_VARIABLES} variables")
        return ("var", name)

    if node.keys() == {"const"}:
        value = node["const"]
        if type(value) is not bool:
            raise FormulaError("Constants must be JSON booleans, not numbers or strings")
        return ("const", value)

    if node.keys() != {"op", "args"}:
        raise FormulaError("Use exactly var, const, or op/args keys")
    operator, args = node["op"], node["args"]
    if type(operator) is not str or operator not in _BINARY | {"not"}:
        raise FormulaError("Unsupported operator")
    if type(args) is not list:
        raise FormulaError("Operator args must be a JSON array")
    arity = 1 if operator == "not" else 2
    if len(args) != arity:
        raise FormulaError(f"Operator {operator} requires exactly {arity} argument(s)")
    return (operator, *(_compile(arg, budget, depth + 1) for arg in args))


def _evaluate(expression: tuple, assignment: dict[str, bool]) -> bool:
    operator = expression[0]
    if operator == "var":
        return assignment[expression[1]]
    if operator == "const":
        return expression[1]
    left = _evaluate(expression[1], assignment)
    if operator == "not":
        return not left
    right = _evaluate(expression[2], assignment)
    if operator == "and":
        return left and right
    if operator == "or":
        return left or right
    if operator == "implies":
        return (not left) or right
    # Only a validated binary iff reaches this branch.
    return left == right


def evaluate_formula(formula: dict, assignment: dict[str, bool]) -> bool:
    """Evaluate one accepted formula with an exact, Boolean assignment.

    Missing variables, unused variables, and integer stand-ins for booleans are
    rejected, so a typographical error cannot silently change the interpretation.
    """
    budget = _Budget()
    expression = _compile(formula, budget)
    if type(assignment) is not dict or assignment.keys() != budget.variables:
        raise FormulaError("Assignment keys must match the formula variables exactly")
    if any(type(value) is not bool for value in assignment.values()):
        raise FormulaError("Assignment values must be JSON booleans")
    return _evaluate(expression, assignment)


def analyse_argument(premises: list[dict], conclusion: dict) -> dict:
    """Return exhaustive entailment and consistency results for a bounded AST.

    ``valid`` is true exactly when no assignment makes every premise true and
    the conclusion false. Inconsistent premises therefore yield ``valid=True``
    and ``premises_consistent=False``. Consumers must report both fields. Such
    vacuous entailment is not evidence that the conclusion is true in the world.

    Empty premises are allowed: a tautological conclusion is valid, while a
    contingent conclusion is not. The empty premise set is consistent.
    """
    if type(premises) is not list:
        raise FormulaError("Premises must be a JSON array of formula objects")
    if len(premises) >= MAX_NODES:
        raise FormulaError("Too many premises for the argument node budget")
    budget = _Budget()
    compiled_premises = [_compile(premise, budget) for premise in premises]
    compiled_conclusion = _compile(conclusion, budget)
    variables = sorted(budget.variables)
    checked = 0
    satisfying = 0
    counterexample = None
    premise_witness = None
    for values in product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, values))
        checked += 1
        if all(_evaluate(premise, assignment) for premise in compiled_premises):
            satisfying += 1
            if premise_witness is None:
                premise_witness = assignment.copy()
            if not _evaluate(compiled_conclusion, assignment) and counterexample is None:
                counterexample = assignment.copy()
    return {
        "valid": counterexample is None,
        "premises_consistent": satisfying > 0,
        "variables": variables,
        "assignments_checked": checked,
        "satisfying_premise_assignments": satisfying,
        "premise_witness": premise_witness,
        "counterexample": counterexample,
        "claim_scope": "classical_propositional_entailment_only",
    }
