# FlowLab report

## Coverage

- Events: **17**
- Sessions: **3**
- Resolved blockers: **2**
- Verification events: **3**

## Orientation

- Measurable sessions: **3**
- Median fraction: **16.7%**
- p75 fraction: **16.7%**
- p90 fraction: **16.7%**
- Median absolute time: **5.0 min**
- Gate signal: **UNMEASURABLE** — only 3 measurable sessions; gate requires 10

## Blockers by class

| Class | n | Median | p90 | CV | p90/median | Variance gate |
|---|---:|---:|---:|---:|---:|---|
| design | 1 | 20.0 min | 20.0 min | 0.00 | 1.00 | no |
| human | 1 | 20.0 min | 20.0 min | 0.00 | 1.00 | no |

## Control split

- Endogenous blocked time: **20.0 min**
- Exogenous blocked time: **20.0 min**
- Unknown blocked time: **0.0 s**
- Exogenous share of classified time: **50.0%**
- Gate signal: **ADDRESSABLE_CANDIDATE**

## Oracle observations

| Kind | Strength | Result | Count |
|---|---|---|---:|
| bounded | medium | fail | 1 |
| human | medium | pass | 1 |
| mechanical | strong | pass | 1 |

## Data quality

- Events missing session ID: **0**
- Blocker events missing blocker ID: **0**
- Orphan blocker resolutions: **0**
- Unresolved open blockers: **0**
- Truncated sessions: **0**

## Interpretation boundary

Gate signals are not final decisions. Competitive duplication still requires a suitable oracle and bounded discard/reconciliation cost. Missing blocker events are reported as missing data rather than inferred from silence.
