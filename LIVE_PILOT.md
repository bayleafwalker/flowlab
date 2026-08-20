# Live pilot protocol

A live pilot is required when historical logs cannot support a defensible case reconstruction, and optional otherwise.

## Select the work item

Choose one real work item that has:

- a strong or bounded machine oracle;
- a clear reversible sandbox/worktree;
- a likely blocker or search-heavy phase;
- no need for repeated human taste judgments;
- useful product value even if the workflow hypothesis fails.

Prefer migration dry-runs, bisection, reproducer construction, flaky-test isolation, candidate patch search, deterministic renderer checks, or evidence extraction. Avoid architecture forks whose only oracle is “which design do you like?”

## Staffing

```text
one authoritative owner
    ├── excavator/reproducer
    ├── candidate-search worker(s), only behind the oracle
    ├── challenger
    └── integrator/verifier
```

The human does not dispatch, relay context, or approve routine transitions. Ask upward only when a semantic or authority boundary from `END_STATE.md` is crossed.

## Instrumentation

Record at least:

- session/workfront start and end;
- first meaningful edit;
- blocker opened/resolved with class and control;
- verification start/finish, oracle kind/strength/result;
- handoff and invalidation events;
- human escalation with reason category.

Use canonical `auditctl` events where available. When they are absent, write a separate disposable normalized NDJSON stream rather than changing production instrumentation mid-pilot.

## Comparison

The counterfactual is not “ten agents would obviously be faster.” State:

- what the owner would have done alone;
- what support/breadth work was added;
- which added work changed the verified completion time;
- selection, review, integration, and discarded-work cost;
- whether any human interaction supplied semantic information or merely repaired the control plane.

## Pass condition

The pilot passes only when it yields a verified product result **and** enough evidence to say whether the extra allocation reduced time-to-verified-complete. More output is not a pass condition.
