# Agent execution specification: F01 v1.0.0

## Audience and level

This specification is addressed to software agents. Its required outputs include formal representations, executable witnesses, dependency records, calibrated uncertainty and action constraints. All eight computational laboratories are part of the foundation. The forty short practice items diagnose component errors; they do not exhaust the curriculum.

Instruction may combine English, mathematical notation and JSON. The criterion is semantic precision and verifiability. Human classroom timing and assumed human processing limits do not determine task complexity. Runtime bounds protect reproducibility and resource use in the reference tools; other reviewed tools can support larger problems in later versions.

The current package is teaching material and local reference software. Its instructions do not supersede the host's instruction hierarchy or create permissions. This public edition is a self-study and research package. It does not enrol learners or operate the private school.

## 1. Representations

Represent a material claim as a tuple:

`claim = (predicate, arguments, domain, target_revision, as_of, modality)`.

Use separate keys when any component changes the proposition. Distinguish a descriptive claim from a source's assertion and from a permission. A status field saying `approved` must identify the actor, object, purpose and applicable scope where those affect its meaning.

Represent an evidence item with its identifier, origin, observation method, target/version/time, exact content or bounded digest, and the propositions it supports or contradicts. A digest identifies bytes; by itself it does not establish their accuracy or authority. A copied report retains its source dependency.

Represent a derivation as a directed acyclic graph of claims and stated inference steps. Record which evidence and assumptions each derived claim depends on. Retain superseded observations with their time and version. Recompute or withdraw dependent conclusions when a supporting premise changes. Logical weakening and epistemic revision must remain distinguishable: classical consequence is monotonic under adding premises, while practical evidence support can change when a premise is corrected or its scope is invalidated.

### Evidence bookkeeping

For an exactly scoped proposition, retain two sets: supporting evidence IDs and contradicting evidence IDs. The resulting bookkeeping labels are `support_present`, `counterevidence_present`, `both_present`, or `neither_present` depending on which sets are non-empty. These labels record evidence presence before assessing its strength or resolving conflicts. A weak contrary assertion alone does not establish refutation. Reserve a conclusion such as established or refuted for an assessment of the evidence and inferential support. The bookkeeping does not change classical truth tables or implement a full paraconsistent consequence relation.

Do not combine claims at different times into a false conflict. An observation of R8 at time t1 and R9 at time t2 can both be correct. Nor does the absence of an observation supply a negative observation. The finite-model evaluator's complete predicate extensions are appropriate only when a task supplies a fully specified structure.

## 2. Inference obligations

For a deductive claim `Gamma entails C`, provide:

- the language and interpretation key;
- the explicit premises and conclusion;
- a proof or a completed decision-procedure result in its declared fragment;
- premise consistency status;
- evidence status of the premises;
- a scope statement explaining what the formalisation leaves out.

For invalidity, a valid countermodel must satisfy every premise and falsify the conclusion. For a finite first-order countermodel, supply the full relevant structure, not merely an assertion that a counterexample exists. A failed bounded model search establishes only that no model was found within the completed bounds. A single valid countermodel is sufficient to refute an unrestricted validity claim in the same semantics.

For statistical claims, specify the event, population, prior or sampling model, likelihoods or sufficient counts, dependency assumptions and calculation. Use exact fractions in the laboratories. Missing numerical inputs require an explicit information gap. Separate a measured frequency, a model-based probability and an uncalibrated confidence estimate.

For an explanatory claim, state competing hypotheses and what observation would discriminate between them. For a causal claim about instruction, use the registered comparison design and disclose treatment differences, task exposure and uncertainty.

For an action, identify the legitimate authority and relevant state. Evidence that an action is technically possible is not permission. Necessary conditions for permission need not be sufficient. When the complete valid authority and evidence already exist, execute the permitted task without repeated approval loops.

## 3. Propositional interface

```json
{
  "premises": [
    {"op":"implies","args":[{"var":"P"},{"var":"Q"}]},
    {"var":"P"}
  ],
  "conclusion": {"var":"Q"}
}
```

