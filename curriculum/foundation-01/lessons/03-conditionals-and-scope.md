# U03: Conditionals, definitions and scope

## What the learner should produce

A translation of a rule that states the direction of implication, the relevant domain and any conditions or exceptions. Explain which conclusions follow and which require additional premises.

## Lesson

Under a material-conditional reading, `P -> Q` is false only when `P` is true and `Q` is false. It says that `P` is sufficient for `Q` and `Q` is necessary for `P`. It does not also say `Q -> P`. The biconditional `P <-> Q` supplies both directions.

| Wording under the stipulated classical reading | Form |
| --- | --- |
| P only if Q | P -> Q |
| P if Q | Q -> P |
| P is sufficient for Q | P -> Q |
| P is necessary for Q | Q -> P |
| P if and only if Q | (P -> Q) and (Q -> P) |
| Not both P and Q | not (P and Q) |
| Neither P nor Q | (not P) and (not Q) |
| Not every item is P | Some item is not P, within the stated domain. |

Do not force every ordinary-language "if" into a material conditional without interpretation. A promise, a causal explanation, an exception-bearing policy and a hypothetical counterfactual make different commitments. The formal representation should state the intended reading.

Authorization is especially easy to misread. "Publishing requires approval" gives a necessary condition for permitted publication. Approval alone may leave other requirements unsatisfied. A truth-valued account of what a policy says is also distinct from the policy's legitimate authority over the current task.

## Worked example

The stipulated policy says: "A release may be published only if it has owner approval and its current build passes the required checks."

Let `P` mean permitted publication, `A` mean owner approval, and `T` mean current required checks passed. The rule gives `P -> (A and T)`. It does not, by itself, give `(A and T) -> P`. There could be an additional embargo. Nor does passing an earlier build establish `T` for the current build.

To derive permission from `A and T`, a source must establish that these conditions are sufficient in this context. When the real task already contains complete valid authority, use it; do not add repetitive approval requests. The lesson is to preserve actual conditions, including their sufficiency where provided.

## Definitions and equivocation

A definition can settle how a term is used in a specified system. It does not establish that the defined object exists, that a policy is justified, or that an empirical property holds. Declaring a field `verified=true` is not the same event as independently verifying a claim.

Preserve qualifiers across an inference. "Reliable on these tests" and "reliable on all future tasks" denote different claims. Similarly, "agent" may mean an authenticated client, an approved process or a model-backed system. An argument that changes the meaning halfway through can appear valid when its symbols hide the change.

## Common invalid patterns

- `P -> Q; Q; therefore P`: affirming the consequent.
- `P -> Q; not P; therefore not Q`: denying the antecedent.

Their valid counterparts include modus ponens (`P -> Q; P; therefore Q`) and modus tollens (`P -> Q; not Q; therefore not P`). The latter requires the conditional and negation to use the same meaning and scope.

## Transfer prompt

A release note says, "Only checked files enter the package." The package is empty. Identify what follows about checking and existence. Then explain why a parser that reads "only" in the wrong direction could falsely claim completeness.

## Reading and correction

S04, printed/PDF pp. 24-25, on conditionals; S05, section 2.7, on conditional translation. S03 chapter 5 is useful supplementary reading, but its uploaded p. 47 contains a prose reversal of a necessity relation. This module uses `A -> B` to mean A sufficient for B and B necessary for A; the correction and exact location are recorded in the [source register](../SOURCES.md).
