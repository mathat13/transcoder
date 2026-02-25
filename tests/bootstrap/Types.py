from dataclasses import dataclass

from tests.fakes.FakeFileSystem import FakeFileSystem
from tests.fakes.FakeRadarrAPIAdapter import FakeRadarrAPIAdapter
from tests.fakes.FakeJellyfinAPIAdapter import FakeJellyfinAPIAdapter
from tests.fakes.FakeSyncEventBus import FakeSyncEventBus
from tests.fakes.FakeJobRepository import FakeJobRepository

from application import (
    ProcessAssemblerRegistry,
    OutcomeHandlerRegistry,
    EventPublisher,
    ProcessManager,
    JobService,
    ProcessRunner,
    TaskScheduler,
)

@dataclass(frozen=True)
class ApplicationTestSystem:
    filesystem: FakeFileSystem
    radarr: FakeRadarrAPIAdapter
    jellyfin: FakeJellyfinAPIAdapter
    job_repo: FakeJobRepository
    assembler_registry: ProcessAssemblerRegistry
    outcome_registry: OutcomeHandlerRegistry
    runner: ProcessRunner
    manager: ProcessManager
    job_service: JobService
    event_bus: FakeSyncEventBus
    publisher: EventPublisher
    scheduler: TaskScheduler

@dataclass(frozen=True)
class WorkflowTestSystem:
    filesystem: FakeFileSystem
    radarr: FakeRadarrAPIAdapter
    jellyfin: FakeJellyfinAPIAdapter
    assembler_registry: ProcessAssemblerRegistry
    outcome_registry: OutcomeHandlerRegistry
    runner: ProcessRunner
    manager: ProcessManager
    event_bus: FakeSyncEventBus
    publisher: EventPublisher
    scheduler: TaskScheduler

@dataclass(frozen=True)
class JobServiceTestSystem:
    job_repo: FakeJobRepository
    job_service: JobService
    event_bus: FakeSyncEventBus
    publisher: EventPublisher
