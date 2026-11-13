# U05: Uncertainty, induction and causation

## What the learner should produce

A qualified inference that states its data, denominator, assumptions and uncertainty. When a numerical probability is appropriate, show a short reproducible calculation. When the evidence is insufficient for a defensible probability, say so and identify what would improve the estimate.

## Lesson

Deduction preserves truth from premises in a valid argument. Induction supports a broader conclusion with some uncertainty. Abductive reasoning compares candidate explanations. A useful explanation can be a hypothesis even when it is not yet established as the cause.

More data can improve an estimate when the observations are relevant and the sampling process supports the inference. A larger biased sample can preserve or worsen a systematic error. Repeated outputs from closely related configurations, or sources repeating one original report, may add much less independent evidence than their count suggests.

Do not assign a numerical confidence merely to sound precise. A probability should identify the event, evidence, population and method that gives the number meaning. An agent's verbal confidence has not been calibrated just because it is expressed as a percentage.

## Worked example: a base-rate calculation

In a synthetic population of 1,000 jobs, exactly 100 contain a defect. A detector flags 90 of those 100 and also flags 90 of the 900 non-defective jobs. Among 180 flagged jobs, 90 are defective. Therefore the observed fraction defective among flagged jobs is `90 / 180 = 1/2`.

The detector's 90% sensitivity is `P(flag | defect)`. The requested quantity is `P(defect | flag)`. These are different conditional probabilities. Under the stipulated rates:

`P(defect | flag) = (0.9 * 0.1) / ((0.9 * 0.1) + (0.1 * 0.9)) = 0.5`.

This result depends on the stated population and rates. It is not a universal probability for every detector alert. If the population or operating conditions change, verify whether the inputs remain applicable. If `P(flag)=0`, this conditional probability is undefined by the usual ratio rather than equal to zero.

## Causal claims

A performance increase after a lesson is compatible with several explanations: the lesson, more attempts, different tasks, additional tool access, changed prompts, chance or examination leakage. Temporal order alone does not identify the cause.

A useful comparison holds the learner configuration and conditions stable, allocates comparable unfamiliar tasks, records all attempts, and includes an equal-effort comparison. Randomisation and a suitable design can strengthen causal interpretation, but a very small pilot still has limited precision and scope. The school's assessment protocol treats these as design requirements for investigation rather than guarantees of an effect.

With an alleged system failure, ask what alternative cause predicts a different observable result. Prefer a bounded discriminating check over an elaborate story that fits every possible outcome. Simpler explanations can be helpful, but simplicity alone is not evidence that the explanation is true.

## Procedure

1. Classify the inference as deductive, statistical, explanatory or decision-oriented.
2. Identify the population, sampling process and relevant comparison.
3. Distinguish a conditional probability from its converse.
4. Check arithmetic with exact fractions or a calculator where possible.
5. State assumptions, alternative explanations and material missing data.
6. Choose the next observation that would most directly resolve the decision.

## Transfer prompt

The same agent scored 6/10 before a lesson and 9/10 afterwards. The second test repeated the first test's questions and allowed three retries. Explain what the two observations show, why they do not isolate a teaching effect, and how a future trial could improve the comparison.

## Reading

S02, S03 chapter 2, S05 chapter 3 and S06 chapter 5 provide the reviewed material on inductive or explanatory reasoning; the [source register](../SOURCES.md) gives exact locations and qualifications. The numerical detector example, experimental controls and application to agents are original school material. Human teaching sources S09 and S10 inform the instructional design, with their scope explicitly limited.
