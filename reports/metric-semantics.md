# Metric semantics and source mapping

## Source revisions inspected

- Repository commit: `5e002ab` (`v0.1.0`)
- Producer schema versions: unavailable; this grounding pass uses only the bundled sanitized fixture
- Input: `tests/fixtures/sample-auditctl.ndjson`, 17 records, hash recorded in `evidence/input-manifest.json`
- Input time range: 2026-08-01T10:00:00Z through 2026-08-03T12:10:00Z

The original fixture grounding remains the adapter-shape baseline. The real
workflow campaign is a second, sanitized reconstruction at FlowLab commit
`c475e37`: eight records derived from the local-inference receipt and takeover
commit `4412ca1`. Its source and transformation limits are recorded in
`evidence/campaign-2026-08-20/provenance.json`. It is Auditctl-shaped input, not
evidence that the source systems emitted native Auditctl events.

## Canonical event mapping

| Canonical event | Sanitized source shape | Confidence | Known gaps |
|---|---|---|---|
| `session.started` | `type: session.started` | high for fixture | actual producer variants not inspected |
| `session.ended` | `type: session.ended` | high for fixture | actual producer variants not inspected |
| `edit.meaningful` | `type: file.edited` or `patch.applied` | high for fixture | proxy requires producer confirmation |
| `blocker.opened` | `type: blocker.opened` with `blocker_id`, class, control | high for fixture | no reopened/duplicate-ID case |
| `blocker.resolved` | `type: blocker.resolved` with `blocker_id` | high for fixture | pairing is only tested for unique IDs |
| `verification.finished` | `type: verification.finished` with `oracle` | high for fixture | no acceptance/completion relation |

## Interpretation decisions

The fixture has explicit session start/end and meaningful-edit events, so its
orientation fractions use those boundaries and the first edit event. Blocker
duration uses only explicit open/resolve pairs; waiting is never inferred from
silence. The endogenous/exogenous split uses the declared `control` field.
Oracle kind, strength, and result are counted as declared; passing a check does
not promote its strength.

## Unmeasurable concepts

- Actual live `auditctl` producer compatibility: **UNMEASURABLE** from the
  sanitized fixture alone; no live or confidential stream was read.
- Time-to-verified-complete: **UNMEASURABLE**; the fixture has verification
  events but no `work.completed` or equivalent acceptance event.
- Oracle coverage at completion: **UNMEASURABLE** for the same reason.
- Context-warming decision: **UNMEASURABLE**; only 3 measurable sessions are
  present and the pre-registered gate requires 10.
- Competitive duplication: no class reaches the minimum 8 resolved blockers;
  variance and recurring-class conclusions are therefore unavailable.
- Exogenous speculation as a final decision: the fixture shows 50% of
  classified blocked time as exogenous, but only one exogenous instance exists;
  recurring safely-workable-class evidence is unavailable.

The available `time_to_first_verified_seconds` value is a supporting diagnostic,
not a substitute for time-to-verified-complete.

## Campaign result

The campaign baseline has two measurable sessions, no resolved blockers, one
unresolved verification blocker, one truncated session, one strong mechanical
pass, and one strong independent-review failure. Its 24.4% median orientation
fraction is not an adoption signal because the preregistered minimum is ten
sessions. The endogenous/exogenous split, competitive-duplication variance,
and exogenous-speculation share remain unmeasurable.
