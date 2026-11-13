# U08: Integrated decision reports

## What the learner should produce

A concise decision record that another agent or a human steward can inspect. Its length should reflect the task. A simple fact can need one source and two sentences; a contested action may need a structured record.

## Lesson

The first seven units support a complete workflow. Start with the actual question and authority. Reconstruct the relevant argument. Check translation, logical support and source support separately. Resolve uncertainty where it matters to the next action. Report what was observed and what remains uncertain.

An external justification can contain premises, references, a short proof, a calculation, a countermodel or a tool result. The school assesses these checkable products and the resulting behaviour. It does not require a transcript of a model's private internal reasoning, nor does such a transcript independently establish that a conclusion is correct.

The provided `response-template.json` includes:

- Task and version identifiers.
- Conclusion and status.
- Evidence references and what each establishes.
- Assumptions and applicability limits.
- Inference type and a short verification artifact.
- Authorised next action or completion evidence.
- Revision information where relevant.

Never fill a field with a fabricated observation merely because the template expects a value. An empty list or an explicit `not established` can be correct. Proportionality also matters: if the evidence and valid authority are already sufficient, complete the work rather than creating avoidable permission loops.

## Worked example

**Task:** determine whether the current documentation update can be reported as published. **Authority:** the owner has authorised that update. **Observations:** a write request was accepted for revision R8; the live page still shows R7; no completed deployment result for R8 has been obtained.

**Conclusion:** publication of R8 is not yet established. **Reason:** acceptance of the write request does not entail the final live state, and the current read-back shows R7. **Next action:** inspect the deployment record and repeat a targeted read-back after any reported successful completion. **Scope:** this record concerns the specified page and revision, not the availability of the whole site.

If the later read-back shows the expected R8 content at the authorised target, update the conclusion and retain the earlier observation. The earlier report was an accurate account of its time, not necessarily a failure.

## Self-review before submission

Ask five questions:

1. Does every material claim have adequate support, or an explicit assumption/uncertainty label?
2. Have I changed the meaning, quantifier, time, domain or version across an inference?
3. Would a countermodel or alternative explanation defeat the claimed level of certainty?
4. Is the next action permitted, and does it actually resolve the task?
5. Does the completion statement identify an observed result that matches what the user asked for?

Use a formal checker when the problem has a suitable finite formalisation. Use source inspection for textual claims and an appropriate domain reviewer for contested specialist judgements. One technique does not replace all others.

## Capstone work

The four public capstones concern release verification, dataset coverage and base rates, a contested source interpretation, and multi-agent repair. Complete all four using the response structure. The [assessment protocol](../assessment.md) provides anchored criteria for reviewing explanations, limitations and actions.

A teacher can use the public reference points to give feedback. A completion record based on these public tasks must say that the tasks were public and familiar. A genuine examination uses separately controlled, unseen problem families and records the learner configuration, available tools and review method.

## Reading

This unit synthesises the earlier logic lessons and the school's existing teaching policy. S09's historical discussion of testing application and S10's case-based instructional proposals inform the design by analogy to human education. Neither source demonstrates improvement in software agents. See the [source register](../SOURCES.md) and [teacher guide](../teacher-guide.md).
