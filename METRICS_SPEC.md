# Measurement specification

## 1. Orientation fraction

For a session with a known start, end, and first meaningful edit:

```text
orientation_fraction = (first_meaningful_edit - session_start)
                       / (session_end - session_start)
```

A meaningful edit must be mapped from actual events. Reading, searching, planning, and tool setup do not count. A commit may be too late to serve as the proxy if patch/write events exist.

Report count, median, p75, p90, mean, and missingness. Also report absolute orientation seconds. A low fraction can still matter for very long sessions, so do not use the percentage alone.

## 2. Blocker variance

Pair explicit blocker-open and blocker-resolve events. Report duration distributions by blocker class and control type.

Competitive duplication is not justified by high mean alone. Look for:

- adequate sample size;
- high coefficient of variation;
- a long p90/median ratio;
- a strong/cheap oracle;
- low merge, selection, and reconciliation cost.

If blocker events are not explicit, classify the metric as UNMEASURABLE rather than inferring waiting from silence.

## 3. Endogenous/exogenous split

Blocked duration is:

- **endogenous** when the workflow owns the decision or work: design, implementation, integration, test repair, environment repair;
- **exogenous** when it waits on an external authority or clock: human response, vendor, compliance/legal decision, external service, rate-limit reset, long-running independent job.

Do not classify “waiting on another agent” as exogenous.

Report total duration and share by control type, plus unknown/unclassified time.

## 4. Oracle strength

An oracle declaration describes what grades a work item and how much confidence it provides. Record at least:

- kind: mechanical, bounded, human, none;
- strength: strong, medium, weak;
- latency;
- result;
- evidence location.

Passing tests are not automatically a strong oracle. Strength describes the relationship between the check and the desired outcome, not the reliability of the test runner.

## Primary outcome

All recommendations must target **time-to-verified-complete**. Time-to-first-output, number of sessions, patches produced, and agent utilisation are supporting diagnostics only.
