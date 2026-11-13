# U02: Validity, soundness and countermodels

## What the learner should produce

A validity judgement with a checkable basis, accompanied by a separate statement about premise support. For an invalid argument, produce one interpretation in which every premise is true and the conclusion is false. For a valid propositional argument, provide a short proof or a complete bounded truth-table result for the stated formalisation.

## Lesson

In classical logic, an argument is valid when no interpretation makes all its premises true and its conclusion false. Soundness requires validity and true premises. Actual truth of a conclusion does not validate the route used to reach it. An invalid inference can happen to reach a true conclusion; a valid inference from false premises can reach a false conclusion.

For agent work, keep three questions separate:

1. Did we translate the claim faithfully?
2. Does the conclusion follow under that formalisation?
3. What supports the premises in the actual task?

A truth-table checker addresses the second question within its supported language. It cannot independently answer the first or third. Formalising "approved" as a single atom will conceal an ambiguity if one document means "approved for testing" and another means "approved for production".

## Worked example: an invalid converse

Let `A` mean "this run used the reviewed configuration" and `B` mean "this run passed the practice test". Suppose the exercise explicitly stipulates `A -> B`. The agent observes `B` and concludes `A`.

The argument is invalid. Use `A=false, B=true`: the conditional and the observed pass are both true, while the conclusion is false. Other configurations might also pass. This countermodel establishes a defect in the inference even if further evidence later establishes `A`.

By contrast, `A -> B; A; therefore B` is valid. Whether it is sound in a real evaluation still depends on the truth of the universal conditional and the configuration claim.

## Consistency and vacuous validity

A premise set is consistent if at least one interpretation makes all its members true. An inconsistent set has no such interpretation. Under classical semantic consequence, an inconsistent set entails every formula because there is no interpretation with all premises true and the conclusion false.

This is a property of the consequence relation. It is a poor operational basis for treating arbitrary claims as established. When two credible records conflict, isolate the incompatible premises, check versions and scope, and refrain from using the inconsistency to justify an unrelated action. The local checker reports premise consistency alongside validity for this reason.

The same caution applies to a universal rule over an empty predicate. Its formal truth can be legitimate while its evidential value for a real-world success claim is negligible. Unit U04 develops this issue.

## What a search can establish

A genuine countermodel is sufficient to establish invalidity. A failed search for one is conclusive only when the method is complete for the stated problem and has actually completed. The bundled checker enumerates all assignments for at most eight propositional atoms, within its bounded input limits. A person or model saying "I cannot think of a counterexample" has not performed that complete search.

First-order validity over unrestricted structures is outside this checker. Testing a few finite structures cannot establish unrestricted first-order validity. Record the kind and bounds of a check so that its conclusion remains interpretable.

## Procedure

1. Define symbols and preserve distinctions in the original wording.
2. State the premises and conclusion separately.
3. Look for a countermodel; use a complete bounded method where appropriate.
4. Check whether the premise set itself is satisfiable.
5. Record validity and consistency without confusing them with verified premise truth.
6. Audit the translation and the evidence before using the conclusion in an action.

## Transfer prompt

Two logs assert `published` and `not published` for what appears to be the same release. A formal proof derives `safe_to_delete_backup`. Explain why this derivation cannot justify deleting anything. Specify the version, target, time and authority questions that need investigation.

## Reading

S04, printed/PDF pp. 8-9, on validity; p. 63, on a misleading translation that conceals different meanings. S07 and S08 provide complementary introductions to argument form and counterexamples. Full verified references are in the [source register](../SOURCES.md). The workflow and agent scenarios are original applications.
