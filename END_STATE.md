# Discriminating end state — revision 1

## Observable postconditions

- A single command converts local `auditctl` NDJSON into a deterministic aggregate report.
- The report includes orientation fraction, blocker distributions, endogenous/exogenous blocked time, and oracle coverage.
- Every metric names its event assumptions and data-quality limitations.
- At least one real blocker class is reconstructed far enough to test whether added breadth would have shortened time-to-verified-complete.
- The final reducer produces explicit ADOPT/PILOT/REJECT/UNMEASURABLE outcomes for warming, duplicate search, exogenous speculation, and work-item oracle declarations.
- A future session can reproduce the results from the mapping, source manifest, commands, and local input without reading this conversation.

## Invariants

- Source logs are read-only.
- Raw logs, prompts, secrets, tokens, internal endpoints, and unnecessary private metadata are not committed.
- Aggregate results remain traceable to source hashes and declared mappings.
- Metric semantics are not silently changed to improve the result.
- A production integration is not smuggled into the experiment.
- The package remains removable without migration or rollback work.

## Reversibility budget

The experiment may create a new local repository and sanitized reports. It may not mutate live databases, deployed services, canonical event schemas, or production workflows.

Rollback is deletion of the repository and any disposable worktrees.

## Explicit don't-cares

- Dashboard technology.
- Whether the eventual production exporter uses Prometheus, Loki, SQL, or static reports.
- Final CLI naming.
- Visual styling beyond readable evidence.
- General-purpose support for event formats other than the user's actual `auditctl` stream.

## Questions that justify human escalation

- A remaining branch changes a business- or user-visible meaning not described here.
- Processing the available logs would expose material secrets or employer/customer-confidential data.
- A proposed live pilot would cross an authority or irreversibility boundary.
- Two qualitative outcomes cannot be distinguished mechanically and selecting one affects the final recommendation.

Everything else is control-plane work and belongs to the orchestrator.
