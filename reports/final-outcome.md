# FlowLab final outcome — 20 August 2026

## Executive result

The evaluation stack works end to end on sanitized evidence, and the local
worker produced one useful bounded result under frontier review. The campaign
does **not** establish a capacity-policy benefit: only two sessions are
measurable, no blocker is resolved, one session is truncated, and the takeover
verdict remains withheld. The correct outcome is to retain the evaluators,
narrow local inference to oracle-backed tasks, and build no warming,
duplication, or speculation mechanism until native flow events exist.

## Intent versus outcome

| Intent | Observed outcome | Adjudication |
| --- | --- | --- |
| Dogfood local inference in a regular coordinated workflow | One 26.235-second attempt produced an accepted manifest repair after a small coordinator refinement; 12 tests and both manifest gates passed | **NARROW** to bounded, mechanically verifiable work; formal route qualification remains unproven |
| Prove trace-grounded candidate evaluation | Acceptance Lab scored both sanitized cases 1.000/PASS and verified disposable event chains of 11 and 8 events | **ADOPT** the read-only evaluation pattern; neither PASS promotes the takeover experiment or route qualification |
| Measure orientation and time to first verification | 2/2 sessions measurable; median orientation 59.786 seconds and 24.4%; one passing time-to-first-verification observation at 26.235 seconds | **UNMEASURABLE** for policy because the gate requires 10 sessions |
| Find blocker classes suitable for competitive duplication | 0 resolved blockers; 1 unresolved verification blocker | **UNMEASURABLE**; no eligible class |
| Quantify endogenous/exogenous waiting and speculation potential | No resolved blocked duration, so the classified split and exogenous share are absent | **UNMEASURABLE**; do not infer waits from gaps |
| Test heterogeneous oracle evidence | One strong mechanical pass and one strong independent-review fail were preserved | **PILOT** consistent oracle metadata; the failure correctly prevents a false takeover pass |

## Evidence summary

- Sanitized input: 8 records, SHA-256
  `4522d7cb6f741c719a6145234a27adcb46dcce249820932961c3f8b4e4e89d5f`
- Mapping SHA-256:
  `f96be35df5c54e27a7d269e75e560bffb030bcb15884983524c07f89ee923d63`
- FlowLab code and baseline commit: `c475e37`
- Baseline report SHA-256:
  `05560c99bc881518a6ebbdeeecad6e161add4e97041b30d06714fd211d37999e`
- Acceptance Lab campaign commit: `f49ef53`
- Local-inference Acceptance candidate-output SHA-256:
  `3e385d90c533f2a4c3b123fca465bd92fc545b98f48244f5e2d59e95ce661469`
- Takeover-state Acceptance candidate-output SHA-256:
  `ffa84e64b47e235136e4f6fe33137d3429e48d919bfcfcf8a92978f8694ba2f9`
- Normalization errors: 0
- Sessions: 2; resolved blockers: 0; verification events: 2
- Data-quality warnings: 1 unresolved blocker, 1 truncated session

## Decisions

### Context warming

Outcome: **UNMEASURABLE**. The observed median crosses the numerical adopt
threshold, but the two-session sample fails the minimum-10-session gate.

### Competitive duplicate search

Outcome: **UNMEASURABLE**. No blocker class has a resolved duration, much less
the required eight observations and variance evidence.

### Exogenous speculation

Outcome: **UNMEASURABLE**. There is no classified resolved blocked time.

### `oracle:` declaration

Outcome: **PILOT**. Heterogeneous strong oracles were materially useful, but the
source producers do not yet emit the field consistently and Sprintctl must be
checked for an existing authoritative equivalent before adding metadata.

### Ownership

- Acceptance Lab: trace-grounded scenario evaluation and deterministic gates.
- FlowLab: normalized aggregate flow metrics and capacity-policy signals.
- Auditctl producers: native operational event emission.
- Sprintctl: possible work-intent oracle declaration, only if non-duplicative.
- Vuoro: nowhere yet; the two-consumer extraction gate is not met.

## What was falsified

- A high orientation fraction in a tiny sample is not sufficient to adopt
  context warming.
- Tool-permission error counts cannot be converted into blocker duration without
  explicit open/resolved events.
- A candidate's self-declared context boundary is not proof of physical context
  isolation; the takeover G1 claim was correctly rejected.

## Limitations

The source stream is sanitized and deterministically reconstructed from exact
receipts and Git commits. It demonstrates the adapter and reducer path but does
not prove live Auditctl producer compatibility. It excludes prompts, raw model
outputs, raw transcripts, command output, credentials, and private session
material. The takeover package was inspected only at `4412ca1`; its later B2,
fair-control, blind-review, and final-adjudication work is outside this report.

## Reproduction

At FlowLab commit `c475e37`:

```bash
./scripts/verify.sh
./scripts/run-campaign.sh reports/reproduction
diff -u reports/baseline/report.json reports/reproduction/report.json
```

At Acceptance Lab commit `f49ef53`:

```bash
python -m pip install -e ".[dev]"
make validate
PYTHONPATH=src python scripts/run_campaign.py
```

The FlowLab input, normalized stream, profile, and reports are byte-stable. The
Acceptance reports omit wall-clock timestamps and event UUIDs but still exercise
and verify a disposable append-only event store on every run.
