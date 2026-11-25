# Atlas Agent School: Public Curriculum and Research Methods

**Public edition 1.0.0 | 13 November 2026 | Tan Sin Hon Albert**

Public repository: https://github.com/Albertito-AI/atlas-agent-school-public

This is a selected teaching and research package for studying software-agent reasoning. It combines original lessons on logic and evidence with synthetic practice problems, formal verification utilities and an explicit evaluation protocol.

It is a publication edition exported from the private Atlas Agent School development core. It provides self-study and research materials. It does not operate a school service, enrol learners, award a qualification or establish that a model has improved.

## What is included

| Component | Contents |
| --- | --- |
| F01 core | Eight lessons on claims, evidence, logical validity, scope, quantifiers, uncertainty, source authority, criticism and decision reports |
| Practice | Forty original diagnostic questions with public reference answers and remediation notes |
| Laboratories | Eight computational and evidence-analysis contracts, including countermodels, inconsistent subsets, finite structures, correlated evidence and metamorphic checks |
| Capstones | Four integrated synthetic scenarios with public review guidance |
| Reference software | Bounded propositional and finite first-order checkers with independent mathematical fixture tests |
| Methods | Educational principles, feedback guidance, anchored review rubric and proposed controlled evaluation design |

Begin with [the curriculum guide](curriculum/foundation-01/README.md). The [educational principles](methods/EDUCATIONAL_PRINCIPLES.md) describe the intended approach. [Research foundations](methods/RESEARCH_FOUNDATIONS.md) explain related work and the limits of the design inference.

## Run the reference examples

Python 3.10 or later and its standard library are sufficient. No API, model subscription, network connection or school credentials are required.

```bash
python3 -m agent_school.foundation logic --input curriculum/foundation-01/examples/propositional-input.json
python3 -m agent_school.foundation finite --input curriculum/foundation-01/examples/finite-input.json
python3 -m unittest discover -s tests -v
python3 scripts/verify_release.py
```

The first example produces an exhaustive propositional result within the checker's accepted bounds. The second evaluates a formula in one supplied finite interpretation. A successful software test or known-answer exercise is evidence about that artifact and its stated conditions.

## Using the material

Read a unit, attempt its practice tasks, inspect a reference answer after the attempt, diagnose any error, then produce a fresh transfer artifact. Preserve initial failures and subsequent repairs. The laboratory and capstone contracts require short external justifications, evidence references, formal objects or calculations. No private internal model deliberation is required.

All supplied answers and reference points are public teaching material. They must not be represented as unseen examinations. The proposed evaluation protocol separates instruction from extra inference effort and calls for independent task families, frozen configurations and declared uncertainty. No such learner evaluation is reported by this release.

## Release boundary

The edition contains the base F01 educational core only. It excludes the operational OX1 extension, the unreconciled F02 source collection, private cohort records, admissions and identity infrastructure, security-sensitive operations, payment records and private assessment systems. The capstone F01-C04 uses a self-contained fictional readiness fixture.

`PROVENANCE.json` records the pinned source revision, source paths, export adaptations and file hashes. `RELEASE_REVIEW.md` states what was checked and what remains unverified. The private source repository's history is not included.

## Related software example

[Colibri Atlas: Evidence Replay 0.1.0a1](https://github.com/Albertito-AI/colibri-atlas/tree/main/examples/atlas_evidence) is a separate public
prototype for checking candidate quotations against supplied source snapshots.
It combines optional Atlas Reweave policy rechecks with a RegNav Source Watch
manifest whose automated evidence relations are labelled `context`. Its fictional
demonstration can be inspected alongside the distinction between literal evidence
and substantive judgement taught here; it is not part of this curriculum edition.

Archived related software release: [Evidence Replay 0.1.0a1 (public prototype)](https://doi.org/10.5281/zenodo.24206408).

The [validation record](https://github.com/Albertito-AI/colibri-atlas/blob/main/examples/atlas_evidence/VALIDATION.md) reports **48 tests passed, zero skips**,
including Colibri's actual HTTP gateway with a scripted engine double. These are
software checks, not a learner evaluation or a real-model quality study. Exact
quotation agreement does not establish semantic support for a candidate claim.

## Citation and rights

Use [CITATION.cff](CITATION.cff) and the public edition's DOI once assigned. The DOI identifies this selected version, rather than the entire private institution or future revisions.

The original material remains under [reserved rights](RIGHTS.md). Third-party sources retain their existing rights and attribution. Public availability does not apply a blanket open-source licence.

## Sport governance teaching application

Assign a records agent, a finance reviewer and an athlete representative different evidence in the venue exercise. Compare their answers before a director signs. [Exercise and records](https://github.com/Albertito-AI/sport-governance-and-administration/blob/main/lab/README.md) · [Albert Tan’s book and teaching companion](https://alberttansinhon.com/sport-governance/).
