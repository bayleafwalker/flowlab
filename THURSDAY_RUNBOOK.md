# Thursday quota runbook

The reset is on **Thursday, 20 August 2026**. Use the whole available allowance on one campaign, but do not spend the last useful capacity before integration and reduction are safe.

## Quota allocation by function

These are proportions of whatever allowance is available, not assumptions about a particular product limit.

| Share | Function | Typical sessions |
|---:|---|---|
| 10% | Grounding | repository/event excavation, source manifest, mapping hypotheses |
| 25% | Metric kernel | implementation, fixtures, property tests, semantic checks |
| 20% | Baseline and case reconstruction | aggregate run, one real blocker class, counterfactual timeline |
| 20% | Adversarial work | independent challengers, missing-event search, review-cost accounting |
| 15% | Integration and reducer reserve | reproduction, ADR, final evidence packet |
| 10% | Ordered quota sink | second case, mutation tests, exporter spike, publication artifact |

The proportions may move as gates resolve, but **never consume the reducer reserve on new feature work**.

## Session topology

Use one durable coordinator and one authoritative integration/design owner. Other sessions attach to the active workfront:

```text
                          COORDINATOR
                               │
                    authoritative workfront
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
      excavators          implementers         challengers
          │                    │                    │
          └────────────────────┴────────────────────┘
                               │
                            reducer
```

Do not launch several independent coordinators. That maximizes meetings between robots, a known growth industry with limited customer demand.

## Burn rule

Before the required outcome is secured, spend capacity only on the current gate. After `reports/final-outcome.md` and the ADR exist in draft, burn remaining quota down the ordered list in `orchestrator/QUOTA_SINK.md`.

The last session should be an **independent reproducer/reviewer**, not another implementer. Its job is to consume the package cold and either reproduce the result or identify the missing handoff state.

## Preferred live pilot selection

Do not preselect a favorite project. Derive a candidate from the logs using these filters:

1. recurring blocker class;
2. strong or bounded machine oracle;
3. low deployment blast radius;
4. no major qualitative review burden;
5. useful result even if the broader theory is rejected.

Good shapes include bisection, migration dry-runs, minimal reproducers, flaky-test isolation, generated candidate patches behind a strong suite, and deterministic evidence extraction. Avoid eight-agent architecture beauty contests.
