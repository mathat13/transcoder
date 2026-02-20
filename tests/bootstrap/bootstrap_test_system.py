from tests.bootstrap.TestSystem import TestSystem
from tests.fakes.FakeFileSystem import FakeFileSystem
from tests.fakes.FakeRadarrAPIAdapter import FakeRadarrAPIAdapter
from tests.fakes.FakeJellyfinAPIAdapter import FakeJellyfinAPIAdapter
from tests.fakes.FakeProcessRunner import FakeProcessRunner
from tests.fakes.FakeSyncEventBus import FakeSyncEventBus

from domain import (
    JobCompleted,

)
from application import (
    JobCompletionProcessAssembler,
    ProcessAssemblerRegistry,
    JobCompletionOutcomeHandler,
    OutcomeHandlerRegistry,
    EventPublisher,
    ProcessManager,
    TaskScheduler,
    ProcessRunner,
    ProcessRunnerResult,
)

def bootstrap_test_system(
    *,
    runner: ProcessRunner | None = None,
) -> TestSystem:
    # --- infrastructure fakes ---
    filesystem = FakeFileSystem()
    radarr = FakeRadarrAPIAdapter()
    jellyfin = FakeJellyfinAPIAdapter()

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
    runner = runner or FakeProcessRunner(result=ProcessRunnerResult.success())

    # --- side effects ---
    publisher = EventPublisher(event_bus=FakeSyncEventBus())
    scheduler = TaskScheduler()

    # --- orchestration ---
    manager = ProcessManager(
        runner=runner,
        publisher=publisher,
        scheduler=scheduler,
        assemblers=assembler_registry,
        outcomes=outcome_registry,
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