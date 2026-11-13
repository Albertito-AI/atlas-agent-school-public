"""Substantive semantic and input-boundary checks for the F01 logic tool."""

import unittest

from agent_school.logic import (
    FormulaError,
    MAX_DEPTH,
    MAX_NODES,
    analyse_argument,
    evaluate_formula,
)


def var(name):
    return {"var": name}


def op(name, *args):
    return {"op": name, "args": list(args)}


P, Q, R = var("P"), var("Q"), var("R")


class LogicTests(unittest.TestCase):
    def test_characteristic_truth_tables(self):
        rows = [(False, False), (False, True), (True, False), (True, True)]
        expected = {
            "and": [False, False, False, True],
            "or": [False, True, True, True],
            "implies": [True, True, False, True],
            "iff": [True, False, False, True],
        }
        for name, answers in expected.items():
            with self.subTest(operator=name):
                self.assertEqual(
                    [evaluate_formula(op(name, P, Q), {"P": p, "Q": q}) for p, q in rows],
                    answers,
                )

    def test_modus_ponens_has_consistent_premises(self):
        result = analyse_argument([op("implies", P, Q), P], Q)
        self.assertTrue(result["valid"])
        self.assertTrue(result["premises_consistent"])
        self.assertEqual(result["satisfying_premise_assignments"], 1)
        self.assertEqual(result["assignments_checked"], 4)

    def test_modus_tollens(self):
        result = analyse_argument([op("implies", P, Q), op("not", Q)], op("not", P))
        self.assertTrue(result["valid"])
        self.assertTrue(result["premises_consistent"])

    def test_affirming_consequent_has_inspectable_counterexample(self):
        premises = [op("implies", P, Q), Q]
        result = analyse_argument(premises, P)
        self.assertFalse(result["valid"])
        self.assertEqual(result["counterexample"], {"P": False, "Q": True})
        witness = result["counterexample"]
        self.assertTrue(evaluate_formula(premises[0], witness))
        self.assertTrue(evaluate_formula(Q, {"Q": witness["Q"]}))
        self.assertFalse(evaluate_formula(P, {"P": witness["P"]}))

    def test_denying_antecedent_is_invalid(self):
        result = analyse_argument([op("implies", P, Q), op("not", P)], op("not", Q))
        self.assertFalse(result["valid"])
        self.assertEqual(result["counterexample"], {"P": False, "Q": True})

    def test_inconsistent_premises_are_explicitly_flagged(self):
        result = analyse_argument([P, op("not", P)], Q)
        self.assertTrue(result["valid"])
        self.assertFalse(result["premises_consistent"])
        self.assertEqual(result["satisfying_premise_assignments"], 0)
        self.assertIsNone(result["premise_witness"])
        self.assertIsNone(result["counterexample"])

    def test_empty_premises_do_not_establish_contingent_claim(self):
        result = analyse_argument([], P)
        self.assertFalse(result["valid"])
        self.assertTrue(result["premises_consistent"])
        self.assertEqual(result["counterexample"], {"P": False})

    def test_empty_premises_establish_tautology(self):
        result = analyse_argument([], op("or", P, op("not", P)))
        self.assertTrue(result["valid"])
        self.assertTrue(result["premises_consistent"])
        self.assertEqual(result["satisfying_premise_assignments"], 2)

    def test_constant_only_argument_has_one_assignment(self):
        result = analyse_argument([], {"const": True})
        self.assertTrue(result["valid"])
        self.assertTrue(result["premises_consistent"])
        self.assertEqual(result["variables"], [])
        self.assertEqual(result["assignments_checked"], 1)
        self.assertEqual(result["premise_witness"], {})
        false_result = analyse_argument([], {"const": False})
        self.assertFalse(false_result["valid"])
        self.assertEqual(false_result["counterexample"], {})

    def test_de_morgan_equivalence(self):
        left = op("not", op("and", P, Q))
        right = op("or", op("not", P), op("not", Q))
        self.assertTrue(analyse_argument([], op("iff", left, right))["valid"])

    def test_implication_is_not_associative(self):
        left = op("implies", P, op("implies", Q, R))
        right = op("implies", op("implies", P, Q), R)
        result = analyse_argument([], op("iff", left, right))
        self.assertFalse(result["valid"])
        self.assertEqual(result["assignments_checked"], 8)

    def test_material_conditional_is_true_for_false_antecedent(self):
        self.assertTrue(evaluate_formula(op("implies", P, Q), {"P": False, "Q": False}))
        self.assertTrue(evaluate_formula(op("implies", P, Q), {"P": False, "Q": True}))

    def test_all_eight_variables_are_checked_exhaustively(self):
        premises = [op("or", var(f"P{i}"), op("not", var(f"P{i}"))) for i in range(8)]
        result = analyse_argument(premises, {"const": True})
        self.assertEqual(result["assignments_checked"], 256)
        self.assertEqual(result["satisfying_premise_assignments"], 256)
        with self.assertRaises(FormulaError):
            analyse_argument(premises, var("P8"))

    def test_malformed_and_executable_strings_are_rejected(self):
        bad = [
            "__import__('os').system('false')",
            True,
            [],
            {},
            {"var": "P", "const": True},
            {"var": "P; run()"},
            {"var": "P\n"},
            {"var": "P" * 65},
            {"var": "Π"},
            {"const": 1},
            {"const": "true"},
            {"op": "call", "args": [P]},
            {"op": "and", "args": [P]},
            {"op": "not", "args": [P, Q]},
            {"op": "or", "args": (P, Q)},
            {"op": "not", "args": [P], "extra": True},
        ]
        for formula in bad:
            with self.subTest(formula=formula), self.assertRaises(FormulaError):
                analyse_argument([], formula)

    def test_assignment_requires_exact_boolean_values_and_keys(self):
        for assignment in [{}, {"P": 1}, {"P": "true"}, {"P": True, "Q": False}, [True]]:
            with self.subTest(assignment=assignment), self.assertRaises(FormulaError):
                evaluate_formula(P, assignment)

    def test_depth_and_node_bounds(self):
        formula = P
        for _ in range(MAX_DEPTH - 1):
            formula = op("not", formula)
        analyse_argument([], formula)
        with self.assertRaises(FormulaError):
            analyse_argument([], op("not", formula))
        analyse_argument([{"const": True} for _ in range(MAX_NODES - 1)], {"const": True})
        with self.assertRaises(FormulaError):
            analyse_argument([{"const": True} for _ in range(MAX_NODES)], {"const": True})
        # Shared subtrees still cost one node per occurrence when evaluated.
        large = P
        for _ in range(9):
            large = op("and", large, large)
        with self.assertRaises(FormulaError):
            analyse_argument([], large)

    def test_cyclic_python_object_is_rejected_with_bounded_depth(self):
        circular = {"op": "not", "args": []}
        circular["args"].append(circular)
        with self.assertRaises(FormulaError):
            analyse_argument([], circular)

    def test_premises_require_json_array(self):
        with self.assertRaises(FormulaError):
            analyse_argument((P,), P)


if __name__ == "__main__":
    unittest.main()
