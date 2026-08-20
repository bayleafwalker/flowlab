# Case study: bounded local inference with an independent oracle

## Intent

A frontier coordinator delegated a real, bounded manifest-verifier repair to
the local `worker-fast` profile, then independently inspected and refined the
result. The intended test was ordinary workflow use—not a synthetic model
benchmark—and the candidate had no authority to commit, push, mutate sprint
state, or touch a cluster.

## Observed outcome

- One worker attempt completed in 26.235 seconds.
- The first completed edit occurred 11.572 seconds after session start, an
  orientation fraction of 44.1% for this session.
- The coordinator removed one redundant predicate, accepted the result, and
  recorded 12 passing tests, a positive 26-file manifest gate, and a negative
  gate that rejected `unexpected-payload.txt` by name.
- Seven tool calls were permission-denied. The source receipt records their
  count but no explicit blocker-open/resolved lifecycle, so FlowLab does not
  invent blocker duration from them.
- The route remains `experimental_unqualified`: same-identity workstation
  containment does not prove the named formal AgentOps hybrid route.

Acceptance Lab independently scores the bounded outcome **PASS** at campaign
commit `f49ef53`. That pass includes the qualification limitation as a required,
cited fact; it is not a route-qualification verdict.

## Challenger case

The takeover package at commit `4412ca1` shows why the oracle matters. An
independent review found that the first Worker-B proof had physically exposed
later events, overriding the stale G1 pass claim. The sanitized flow therefore
records a strong independent-review failure and an unresolved verification
blocker. Acceptance Lab's second **PASS** means only that its read-only reducer
reports G1 unproven, G7/G8 pending, and the final verdict withheld.

## Recommendation

**NARROW** local inference to bounded repository tasks with explicit mechanical
oracles and frontier review. Do not use this two-session reconstruction to set
capacity policy, claim formal route qualification, or bypass independent
review. Emit native session/edit/blocker/verification events before attempting
a larger flow experiment.
