# ADR-0002: Presentation Layer Response Handling Strategy

## Status
In-Progress

## Context

Adapter layer must co-ordinate conversion of presentation outcomes into framework responses.  Currently, ingress and egress presenters use different mechanisms for performing this functionality:

- Ingress presenters return defined presentation objects per outcome to adapter layer for conversion to framework response
- Egress presenters integrate with framwork exception-based flow control mechanisms for performing presentation outcome to framework response mapping

 We must decide between:

- Presenters returning presentation objects for adapter layer to convert to transport response explicitly
- Presenters integrating with framework using exception-based control flow to perform same functionality

## Decision

Presentation outcomes will be modelled as presentation objects containing transport intent (things like status code, data payload).  Presenters will return presentation objects directly to route, route will perform final conversion from presentation object to framework object.

## Consequences

### Positive

- Keeps translation layer clean of framework, allowing adaptation across transport protocols to be simpler
- Centralizes adapter layer request handling into adapter, simplifying architecture conceptually
- Collapses application success and application failure result lifecycles into one
- Makes presentation responsibilities explicit by modelling HTTP intent as data rather than control flow

### Negative

- Requires custom presentation code to return a valid response to framework
- Routes take more boilerplate code
- Bypassing response_model validation removes automatic framework-level egress validation.
Equivalent guarantees must be enforced within presentation code.

## Alternatives Considered

Presenters integrating with framework using exception-based control

Pros:
- Allows for easier implementation through defined pathways
- Routes stay thin

Cons:
- Translation layer becomes framework aware, reducing translation layer portability across transport protocols
- More overhead required in understanding request lifecycle
