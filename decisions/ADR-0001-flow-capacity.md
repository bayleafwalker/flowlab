# ADR-0001: retain the evaluators; defer capacity interventions

- Status: Accepted for the lab; no production mutation authorized
- Date: 2026-08-20
- Evidence baseline: FlowLab commit `c475e37`
- Acceptance campaign: Acceptance Lab commit `f49ef53`

## Context

The campaign has two inspected workflows and eight sanitized, Auditctl-shaped
events. They provide a real local-inference success and a real independent
review failure, but no resolved blocker interval and only two measurable
orientation sessions. One session is truncated with an unresolved blocker.
The event stream is a deterministic reconstruction from receipts and Git
evidence, not a claim that either producer emitted native Auditctl events.

## Decision

1. Keep Acceptance Lab as the owner of scenario-specific, trace-grounded
   candidate scoring. Keep FlowLab as the owner of aggregate flow metrics.
   Neither adopts the other's schema.
2. **NARROW** local `worker-fast` use to bounded repository changes with strong
   mechanical gates and frontier coordinator review. The observed run is useful
   experimental evidence, not formal route qualification.
3. Mark context warming, competitive duplicate search, and exogenous
   speculation **UNMEASURABLE** for this campaign. Build none of them from this
   sample.
4. **PILOT** an `oracle` declaration only after checking Sprintctl's current
   authoritative fields. Flow event emission belongs with Auditctl producers;
   work-intent metadata, if non-duplicative, belongs with Sprintctl. No shared
   contract is extracted to Vuoro until a second real consumer exists.
5. The next single change is instrumentation, not more workers: emit explicit
   session start/end, meaningful-edit, blocker open/resolve, verification
   result, and oracle kind/strength fields. This ADR recommends that change; it
   does not authorize or implement production integration.

## Alternatives rejected

- **Adopt context warming now:** rejected because 2 sessions are below the
  preregistered minimum of 10 despite a high observed median.
- **Duplicate blocker search now:** rejected because there are 0 resolved
  blockers, versus the per-class minimum of 8.
- **Speculate across external waits now:** rejected because classified resolved
  blocked time is absent; silence is not waiting-time evidence.
- **Merge evaluation schemas into Vuoro:** rejected because ownership remains
  distinct and the two-consumer extraction threshold is not met.

## Consequences

The lab artifacts remain useful and removable. No appservice, cluster,
deployment, queue, or production orchestrator was mutated. A future campaign
can rerun the same gates once native events provide the missing denominator.
