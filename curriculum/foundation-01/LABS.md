# Computational laboratories

**F01 v1.0.0 | Required agent track | Public development material**

The eight laboratories require agents to construct artifacts that another process can inspect. They are integral to the foundation. Exact-answer practice alone does not complete the module. The full inputs, output obligations and reference points are in [labs.json](labs.json).

## Contracts

| Laboratory | Required reasoning | Artifact |
| --- | --- | --- |
| F01-L01 | Derive a multi-step consequence, audit the converse, separate validity from empirical support. | Propositional AST, exhaustive result, short proof and countermodel. |
| F01-L02 | Enumerate inclusion-minimal inconsistent subsets and inclusion-minimal consistency repairs; choose a repair using stipulated provenance. | Complete conflict/removal sets, satisfying witness and retained history. |
| F01-L03 | Evaluate mixed-domain quantified statements, demonstrate quantifier-order failure, diagnose empty predicates and co-referring constants. | Finite structure, closed formulae, truth values and scope explanation. |
| F01-L04 | Derive exact conditional probabilities from a complete joint table and expose a false independence assumption. | Fractions, checked denominators, dependency account and missing-input analysis. |
| F01-L05 | Recompute an evidence graph after a version change without losing valid historical observations. | Versioned claim keys, support edges, invalidated conclusions and justified next checks. |
| F01-L06 | Bind jobs, revisions, targets and legitimate authority across an adversarial trace. | Event classification, allowed action transitions and accurate state report. |
| F01-L07 | Test variable-renaming invariance, premise duplication, premise removal and contradictory additions. | Metamorphic test records, countermodel and one original mutation. |
| F01-L08 | Critique an alleged learning effect, disentangle confounds and produce a constrained experimental proposal. | Decision record, evidence graph, controlled comparison design and reusable procedure. |

## How to execute

Read [AGENT_SPEC.md](AGENT_SPEC.md) first. Treat a lab's supplied structure or numerical table as complete only when the contract says so. Preserve every stated domain, source, time and revision. A real-world missing observation is not automatically a false predicate in a complete model.

Return the artifacts requested by each lab. The [response template](response-template.json) provides a common handoff record; formal input, calculations and dependency graphs can be companion objects. Include the lab ID, module version, actual learner configuration and tools used in a real run. Leave them unobserved in templates rather than inventing a learner.

For the supplied executable examples, run from the repository root:

```bash
python -m agent_school.foundation logic --input curriculum/foundation-01/examples/propositional-input.json
python -m agent_school.foundation finite --input curriculum/foundation-01/examples/finite-input.json
python -m unittest discover -s tests -p 'test_foundation_labs.py' -v
```

The first example is L01's main argument. The second is L03's statement that each report has a reviewer in its explicitly supplied structure. Both files are public reference inputs.

To investigate L02, enumerate subsets of the five labelled premises and test consistency. A subset is minimally inconsistent when it is inconsistent and every proper subset is consistent. A removal set is a minimal repair when the retained set is consistent and no proper subset of that removal set suffices. Inclusion-minimal and minimum-cardinality are different criteria. The reference verification tests independently enumerate the candidates and compare the complete result sets.

For L04, derive the counts from the joint table and use exact rational arithmetic, for example Python's `fractions.Fraction`. Verify that the counts are non-negative and total 1,000. Conditioning on both copied alerts selects the same 180 cases as conditioning on the first. If independence is imposed incorrectly, the resulting 9/10 posterior describes the mistaken calculation, not the actual table.

For L05 and L06, the main difficulty is semantic and operational. A formal checker can verify a supplied implication but cannot decide whether a log actually concerns the required revision or whether its origin supplies legitimate authority. Produce the binding and provenance evidence explicitly.

For L07, uniform renaming must preserve the whole formula, including every occurrence. Duplicating a premise changes neither its models nor its consequences. Removing a premise can admit countermodels. Adding an inconsistent premise can preserve classical validity while destroying consistency. Report both properties so a superficially favourable validity field does not hide the defect.

For L08, separate the observed numerical difference from its proposed causal interpretation. A difference between model revisions, task exposures or tool access is part of the comparison record. The authorised output is an internal evaluation proposal. No external service should be contacted and no publication action should be taken.

## Verification and review

The reference tests independently verify mathematical subsets of L01-L04 and L07. These tests check the correctness of the published teaching artifacts. They are not a grader for arbitrary learner submissions and are not evidence of learner improvement.

The full lab response, including faithful translation, evidence provenance, interpretation, uncertainty and action choice, requires recorded review under [assessment.md](assessment.md). Review an unsuccessful attempt, identify the specific defect and request a fresh development variant after correction. Retain the initial failure.

Every reference answer in this repository is public. Self-generated tasks, renamed examples and repeated known answers must remain labelled as development work. Any future independent examination requires a separate protected process outside this public package.

## Extension problems

After the required labs, a teacher may increase the number of premises, nest quantifiers, vary relation arity, introduce richer dependency structures or require a formally specified proof system. Each extension needs an appropriate verification method, defined semantics and resource limits. A larger input rejected by the present checker is a tooling boundary. Do not mistake rejection for an answer about logical validity, and do not waive verification because a problem appears too difficult for a human reader.
