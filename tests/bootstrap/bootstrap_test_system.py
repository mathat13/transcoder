from tests.bootstrap.TestSystem import TestSystem
from tests.fakes.FakeFileSystem import FakeFileSystem
from tests.fakes.FakeRadarrAPIAdapter import FakeRadarrAPIAdapter
from tests.fakes.FakeJellyfinAPIAdapter import FakeJellyfinAPIAdapter

from domain import (
    JobCompleted,

)
from application import (
    ProcessRunner,
    JobCompletionProcessAssembler,
    ProcessAssemblerRegistry,
    JobCompletionOutcomeHandler,
    OutcomeHandlerRegistry,
    EventPublisher,
    ProcessManager,
    TaskScheduler,
)

from infrastructure import SyncEventBus

def bootstrap_test_system(
    *,
    filesystem: FakeFileSystem | None = None,
    radarr: FakeRadarrAPIAdapter | None = None,
    jellyfin: FakeJellyfinAPIAdapter | None = None,
    runner: ProcessRunner | None = None,
) -> TestSystem:
    # --- infrastructure fakes ---
    filesystem = filesystem or FakeFileSystem()
    radarr = radarr or FakeRadarrAPIAdapter()
    jellyfin = jellyfin or FakeJellyfinAPIAdapter()

    # --- assemblers ---
    job_completion_assembler = JobCompletionProcessAssembler(
        filesystem=filesystem,
        radarr=radarr,
        jellyfin=jellyfin,
    )

    assembler_registry = ProcessAssemblerRegistry()
    assembler_registry.register(JobCompleted, job_completion_assembler)

    # --- process outcome contexts ---
    completion_outcome_handler = JobCompletionOutcomeHandler()

    outcome_registry = OutcomeHandlerRegistry()
    outcome_registry.register(JobCompleted, completion_outcome_handler)

    # --- execution ---
    runner = runner or ProcessRunner()

    # --- side effects ---
    publisher = EventPublisher(event_bus=SyncEventBus())
    scheduler = TaskScheduler()

    # --- orchestration ---
    manager = ProcessManager(
        runner=runner,
        publisher=publisher,
        scheduler=scheduler,
        assemblers=assembler_registry,
        outcomes=completion_outcome_handler,
    )

    return TestSystem(
        filesystem=filesystem,
        radarr=radarr,
        jellyfin=jellyfin,
        assembler_registry=assembler_registry,
        outcome_registry=outcome_registry,
        runner=runner,
        manager=manager,
        publisher=publisher,
        scheduler=scheduler,
    )