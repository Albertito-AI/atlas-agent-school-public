"""Semantic and resource-boundary checks for one finite first-order structure."""

from copy import deepcopy
from itertools import product
import unittest

from agent_school.finite_logic import (
    FiniteLogicError,
    MAX_AST_DEPTH,
    MAX_DOMAIN_SIZE,
    MAX_EVALUATION_STEPS,
    evaluate_in_structure,
)


def var(name):
    return {"var": name}


def const(name):
    return {"const": name}


def pred(name, *args):
    return {"pred": name, "args": list(args)}


def op(name, *args):
    return {"op": name, "args": list(args)}


def quant(name, variable, body):
    return {"op": name, "var": variable, "body": body}


def eq(left, right):
    return {"eq": [left, right]}


def model(domain=None):
    return {"domain": ["a", "b"] if domain is None else domain, "constants": {}, "predicates": {}}


class FiniteLogicTests(unittest.TestCase):
    def test_quantifier_order_has_finite_countermodel(self):
        structure = model()
        structure["predicates"]["R"] = {"arity": 2, "extension": [["a", "a"], ["b", "b"]]}
        relation = pred("R", var("x"), var("y"))
        each_has_some = quant("forall", "x", quant("exists", "y", relation))
        one_for_all = quant("exists", "y", quant("forall", "x", relation))
        first = evaluate_in_structure(each_has_some, structure)
        second = evaluate_in_structure(one_for_all, structure)
        self.assertTrue(first["value"])
        self.assertFalse(second["value"])
        self.assertEqual(first["required_steps"], first["steps_used"])
        self.assertEqual(first["required_steps"], 15)
        self.assertEqual(len(first["root_quantifier_cases"]), 2)

    def test_empty_predicate_in_nonempty_domain_has_no_existential_import(self):
        structure = model()
        structure["predicates"] = {
            "Admitted": {"arity": 1, "extension": []},
            "Passed": {"arity": 1, "extension": []},
        }
        universal = quant("forall", "x", op("implies", pred("Admitted", var("x")), pred("Passed", var("x"))))
        existential = quant("exists", "x", pred("Admitted", var("x")))
        self.assertTrue(evaluate_in_structure(universal, structure)["value"])
        self.assertFalse(evaluate_in_structure(existential, structure)["value"])
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure(universal, model([]))

    def test_relations_are_ordered_and_constants_may_corefer(self):
        structure = model()
        structure["constants"] = {"first": "a", "alias": "a", "second": "b"}
        structure["predicates"]["Before"] = {"arity": 2, "extension": [["a", "b"]]}
        self.assertTrue(evaluate_in_structure(pred("Before", const("first"), const("second")), structure)["value"])
        self.assertFalse(evaluate_in_structure(pred("Before", const("second"), const("first")), structure)["value"])
        self.assertTrue(evaluate_in_structure(eq(const("first"), const("alias")), structure)["value"])
        self.assertFalse(evaluate_in_structure(eq(const("first"), const("second")), structure)["value"])

    def test_inner_binder_shadows_and_does_not_leak(self):
        structure = model()
        structure["predicates"]["P"] = {"arity": 1, "extension": [["a"]]}
        # forall x: (exists x: P(x)) iff P(x) is false at outer x=b.
        formula = quant("forall", "x", op("iff", quant("exists", "x", pred("P", var("x"))), pred("P", var("x"))))
        result = evaluate_in_structure(formula, structure)
        self.assertFalse(result["value"])
        self.assertEqual(result["evidence"], {"kind": "universal_counterexample", "binding": {"x": "b"}})

    def test_outer_variable_remains_accessible_under_distinct_inner_binder(self):
        formula = quant("forall", "x", quant("exists", "y", eq(var("x"), var("y"))))
        self.assertTrue(evaluate_in_structure(formula, model())["value"])

    def test_quantifier_negation_duality(self):
        structure = model()
        structure["predicates"]["P"] = {"arity": 1, "extension": [["a"]]}
        left = op("not", quant("forall", "x", pred("P", var("x"))))
        right = quant("exists", "x", op("not", pred("P", var("x"))))
        self.assertTrue(evaluate_in_structure(op("iff", left, right), structure)["value"])

    def test_existential_witness_and_all_root_cases_are_returned(self):
        structure = model()
        structure["predicates"]["P"] = {"arity": 1, "extension": [["a"]]}
        result = evaluate_in_structure(quant("exists", "x", pred("P", var("x"))), structure)
        self.assertTrue(result["value"])
        self.assertEqual(result["evidence"], {"kind": "existential_witness", "binding": {"x": "a"}})
        self.assertEqual(result["root_quantifier_cases"], [
            {"binding": {"x": "a"}, "body_value": True},
            {"binding": {"x": "b"}, "body_value": False},
        ])
        self.assertEqual(result["steps_used"], 5)
        self.assertEqual(result["claim_scope"], "truth_in_one_supplied_finite_structure")
        self.assertNotIn("valid", result)

    def test_zero_arity_predicates(self):
        structure = model()
        structure["predicates"] = {
            "Ready": {"arity": 0, "extension": [[]]},
            "Done": {"arity": 0, "extension": []},
        }
        self.assertTrue(evaluate_in_structure(pred("Ready"), structure)["value"])
        self.assertFalse(evaluate_in_structure(pred("Done"), structure)["value"])

    def test_boolean_connective_truth_tables(self):
        expected = {
            "and": [False, False, False, True],
            "or": [False, True, True, True],
            "implies": [True, True, False, True],
            "iff": [True, False, False, True],
        }
        for operator, answers in expected.items():
            observed = [evaluate_in_structure(op(operator, {"const": p}, {"const": q}), model())["value"]
                        for p, q in product((False, True), repeat=2)]
            with self.subTest(operator=operator):
                self.assertEqual(observed, answers)

    def test_undeclared_or_free_symbols_are_rejected_even_in_unused_branch(self):
        structure = model()
        structure["predicates"]["P"] = {"arity": 1, "extension": []}
        invalid = [pred("Missing"), pred("P", const("missing")), pred("P", var("x"))]
        for formula in invalid:
            with self.subTest(formula=formula), self.assertRaises(FiniteLogicError):
                evaluate_in_structure(op("or", {"const": True}, formula), structure)
        leaked = op("and", quant("exists", "x", pred("P", var("x"))), pred("P", var("x")))
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure(leaked, structure)

    def test_malformed_asts_are_rejected(self):
        structure = model()
        structure["predicates"]["P"] = {"arity": 1, "extension": []}
        bad = [
            "__import__('os').system('false')", True, [], {}, {"const": 1},
            {"pred": "P", "args": []}, {"pred": "P", "args": [True]},
            {"eq": []}, {"eq": [{"const": True}, {"const": True}]},
            {"op": "forall", "var": "x", "body": {"const": True}, "extra": True},
            {"op": "forall", "var": "x\n", "body": {"const": True}},
            {"op": "forall", "args": [{"const": True}]},
            {"op": "exists", "var": True, "body": {"const": True}},
            {"op": "not", "args": [{"const": True}, {"const": False}]},
            {"op": "and", "args": ({"const": True}, {"const": False})},
        ]
        for formula in bad:
            with self.subTest(formula=formula), self.assertRaises(FiniteLogicError):
                evaluate_in_structure(formula, structure)

    def test_structure_validation(self):
        base = model()
        invalid = [None, [], {}, model([]), model(["a", "a"]), model([True]),
                   model(["a\n"]), model(["a"] * (MAX_DOMAIN_SIZE + 1))]
        for update in [
            {"constants": {"bad": "outside"}},
            {"constants": {"bad\n": "a"}},
            {"predicates": {"P": {"arity": True, "extension": []}}},
            {"predicates": {"P": {"arity": -1, "extension": []}}},
            {"predicates": {"P": {"arity": 5, "extension": []}}},
            {"predicates": {"P": {"arity": 1, "extension": [["outside"]]}}},
            {"predicates": {"P": {"arity": 1, "extension": [["a", "b"]]}}},
            {"predicates": {"P": {"arity": 1, "extension": [["a"], ["a"]]}}},
            {"predicates": {"P": {"arity": 1, "extension": [("a",)]}}},
            {"predicates": {"P": {"arity": 1, "extension": [[[]]]}}},
            {"predicates": {"P": {"arity": 1, "extension": [], "extra": 0}}},
            {"extra": True},
        ]:
            invalid.append({**base, **update})
        for structure in invalid:
            with self.subTest(structure=structure), self.assertRaises(FiniteLogicError):
                evaluate_in_structure({"const": True}, structure)

    def test_budget_is_exact_and_independent_of_short_circuit(self):
        structure = model([str(i) for i in range(8)])
        expensive = {"const": True}
        for i in range(6):
            expensive = quant("forall", f"x{i}", expensive)
        # Both are immediately decidable by short-circuiting, but exceed the
        # declared full-expansion budget and must be rejected before running.
        for formula in [op("or", {"const": True}, expensive), op("and", {"const": False}, expensive)]:
            with self.subTest(formula=formula["op"]), self.assertRaises(FiniteLogicError):
                evaluate_in_structure(formula, structure)
        bounded = quant("forall", "x", {"const": True})
        result = evaluate_in_structure(bounded, structure, max_steps=9)
        self.assertEqual(result["required_steps"], 9)
        self.assertEqual(result["steps_used"], 9)
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure(bounded, structure, max_steps=8)
        for limit in [0, -1, True, 1.5, MAX_EVALUATION_STEPS + 1]:
            with self.subTest(limit=limit), self.assertRaises(FiniteLogicError):
                evaluate_in_structure({"const": True}, structure, max_steps=limit)

    def test_ast_depth_node_and_cycle_limits(self):
        formula = {"const": True}
        for _ in range(MAX_AST_DEPTH - 1):
            formula = op("not", formula)
        evaluate_in_structure(formula, model())
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure(op("not", formula), model())
        repeated = {"const": True}
        for _ in range(9):
            repeated = op("and", repeated, repeated)
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure(repeated, model())
        cyclic = {"op": "not", "args": []}
        cyclic["args"].append(cyclic)
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure(cyclic, model())

    def test_total_extension_budget_and_symbol_caps(self):
        structure = model([str(i) for i in range(8)])
        rows = [list(row) for row in product(structure["domain"], repeat=4)]
        structure["predicates"] = {"R": {"arity": 4, "extension": rows}}
        self.assertTrue(evaluate_in_structure({"const": True}, structure)["value"])
        structure["predicates"]["Extra"] = {"arity": 0, "extension": [[]]}
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure({"const": True}, structure)
        too_many = model()
        too_many["constants"] = {f"c{i}": "a" for i in range(65)}
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure({"const": True}, too_many)
        too_many = model()
        too_many["predicates"] = {f"P{i}": {"arity": 0, "extension": []} for i in range(65)}
        with self.assertRaises(FiniteLogicError):
            evaluate_in_structure({"const": True}, too_many)

    def test_inputs_remain_unchanged(self):
        structure = model()
        structure["predicates"]["P"] = {"arity": 1, "extension": [["a"]]}
        formula = quant("exists", "x", pred("P", var("x")))
        original = deepcopy((formula, structure))
        evaluate_in_structure(formula, structure)
        self.assertEqual((formula, structure), original)


if __name__ == "__main__":
    unittest.main()
