# Campaign overview

The campaign is deliberately sequential at decision points and parallel only inside mechanically graded workfronts.

## WF-0 — Ground truth

Profile actual `auditctl` NDJSON and inspect event producers/consumers.

Outputs:

- source manifest with hashes and time range;
- field/event profile;
- first-pass mapping;
- explicit list of metrics that are directly measurable, inferable, or absent.

Gate: a sanitized fixture normalizes deterministically and every canonical event is tied to an observed source shape.

## WF-1 — Metric kernel

Adapt and harden the included parser and metric implementation against the real schema.

Parallel support is useful for:

- independent fixture construction;
- timestamp/pathological-event cases;
- property and mutation tests;
- checking semantic assumptions against event producers.

Gate: tests pass; two independent reproductions agree; metric definitions are documented.

## WF-2 — Baseline

Run the four measurements against real data. Produce aggregate distributions and data-quality findings.

Gate: report is reproducible and no conclusion depends on an undocumented inference.

## WF-3 — One real case study

Select a blocker class using evidence, not preference:

- enough observations to reconstruct;
- strong or bounded oracle;
- low blast radius;
- plausible flow impact.

Compare the recorded path with one or more counterfactual allocations. Do not manufacture probabilities. Use observed durations, explicit assumptions, and falsifiable evidence.

Gate: case study states whether breadth would plausibly reduce **time-to-verified-complete**, not merely time-to-first-output.

## WF-4 — Challenger and reducer

Attack every proposed conclusion:

- orientation may be misidentified;
- blocker classes may mix unlike events;
- missing events may masquerade as zero waiting;
- duplicate attempts may move cost into integration/review;
- oracle labels may overstate what the checks prove.

Reducer assigns ADOPT/PILOT/REJECT/UNMEASURABLE to each proposal and writes the ADR.

## WF-5 — Remaining-quota work

Only after the required outcome exists. Follow `orchestrator/QUOTA_SINK.md` in order. Prefer deeper falsification and a second mechanically graded case over new features.
