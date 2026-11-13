# U01: Claims, arguments and evidence

## What the learner should produce

A short reconstruction that identifies the conclusion, its premises, each premise's origin and any missing bridge. Preserve qualifiers such as "some", "in this sample", "may" and "as of this revision". A useful reconstruction makes disagreement local: another agent should be able to identify which premise or inference it disputes.

## Lesson

An argument presents premises as reasons for a conclusion. An explanation may instead start with an accepted event and ask why it occurred. The same sentence can serve different roles in different contexts. Identify what the task asks you to establish before assigning roles.

Separate a proposition from the evidence for it. "The report says the service is healthy" is a proposition about a report. "The service is healthy" is a proposition about the service. Reading the report can establish the first while leaving the second uncertain. A quotation, measurement or database response has its own conditions: who produced it, what it covers, and when it was obtained.

Use these operational categories:

| Category | Example | Check |
| --- | --- | --- |
| Task instruction | "Inspect the deployment; do not publish." | Identify the authorised actor, action and scope. |
| Observation | A specific read-back returned revision 42. | Preserve the tool result, target and time. |
| Source claim | The release note calls revision 42 stable. | Verify the wording and the meaning of stable. |
| Assumption | The supplied list contains every deployment. | Mark the assumption and seek coverage evidence. |
| Inference | Therefore the requested revision is live. | Identify the bridge from the observation to this claim. |
| Proposal | Run an additional check. | Explain why it would resolve a material uncertainty. |

These categories are an agent workflow designed by the school. They are not a claim that the source authors prescribe this exact interface. A command can matter operationally even though it is not itself a truth-valued assertion in the classical logic introduced here.

Reconstruction should be charitable and faithful. Supply a missing premise only as an explicit candidate. Do not quietly improve an argument and then report that the original source established the improved conclusion. If a premise is absent, state what additional proposition would make the inference work and whether it is justified.

## Worked example

The task is to determine whether a requested change is live. A tool returns: `{"job_id":"J7","status":"queued"}`. Another agent says, "The change is complete because the tool returned a job identifier."

- Observed premise: the service accepted a job and returned the status `queued`.
- Proposed conclusion: the change is live.
- Missing bridge: every queued job has already completed successfully and affected the intended target.
- Assessment: the bridge is unsupported and the provided status does not establish completion.
- Appropriate next action: inspect the job state and, if it reports success, verify the target revision where the task requires live-state confirmation.

The correct report is "The job was queued; completion is not yet established." It would also be inaccurate to report that the deployment definitely failed. The available evidence supports neither completed nor failed.

## Procedure

1. State the exact question, including time, target and scope.
2. Separate premises from the proposed conclusion.
3. Attach an origin or explicit assumption label to each premise.
4. Identify any extra bridge the conclusion needs.
5. Decide whether the bridge is a logical relation, an empirical claim, a definition or an authorised policy.
6. Check that kind of bridge using an appropriate method.
7. Report the strongest supported conclusion and a proportionate next step.

## Common error and repair

**Error:** treating a sentence's confident tone, repeated appearance or position in a tool response as proof. **Repair:** ask what observation would differ if the sentence were wrong. Trace the claim to evidence that can bear on it.

**Error:** treating unsupported as false. **Repair:** record "not established" unless evidence also supports the negation.

## Transfer prompt

A search result says that a document contains a particular rule. The document has not been opened. Write a two-sentence status report that distinguishes discovery from verification, and identify the next check. Do not invent a quotation or page number.

## Reading

S04, *forallx*, printed/PDF pp. 5-9, on arguments, sentences and validity. S05, chapter 1, on reconstruction and missing premises; precise edition-specific locations are in the [source register](../SOURCES.md). The queued-job example and operational categories are original school applications.
