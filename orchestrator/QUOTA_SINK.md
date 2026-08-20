# Ordered remaining-quota work

Use only after the required baseline, case study, challenger pass, and first reducer outcome exist.

1. **Adversarial data-quality pass** — search for producer-version drift, clock skew, duplicate IDs, missing end events, reopened blockers, and classification leakage.
2. **Mutation/property testing** — corrupt timestamps, reorder events, duplicate records, truncate streams, and verify explicit failure/data-quality reporting.
3. **Second blocker class** — only if it has a strong or bounded oracle and adds a materially different variance/control profile.
4. **Independent reproduction** — a fresh session rebuilds the report from the handoff without conversational context.
5. **Performance and scale** — streaming ingestion, memory bounds, and large-file benchmark; keep implementation simple unless real logs require more.
6. **Exporter spike** — emit Prometheus/OpenMetrics or a homelab-analytics-friendly table from the stable report model. Do not deploy it.
7. **Cross-project protocol pilot** — apply `oracle:` plus the perpendicular-human escalation rule to one real, low-blast-radius work item selected from the backlog.
8. **Publication artifact** — draft a kotona.app follow-up using actual measurements, including rejected hypotheses. Never publish private paths or raw evidence.

Do not start a dashboard, generalized orchestration product, or multi-tenant service merely to consume quota. That is how one turns temporary abundance into permanent maintenance.
