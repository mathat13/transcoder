# ADR-0001: Translation Layer Ownership Inside Presentation Boundary

## Status
Accepted

## Context
We need to translate external RequestDTO objects into internal Command/Query objects
and map application results into ResponseDTOs.

There is ambiguity whether translation should be:
- part of the application layer
- part of a shared translation service inside the presentation layer
- part of the adapter layer inside the presentation layer

## Decision
We will keep translation logic inside the Presentation Layer, as part of the Adapter Layer.

It will be composed of:
- Ingress Translation
- Egress Translation
But not strictly.

## Consequences

### Positive
- Keeps application layer free of transport concerns
- Allows multiple external clients to reuse same application API
- Localizes HTTP/DTO mapping logic

### Negative
- Increases complexity of presentation layer
- Requires duplication if other adapters emerge (e.g. MQ, CLI)

## Alternatives Considered
- Shared global translation service (rejected due to coupling), possible future evolution for other clients using same transport language.
- Application-owned translation (rejected due to transport leakage).