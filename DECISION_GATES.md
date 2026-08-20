# Initial decision gates

These are pre-registered starting thresholds, not universal truths. Revise them only before viewing the target result, or record the change and rationale in `config/gates.actual.json`.

## Context warming

- **ADOPT candidate:** at least 10 measurable sessions and either median orientation fraction ≥ 0.15 or p75 ≥ 0.25, with a demonstrably reusable context artifact.
- **REJECT candidate:** median < 0.10 and p75 < 0.15, unless absolute orientation time is operationally material.
- Otherwise: **PILOT**.

## Competitive duplicate search

A blocker class is eligible only when all apply:

- at least 8 resolved instances;
- coefficient of variation ≥ 0.75;
- p90 / median ≥ 2.0;
- mechanical or bounded oracle;
- discarded attempts do not create significant integration/review work.

Without an oracle, variance is not enough.

## Exogenous speculation

- **Addressable:** exogenous waits are at least 20% of classified blocked time and at least one recurring class can be worked ahead safely.
- **Low addressable market:** below 10%.
- Between them: pilot only.

Speculation against endogenous design latency is rejected by default: decide or reduce the decision instead.

## `oracle:` declaration

- **ADOPT:** work items already depend on heterogeneous verification and the declaration can be introduced without duplicating an existing authoritative field.
- **PILOT:** useful but event producers cannot yet emit it consistently.
- **REJECT:** another canonical schema already captures the same semantics.
