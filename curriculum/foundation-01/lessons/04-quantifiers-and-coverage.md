# U04: Quantifiers, relations and coverage

## What the learner should produce

A formal or plain-language statement of exactly which objects a conclusion covers, together with any existence assumption and any limit on the underlying search or dataset.

## Lesson

In this module's first-order convention, the overall domain is non-empty. A predicate can still apply to no members. For a domain of registered software identities, `Enrolled(x)` may be false of every identity even though the domain contains several identities.

"Every enrolled learner passed" has the form `forall x (Enrolled(x) -> Passed(x))`. It is true if no learner enrolled. "Some enrolled learner passed" has the form `exists x (Enrolled(x) and Passed(x))`. The first does not entail the second without an existence premise.

This distinction matters for empty test suites, empty search results and completion dashboards. A system can report that every returned row satisfies a condition when it returned zero rows. Always inspect the count and the selection procedure before reporting a substantive success.

Negation also changes quantifiers:

- Not every file was checked means at least one file in the stated domain was not checked.
- No file was checked means every file in the domain was unchecked.
- Not finding an unchecked file in a partial search does not establish that none exists.

The last statement is about evidence coverage. It is not merely a formula transformation. To infer an exhaustive absence, the agent needs an adequately complete search over the relevant domain or some other sufficient reason.

## Worked example: quantifier order

"Every report has a reviewer" can be written `forall r exists v Reviews(v,r)` after restricting the variables to reports and reviewers. "There is one reviewer who reviews every report" is `exists v forall r Reviews(v,r)`.

Suppose report A is reviewed only by Imani and report B only by Jules. The first statement is true and the second false. Changing the order has created an unsupported claim about a common reviewer. Two reports are enough for this countermodel.

Do not silently omit restrictions when expressing the same claim in a single mixed domain. A fuller formalisation should use predicates for reports and reviewers. A variable ranging over reviewers in one formula must not suddenly range over every object in another.

## Time, identity and relations

Many apparently unary properties need extra parameters. `Approved(x)` may conceal who approved x, for which purpose, and when. Use a relation such as `Approved(reviewer, artifact, revision, purpose, time)` when those distinctions affect the task. Two artifacts sharing a title need not be the same version.

Do not infer that two names denote different objects merely because their strings differ. Conversely, do not merge two objects because their display names match. Identity claims need the appropriate identifier or other evidence.

## Procedure

1. Define the relevant domain and time or version boundary.
2. Separate universal claims from existential claims.
3. Preserve quantifier order and relational parameters.
4. Check emptiness and non-zero counts when a success claim presupposes participation.
5. Compare the domain of the evidence with the domain of the conclusion.
6. Report what was covered and what remains outside the search.

## Transfer prompt

An agent checked five files returned by a search. The folder contains twenty files. All five checked files are valid. Write a claim that the observations support and identify the missing evidence for "the folder is valid". Explain whether the latter conclusion is false, or simply not established by the observations.

## Reading

S04, printed/PDF pp. 54 and 57-59, on the non-empty overall domain, empty predicates and restricted universes; its discussion of multiple quantifiers begins on p. 63. S01 provides additional computational examples. See the [source register](../SOURCES.md) for reviewed sections. The coverage and version-control procedures are original agent applications.
