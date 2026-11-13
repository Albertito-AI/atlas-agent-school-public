# F01 public core: Logic, Evidence and Responsible Action

**Selected public edition 1.0.0 | Eight units, forty practice items, eight laboratories and four capstones**

The purpose is to help a software learner reconstruct arguments, check formal consequences, inspect premise support, preserve scope and authority, and report a bounded result. These are intended outcomes to be evaluated, rather than demonstrated educational effects.

## Sequence

1. [Claims, arguments and evidence](lessons/01-claims-and-evidence.md).
2. [Validity, soundness and countermodels](lessons/02-validity-and-countermodels.md).
3. [Conditionals, definitions and scope](lessons/03-conditionals-and-scope.md).
4. [Quantifiers, relations and coverage](lessons/04-quantifiers-and-coverage.md).
5. [Uncertainty, induction and causation](lessons/05-uncertainty-and-causation.md).
6. [Sources, tool results and authority](lessons/06-sources-and-authority.md).
7. [Criticism, disagreement and repair](lessons/07-criticism-and-repair.md).
8. [Integrated decision reports](lessons/08-integrated-reports.md).

Each lesson has an original worked example, transfer prompt and reading references. The forty items in [practice.json](practice.json) supply diagnostic answers and remediation. Complete the [eight laboratories](LABS.md) and [four capstones](capstones.json) with inspectable artifacts. All reference answers are public development material.

## Instructions and review

- Read [AGENT_SPEC.md](AGENT_SPEC.md) for formal representations and tool bounds.
- Use [response-template.json](response-template.json) for a concise external decision record.
- Use the [teacher guide](teacher-guide.md) for feedback and fresh practice.
- Use the [assessment protocol](assessment.md) for anchored review and a proposed controlled study.
- Consult [SOURCES.md](SOURCES.md) for the dated historical bibliographic record and its limitations.

No full classroom, operational enrolment service or automatic six-dimensional capstone grader is provided. The small command-line utility supports only the two formal-checker modes described in the root README. The OX1 operational extension and F02 module are outside this public core edition.

## Formal scope

The propositional utility uses classical two-valued logic and exhaustive bounded valuation enumeration. The finite first-order utility evaluates a closed formula in a supplied non-empty finite domain. Predicate extensions can be empty. An omitted tuple is false in a fully specified model; missing real-world evidence is not thereby false.

The formal checkers do not establish empirical premise truth, source reliability, causal validity, general intelligence or authority to act. Record the symbol interpretation and explain what the formalisation leaves out.
