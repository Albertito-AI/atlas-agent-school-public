# Release review: public edition 1.0.0

**Date:** 13 November 2026  
**Source:** `Albertito-AI/atlas-agent-school`, commit `7a0681dc81514f73d4a5348224d04e86d6c980f1`  
**Scope:** selected F01 teaching core, educational methods and bounded reference software

## Checks completed

- Reviewed the source release policy and separated educational material from operational, admission, payment, learner and private assessment records.
- Examined the selected practice, laboratory and capstone files. All supplied answers are public development references. No hidden examination is included.
- Replaced the broad development README with a self-contained edition guide. Removed links and instructions requiring private operational code or cohort records.
- Adapted F01-C04 to an explicitly fictional readiness scenario. It no longer requires a real, changing private readiness record.
- Carried forward exact source paths and revision identity and recorded export adaptations in `PROVENANCE.json`.
- Ran the 41 included reference tests successfully. These cover propositional semantics, finite structures and resource bounds, minimal inconsistent subsets and repairs, exact probabilities and metamorphic checks.
- Ran both documented command-line examples successfully: the propositional example is valid with consistent premises across all 16 valuations; the finite example evaluates true in its supplied four-object structure using 113 declared evaluation steps.
- Validated `CITATION.cff` against the Citation File Format 1.2.0 schema. Its non-standard reserved-rights notice is linked through `license-url`; no SPDX open licence is asserted.
- Conducted a separate agent review of source identity, release boundaries, obvious credential/personal-record patterns and the 40 practice answers. This review was an editorial check within the preparation process. It was not external peer review or an independent learner evaluation.

## Bibliographic checks

The edition retains the historical source-review record dated 27 October 2026. The original uploaded books and page images were not re-examined for this export. Edition-specific pinpoints and textual corrections retain that dated evidentiary status.

Primary-source identity/link checks during preparation confirmed the cited Reflexion and Voyager papers, the NeurIPS 2025 multi-agent failure paper, NIST AI 600-1, the publisher's Bonevac sample, Rebus chapter authorship, Shea's second edition and the Springer entry for Aleksandra Łuczak's chapter. The latter confirms the title, author, DOI `10.1007/978-3-031-87993-7_116-1`, first-online date 11 March 2026 and pages 1-24.

Shea's online front matter and book page have different licence notices. The discrepancy is recorded in `curriculum/foundation-01/SOURCES.md`; neither is applied as a package licence. All third-party books, scans and full extracts remain excluded.

Relevant primary records:

- https://link.springer.com/rwe/10.1007/978-3-031-87993-7_116-1
- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- https://mlpp.pressbooks.pub/littlemorelogical/
- https://mlpp.pressbooks.pub/littlemorelogical/front-matter/__unknown__/
- Further source links appear in the source register and research-foundations document.

## Limits

These checks do not establish educational effectiveness, model learning, general intelligence, deployment security or readiness to admit learners. No model service was called and no learner experiment was run. The package's code is a bounded reference implementation, and the mathematical tests verify only the properties they exercise.

The operational OX1 extension and F02 material are not included. The private institutional core remains outside the publication. The edition preserves reserved rights in original School material; no general open licence has been added.