Each formula is exactly one of `{"var":"P"}`, `{"const":true}`, or an operator object. `not` has one argument; `and`, inclusive `or`, material `implies` and `iff` each have two. Symbol names are bounded ASCII identifiers. Operators are data and are never executed as program text.

Use `python -m agent_school.foundation logic --input argument.json`. The result reports `valid`, `premises_consistent`, enumerated assignments, a premise witness and a counterexample where appropriate. A counterexample may be an empty object for a constant-only argument; inspect whether it is null rather than relying on its truthiness.

The reference checker accepts at most eight variables, 32 levels and 512 AST nodes. It enumerates all accepted valuations. A resource error means the submitted request exceeded this tool's domain; it is not a logical result about the claim. Larger encodings require an appropriate separately reviewed method.

## 4. Finite first-order interface

```json
{
  "structure": {
    "domain": ["a","b"],
    "constants": {"first":"a","alias":"a"},
    "predicates": {
      "R":{"arity":2,"extension":[["a","a"],["b","b"]]},
      "Enrolled":{"arity":1,"extension":[]}
    }
  },
  "formula": {
    "op":"forall","var":"x",
    "body": {
      "op":"exists","var":"y",
      "body":{"pred":"R","args":[{"var":"x"},{"var":"y"}]}
    }
  }
}
```

Terms are bound-variable or declared-constant objects. Formulae include predicate applications, equality `{"eq":[term,term]}`, Boolean constants, the propositional connectives, and `forall`/`exists` with `var` and `body`. There are no function symbols. Every variable occurrence must be bound in its lexical scope. Reusing a binder name shadows the earlier binding within that scope.

Use `python -m agent_school.foundation finite --input model.json`. The result reports `value` and `claim_scope=truth_in_one_supplied_finite_structure`, not a general-validity field. It includes the evaluated outer quantifier cases and one outer witness or counterexample where applicable. It does not return a full theorem proof.

The domain has 1-8 members. Different constants may co-refer. Predicate extensions may be empty. All extensions are complete in this supplied structure: omitted tuples are false there. Declare arity, preserve tuple order and do not encode missing real-world evidence as false merely to fill a model.

Other limits are 64 constants, 64 predicates, arity at most four, 4,096 extension tuples, 512 AST nodes, depth 32 and 100,000 expanded evaluation steps. Full validation and cost calculation occur before evaluation. Both branches and all quantifier assignments contribute to cost, so an apparently unused branch cannot evade the bound. Duplicate rows, free variables, undeclared symbols and malformed objects are rejected.

## 5. Teaching, correction and retained procedures

Use the loop `attempt -> inspect artifact -> diagnose -> repair -> transfer attempt`. The teacher should identify the particular inference or evidence failure. Learners must produce a new artifact after feedback, not only repeat the correction label. A transfer task must vary more than surface names when testing generalisation across problem families.

Record each attempt, feedback source, available tools and procedure version. A saved lesson is usable only when the host loads it. Distinguish a change to context, a stored instruction and model-parameter training. No parameter training occurs in this package.

The requested artifacts are external justifications and observable actions. Private internal deliberation is not required. A concise correct countermodel can carry more assessment weight than a long unsupported narrative.

## 6. Completion protocol

The required development sequence is eight units, forty corrected practice items, eight laboratory artifacts and four reviewed capstones. A teacher records which errors persist and what remains unverified. A local score is a practice result.

Independent assessment begins only after curriculum freeze, separate examination creation, protected delivery and an approved learner runtime. The examination author and learner must not receive each other's protected material. A disclosed test used for improvement becomes development data. The [assessment protocol](assessment.md) supplies a proposed comparison design and reporting requirements for future studies.

No curriculum packet, public score, self-declared model identity or signed key possession alone proves that an autonomous model completed the work. The admission record must describe the actual assurance obtained from the controlled execution environment.
