# Orchestrator handoff — FlowLab campaign

Date: **Thursday, 20 August 2026**

## Mission

Use the available frontier-model capacity to produce a defensible answer to one question:

> Where does additional agent capacity reduce time-to-verified-complete in the user's actual workflows, and where does it only create more reviewable output?

Do not optimize agent utilisation. Keep work-in-progress bounded and saturate the currently constraining workfront.

## Authoritative end state

Read `END_STATE.md` and `campaign.json` before dispatching work. The campaign is complete only when all required postconditions are evidenced.

## Operating rules

1. **Ground before building.** Profile the actual `auditctl` NDJSON and inspect the relevant repositories before modifying the adapter or metric definitions.
2. **One design authority.** Use one strong owner for metric semantics and integration. Parallel sessions may excavate, test, challenge, or implement bounded components; they must not independently invent competing metric systems.
3. **Swarm only where graded.** Use broad parallelism for schema discovery, fixture generation, property tests, adversarial cases, mutation testing, benchmarks, and reproducibility checks. Use a single strong owner for ambiguous semantics.
4. **Human escalation is semantic only.** Do not ask the user to route tasks, choose workers, repeat known context, or approve ordinary transitions. Escalate only when:
   - two materially different outcomes remain and the declared end state cannot distinguish them;
   - a permission or irreversible action exceeds the package mandate;
   - logs appear to contain secrets or employer/customer-confidential data that cannot be safely processed locally;
   - a qualitative judgment has no declared oracle.
5. **Raw evidence stays local.** Never commit source NDJSON. Commit only bounded profiles, sanitized fixtures, aggregate reports, mappings, and referenced hashes.
6. **No production integration by momentum.** The final reducer may recommend integration, but implementation into Vuoro/auditctl/sprintctl requires an explicit ADR and must remain a separately reversible commit.
7. **Consume quota by increasing confidence, not WIP.** Once the core report works, use remaining capacity from `orchestrator/QUOTA_SINK.md` in order.

## Required artifacts

Produce these paths:

```text
config/auditctl-map.json
evidence/auditctl-profile.json
evidence/input-manifest.json
reports/baseline/report.json
reports/baseline/report.md
reports/case-study/report.md
decisions/ADR-0001-flow-capacity.md
reports/final-outcome.md
```

Create `config/gates.actual.json` only when the pre-registered defaults are revised; record the rationale before inspecting the target result.

The final outcome must state, with evidence:

- whether context warming has enough addressable time to justify implementation;
- which blocker classes, if any, have enough variance for competitive duplication;
- the observed endogenous/exogenous blocked-time split;
- where machine oracles are strong enough to permit breadth;
- which hypothesis was rejected;
- the next single production change, or an explicit decision to build nothing.

## Historical-data fallback

If the logs lack explicit blocker or orientation events, mark the affected metric **UNMEASURABLE** and run the bounded protocol in `LIVE_PILOT.md`. Do not infer waiting from gaps or retrofit a favorable history. The fallback must still produce a real verified project result.

## Workfront protocol

Follow `campaign.json`. Recompute the ready frontier after every gate. Maintain at most **two active workfronts**, except that support/challenger agents may attach to an active workfront without creating a new one.

Preferred allocation:

```text
strong frontier model: metric semantics, reducer, architecture decision
parallel frontier sessions: excavation, tests, challengers, case reconstruction
cheap/local models later: repeatable classification, log triage, bulk fixture mining
```

## Completion command

Before declaring success:

```bash
./scripts/verify.sh
GATES=config/gates.default.json
[ -f config/gates.actual.json ] && GATES=config/gates.actual.json
PYTHONPATH=src python -m flowlab run <sanitized-or-local-log-path> \
  --mapping config/auditctl-map.json \
  --gates "$GATES" \
  --out-dir reports/reproduction

diff -u reports/baseline/report.json reports/reproduction/report.json
```

If input timestamps or source hashes make byte-identical reports inappropriate, normalize only those declared volatile fields and document why.

## Final reducer outcomes

Each proposal must end as exactly one of:

- **ADOPT** — measured benefit and bounded implementation path;
- **PILOT** — plausible signal, insufficient sample;
- **REJECT** — evidence below the decision gate;
- **UNMEASURABLE** — missing instrumentation, with the minimum event addition required.

Do not end with “more research needed” without naming which of those four states applies.
