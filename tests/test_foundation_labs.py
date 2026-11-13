"""Derive mathematical results for the public F01 reference laboratories.

These checks validate public reference artifacts. They do not grade a learner's
complete submission, evaluate its operational judgment, or establish learning.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import unittest

from agent_school.finite_logic import evaluate_in_structure
from agent_school.logic import analyse_argument, evaluate_formula


ROOT = Path(__file__).resolve().parents[1]


def variables(formula):
    if "var" in formula:
        return {formula["var"]}
    if "const" in formula:
        return set()
    return set().union(*(variables(child) for child in formula["args"]))


def value_under(formula, assignment):
    """Project a complete assignment onto the formula's exact variable set."""
    return evaluate_formula(formula, {name: assignment[name] for name in variables(formula)})


def powerset(values):
    for size in range(len(values) + 1):
        for selection in combinations(values, size):
            yield frozenset(selection)


def minimal_sets(collection):
    return {candidate for candidate in collection if not any(other < candidate for other in collection)}


def canonical(formula):
    return json.dumps(formula, sort_keys=True, separators=(",", ":"))


def rename(formula, mapping):
    if "var" in formula:
        return {"var": mapping[formula["var"]]}
    if "const" in formula:
        return formula.copy()
    return {"op": formula["op"], "args": [rename(child, mapping) for child in formula["args"]]}


class FoundationLabReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = json.loads((ROOT / "curriculum/foundation-01/labs.json").read_text())
        cls.labs = {lab["id"]: lab for lab in cls.bundle["labs"]}
        if len(cls.labs) != len(cls.bundle["labs"]):
            raise AssertionError("Laboratory identifiers must be unique")

    def test_l01_entailment_counts_and_reverse_countermodel(self):
        lab = self.labs["F01-L01"]
        task, reference = lab["input"], lab["reference"]
        observed = analyse_argument(task["premises"], task["conclusion"])
        for field in ("valid", "premises_consistent", "assignments_checked", "satisfying_premise_assignments"):
            with self.subTest(field=field):
                self.assertEqual(observed[field], reference[field])
        reverse = task["reverse_test"]
        reverse_result = analyse_argument(reverse["premises"], reverse["conclusion"])
        self.assertEqual(reverse_result["valid"], reference["reverse_valid"])
        witness = reference["reverse_countermodel"]
        self.assertEqual(set(witness), set(reverse_result["variables"]))
        self.assertTrue(all(type(value) is bool for value in witness.values()))
        self.assertTrue(all(value_under(premise, witness) for premise in reverse["premises"]))
        self.assertFalse(value_under(reverse["conclusion"], witness))

    def test_l02_all_inclusion_minimal_conflicts_and_repairs(self):
        lab = self.labs["F01-L02"]
        rows, reference = lab["input"]["premises"], lab["reference"]
        formulae = {row["id"]: row["formula"] for row in rows}
        self.assertEqual(len(formulae), len(rows))
        ids = tuple(formulae)
        all_ids = frozenset(ids)
        names = sorted(set().union(*(variables(formula) for formula in formulae.values())))
        # Build the full valuation table once. Consistency is determined from
        # rows, without relying on the text's stated conflict/removal sets.
        valuations = [dict(zip(names, values)) for values in product((False, True), repeat=len(names))]
        true_sets = [frozenset(key for key, formula in formulae.items() if value_under(formula, valuation))
                     for valuation in valuations]

        def consistent(subset):
            return any(subset <= true_set for true_set in true_sets)

        all_subsets = tuple(powerset(ids))
        inconsistent = {subset for subset in all_subsets if not consistent(subset)}
        restoring_removals = {removed for removed in all_subsets if consistent(all_ids - removed)}
        conflicts = minimal_sets(inconsistent)
        repairs = minimal_sets(restoring_removals)
        self.assertEqual(conflicts, {frozenset(group) for group in reference["minimal_inconsistent_subsets"]})
        self.assertEqual(repairs, {frozenset(group) for group in reference["minimal_removal_sets"]})
        # Inclusion-minimal repairs can have different cardinalities. Verify
        # that the exercise really demonstrates this distinction.
        self.assertGreater(len({len(repair) for repair in repairs}), 1)
        # Each minimal repair must hit every minimal conflict.
        self.assertTrue(all(repair & conflict for repair in repairs for conflict in conflicts))

    def test_l02_reference_repair_has_a_consistency_witness(self):
        lab = self.labs["F01-L02"]
        reference = lab["reference"]
        preferred = frozenset(reference["preferred_removal_set"])
        self.assertIn(preferred, {frozenset(group) for group in reference["minimal_removal_sets"]})
        kept = [row["formula"] for row in lab["input"]["premises"] if row["id"] not in preferred]
        observed = analyse_argument(kept, {"const": True})
        self.assertTrue(observed["premises_consistent"])
        witness = reference["repaired_witness"]
        self.assertEqual(set(witness), set(observed["variables"]))
        self.assertTrue(all(type(value) is bool for value in witness.values()))
        self.assertTrue(all(value_under(premise, witness) for premise in kept))
        # Choosing this repair on evidential grounds remains a task stipulation
        # for rubric review; a truth table cannot make that normative choice.

    def test_l03_relational_values_are_derived_from_extensions(self):
        lab = self.labs["F01-L03"]
        structure = lab["input"]["structure"]
        extensions = structure["predicates"]
        reports = {row[0] for row in extensions["Report"]["extension"]}
        reviewers = {row[0] for row in extensions["Reviewer"]["extension"]}
        reviews = {tuple(row) for row in extensions["Reviews"]["extension"]}
        enrolled = {row[0] for row in extensions["Enrolled"]["extension"]}
        passed = {row[0] for row in extensions["Passed"]["extension"]}
        # Direct set/relational calculations are independent of the AST model
        # evaluator. Comparing both also checks the supplied formalisation.
        derived = {
            "each_report_has_reviewer": all(any((reviewer, report) in reviews for reviewer in reviewers)
                                            for report in reports),
            "one_reviewer_for_all": any(all((reviewer, report) in reviews for report in reports)
                                        for reviewer in reviewers),
            "all_enrolled_passed": enrolled <= passed,
            "someone_enrolled": bool(enrolled),
            "aliases_equal": structure["constants"]["first"] == structure["constants"]["alias"],
        }
        self.assertEqual(derived, lab["reference"]["values"])
        self.assertEqual(set(derived), set(lab["input"]["formulae"]))
        for name, formula in lab["input"]["formulae"].items():
            with self.subTest(formula=name):
                observed = evaluate_in_structure(formula, structure)
                self.assertEqual(observed["value"], derived[name])
                self.assertEqual(observed["claim_scope"], lab["reference"]["claim_scope"])
                self.assertEqual(observed["required_steps"], observed["steps_used"])

    def test_l04_exact_posteriors_follow_from_complete_joint_counts(self):
        lab = self.labs["F01-L04"]
        task = lab["input"]
        cells = {}
        for row in task["joint_counts"]:
            key = tuple(row[event] for event in task["events"])
            self.assertTrue(all(type(flag) is bool for flag in key))
            self.assertIs(type(row["count"]), int)
            self.assertGreaterEqual(row["count"], 0)
            self.assertNotIn(key, cells)
            cells[key] = row["count"]
        self.assertEqual(sum(cells.values()), task["population"])

        def count(**conditions):
            positions = {task["events"].index(name): value for name, value in conditions.items()}
            return sum(value for cell, value in cells.items() if all(cell[index] == flag for index, flag in positions.items()))

        population = task["population"]
        d, no_d = count(D=True), count(D=False)
        self.assertGreater(d, 0)
        self.assertGreater(no_d, 0)
        prior = Fraction(d, population)
        sensitivity_1 = Fraction(count(D=True, E1=True), d)
        sensitivity_2 = Fraction(count(D=True, E2=True), d)
        false_positive_1 = Fraction(count(D=False, E1=True), no_d)
        false_positive_2 = Fraction(count(D=False, E2=True), no_d)
        posterior = Fraction(count(D=True, E1=True, E2=True), count(E1=True, E2=True))
        wrong_numerator = prior * sensitivity_1 * sensitivity_2
        wrong_denominator = wrong_numerator + (1 - prior) * false_positive_1 * false_positive_2
        derived = {
            "prior": prior,
            "sensitivity": sensitivity_1,
            "false_positive_rate": false_positive_1,
            "posterior_both": posterior,
            "erroneous_independence_posterior": wrong_numerator / wrong_denominator,
        }
        for name, expected in derived.items():
            with self.subTest(quantity=name):
                self.assertEqual(Fraction(lab["reference"][name]), expected)
        # Verify the dependency claim from the supplied data, rather than
        # simply accepting the prose that calls E2 a copy of E1.
        self.assertEqual(count(E1=True, E2=False) + count(E1=False, E2=True), 0)
        self.assertEqual(posterior, Fraction(count(D=True, E1=True), count(E1=True)))
        self.assertGreater(derived["erroneous_independence_posterior"], posterior)

    def test_l07_mutations_are_the_stated_structural_changes(self):
        lab = self.labs["F01-L07"]
        cases = {case["id"]: case for case in lab["input"]["cases"]}
        self.assertEqual(len(cases), len(lab["input"]["cases"]))
        base = cases["base"]
        mapping = lab["input"]["renaming_map"]
        self.assertEqual(len(mapping), len(set(mapping.values())))
        self.assertEqual(cases["renamed"]["premises"], [rename(formula, mapping) for formula in base["premises"]])
        self.assertEqual(cases["renamed"]["conclusion"], rename(base["conclusion"], mapping))
        base_counts = Counter(canonical(formula) for formula in base["premises"])
        duplicate_counts = Counter(canonical(formula) for formula in cases["duplicate"]["premises"])
        self.assertEqual(set(base_counts), set(duplicate_counts))
        self.assertTrue(all(duplicate_counts[key] >= count for key, count in base_counts.items()))
        self.assertEqual(sum(duplicate_counts.values()), sum(base_counts.values()) + 1)
        self.assertEqual(cases["removed_activation"]["premises"], base["premises"][:-1])
        self.assertEqual(cases["added_contradiction"]["premises"],
                         base["premises"] + [{"op": "not", "args": [base["premises"][-1]]}])
        for name in ("duplicate", "removed_activation", "added_contradiction"):
            self.assertEqual(cases[name]["conclusion"], base["conclusion"])

    def test_l07_exhaustive_results_and_invariance(self):
        lab = self.labs["F01-L07"]
        observed = {case["id"]: analyse_argument(case["premises"], case["conclusion"])
                    for case in lab["input"]["cases"]}
        self.assertEqual(set(observed), set(lab["reference"]["case_results"]))
        for name, reference in lab["reference"]["case_results"].items():
            with self.subTest(case=name):
                self.assertEqual({field: observed[name][field] for field in reference}, reference)
        invariant_fields = ("valid", "premises_consistent", "assignments_checked", "satisfying_premise_assignments")
        for name in ("renamed", "duplicate"):
            self.assertEqual({field: observed[name][field] for field in invariant_fields},
                             {field: observed["base"][field] for field in invariant_fields})
        removed = next(case for case in lab["input"]["cases"] if case["id"] == "removed_activation")
        witness = observed["removed_activation"]["counterexample"]
        self.assertIsNotNone(witness)
        self.assertTrue(all(value_under(premise, witness) for premise in removed["premises"]))
        self.assertFalse(value_under(removed["conclusion"], witness))
        self.assertEqual(observed["added_contradiction"]["satisfying_premise_assignments"], 0)


if __name__ == "__main__":
    unittest.main()
