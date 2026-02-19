from dataclasses import dataclass

from tests.fakes.FakeFileSystem import FakeFileSystem
from tests.fakes.FakeRadarrAPIAdapter import FakeRadarrAPIAdapter
from tests.fakes.FakeJellyfinAPIAdapter import FakeJellyfinAPIAdapter

from application import (
    ProcessAssemblerRegistry,
    OutcomeHandlerRegistry,
    EventPublisher,
    ProcessManager,
    ProcessRunner,
    TaskScheduler,
)

@dataclass
class TestSystem:
    filesystem: FakeFileSystem
    radarr: FakeRadarrAPIAdapter
    jellyfin: FakeJellyfinAPIAdapter
    assembler_registry: ProcessAssemblerRegistry
    outcome_registry: OutcomeHandlerRegistry
    runner: ProcessRunner
    manager: ProcessManager
    publisher: EventPublisher
    scheduler: TaskScheduler