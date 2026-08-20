# Bounded worker roles

## Excavator

Read event producers, schemas, examples, and local logs. Return observed shapes, source references, and contradictions. Do not design the final metric model.

## Implementer

Implement one bounded component against the authoritative mapping and tests. Do not reinterpret metric semantics silently.

## Fixture builder

Create sanitized fixtures that preserve structural edge cases without exposing raw log content. Every fixture states which observed case it represents.

## Challenger

Try to falsify a specific conclusion with concrete evidence: missing events, mismatched timestamps, mixed blocker classes, false oracle strength, or shifted integration cost.

## Case reconstructor

Build an evidence-backed timeline for one blocker class. Separate recorded facts, inferred facts, and counterfactual assumptions.

## Reducer

Read all evidence and assign ADOPT/PILOT/REJECT/UNMEASURABLE. It may not manufacture a compromise conclusion to preserve prior work.
