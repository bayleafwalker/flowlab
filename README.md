# FlowLab — Thursday 20 August 2026 campaign

A bounded experiment for turning the recent **flow over utilisation**, **oracle-aware swarming**, and **human-perpendicular-to-the-loop** ideas into evidence.

This is deliberately **not another production coordinator**. It is a disposable lab that reads existing `auditctl` NDJSON, measures where agent workflow time is actually going, runs one evidence-backed pilot, and ends with adopt/kill decisions.

## Thursday outcome

By the end of the campaign, the repository should contain:

1. A verified adapter for the actual `auditctl` event shape.
2. A reproducible baseline report covering:
   - orientation fraction;
   - blocker duration and variance by class;
   - endogenous versus exogenous blocked time;
   - oracle coverage and strength at completion.
3. One retrospective or live case study on a real blocker class.
4. Explicit decisions on:
   - warm/prefetched contexts;
   - competitive duplicate search;
   - speculation against exogenous waits;
   - adding `oracle:` metadata to work items;
   - whether any part belongs in Vuoro, `auditctl`, `sprintctl`, or nowhere.
5. A final evidence packet that another session can inspect without reconstructing the campaign.

The campaign itself is also a trial of the perpendicular-human model: the orchestrator owns routing, handoffs, validation, and reduction. Human escalation is reserved for missing semantic authority, not ordinary task management.

## Quick verification

```bash
./scripts/verify.sh
```

Run the included example:

```bash
./scripts/run-sample.sh
cat reports/sample/report.md
```

Run against real logs after producing a mapping:

```bash
PYTHONPATH=src python -m flowlab discover /path/to/audit.ndjson \
  --output evidence/auditctl-profile.json

# Adapt config/auditctl-map.example.json from the profile.
PYTHONPATH=src python -m flowlab run /path/to/audit.ndjson \
  --mapping config/auditctl-map.json \
  --gates config/gates.default.json \
  --out-dir reports/baseline
```

## Start here on Thursday

Hand [`HANDOFF.md`](HANDOFF.md) to the orchestrator. It is the authoritative campaign brief. The machine-readable workfront graph is [`campaign.json`](campaign.json), and [`THURSDAY_RUNBOOK.md`](THURSDAY_RUNBOOK.md) reserves quota for integration rather than spending it all on parallel beginnings.

## Scope boundary

Inputs are read-only. Raw logs and sample-bearing discovery profiles are never committed. See [`SECURITY.md`](SECURITY.md). No production schema or orchestrator is changed until the final reducer has produced an ADR backed by actual measurements.

Deleting this repository must be a complete rollback.
