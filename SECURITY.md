# Evidence handling

`auditctl` streams may contain command output, paths, prompts, endpoints, identifiers, or secrets. Treat raw NDJSON as private operational evidence.

## Rules

- Keep raw logs outside the repository or under ignored `evidence/raw/`.
- The default `flowlab discover` output records field names, coverage, and types but **does not include raw sample values**.
- `flowlab discover --include-samples` is for local mapping work only. Write it under `evidence/raw/` and do not commit it.
- Build sanitized fixtures manually from structural cases. Replace tokens, addresses, paths, customer/employer names, and unique identifiers.
- Aggregate reports may be committed only after checking that blocker class labels and work IDs do not expose confidential project details.
- Store an input hash and record count rather than copying source records into the evidence packet.

## Lightweight classification before sharing

Review generated artifacts for:

1. credentials, API keys, cookies, bearer tokens, private keys;
2. customer or employer-confidential data;
3. reachable endpoints or operational weaknesses;
4. personal identifiers;
5. unnecessary internal paths, hostnames, repository names, or session text.

A source hash, event count, duration distribution, or generic blocker label is normally low consequence. Raw tool output is not.
