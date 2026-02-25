from tests.bootstrap.Types import (ApplicationTestSystem,
                                   JobServiceTestSystem,
                                   WorkflowTestSystem,
                                   )
from tests.fakes.FakeFileSystem import FakeFileSystem
from tests.fakes.FakeRadarrAPIAdapter import FakeRadarrAPIAdapter
from tests.fakes.FakeJellyfinAPIAdapter import FakeJellyfinAPIAdapter
from tests.fakes.FakeProcessRunner import FakeProcessRunner
from tests.fakes.FakeSyncEventBus import FakeSyncEventBus
from tests.fakes.FakeJobRepository import FakeJobRepository

from domain import (
    JobCompleted,
    JobMovedToVerifying,
)
from application import (
    JobCompletionProcessAssembler,
    JobVerificationProcessAssembler,
    ProcessAssemblerRegistry,
    JobCompletionOutcomeHandler,
    JobVerificationOutcomeHandler,
    OutcomeHandlerRegistry,
    EventPublisher,
    ProcessManager,
    TaskScheduler,
    ProcessRunner,
    ProcessRunnerResult,
    JobService,
    TranscodeVerified,
)

def bootstrap_application_test_system(
    *,
    runner: ProcessRunner | None = None,
) -> ApplicationTestSystem:
    # --- infrastructure fakes ---
    filesystem = FakeFileSystem()
    radarr = FakeRadarrAPIAdapter()
    jellyfin = FakeJellyfinAPIAdapter()
    job_repo = FakeJobRepository()

    # --- assemblers ---
    job_completion_assembler = JobCompletionProcessAssembler(
        filesystem=filesystem,
        radarr=radarr,
        jellyfin=jellyfin,
    )

    job_verification_assembler = JobVerificationProcessAssembler(
        filesystem=filesystem,
    )

    assembler_registry = ProcessAssemblerRegistry()
    assembler_registry.register(JobMovedToVerifying, job_verification_assembler)
    assembler_registry.register(JobCompleted, job_completion_assembler)

    # --- process outcome contexts ---
    completion_outcome_handler = JobCompletionOutcomeHandler()
    verification_outcome_handler = JobVerificationOutcomeHandler()

    outcome_registry = OutcomeHandlerRegistry()
    outcome_registry.register(JobMovedToVerifying, verification_outcome_handler)
    outcome_registry.register(JobCompleted, completion_outcome_handler)

    # --- execution ---
    runner = runner or FakeProcessRunner(result=ProcessRunnerResult.success())

    # --- side effects ---
    event_bus=FakeSyncEventBus()
    publisher = EventPublisher(event_bus=event_bus)
    scheduler = TaskScheduler()

    # --- orchestration ---
    manager = ProcessManager(
        runner=runner,
        publisher=publisher,
        scheduler=scheduler,
        assemblers=assembler_registry,
        outcomes=outcome_registry,
    )

    job_service = JobService(
        repo=job_repo,
        event_publisher=publisher
        )

    # --- event subscription
    event_bus.subscribe(JobCompleted, manager)
    event_bus.subscribe(JobMovedToVerifying, manager)
    event_bus.subscribe(TranscodeVerified, job_service)

    return ApplicationTestSystem(
        filesystem=filesystem,
        radarr=radarr,
        jellyfin=jellyfin,
        job_repo=job_repo,
        assembler_registry=assembler_registry,
        outcome_registry=outcome_registry,
        runner=runner,
        manager=manager,
        job_service=job_service,
        event_bus=event_bus,
        publisher=publisher,
        scheduler=scheduler,
    )

def bootstrap_workflow_test_system(
    *,
    runner: ProcessRunner | None = None,
) -> WorkflowTestSystem:
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

    job_verification_assembler = JobVerificationProcessAssembler(
        filesystem=filesystem,
    )

    assembler_registry = ProcessAssemblerRegistry()
    assembler_registry.register(JobMovedToVerifying, job_verification_assembler)
    assembler_registry.register(JobCompleted, job_completion_assembler)

    # --- process outcome contexts ---
    completion_outcome_handler = JobCompletionOutcomeHandler()
    verification_outcome_handler = JobVerificationOutcomeHandler()

    outcome_registry = OutcomeHandlerRegistry()
    outcome_registry.register(JobMovedToVerifying, verification_outcome_handler)
    outcome_registry.register(JobCompleted, completion_outcome_handler)

    # --- execution ---
    runner = runner or FakeProcessRunner(result=ProcessRunnerResult.success())

    # --- side effects ---
    event_bus=FakeSyncEventBus()
    publisher = EventPublisher(event_bus=event_bus)
    scheduler = TaskScheduler()

    # --- orchestration ---
    manager = ProcessManager(
        runner=runner,
        publisher=publisher,
        scheduler=scheduler,
        assemblers=assembler_registry,
        outcomes=outcome_registry,
    )

    # --- event subscription
    event_bus.subscribe(JobCompleted, manager)
    event_bus.subscribe(JobMovedToVerifying, manager)

    return WorkflowTestSystem(
        filesystem=filesystem,
        radarr=radarr,
        jellyfin=jellyfin,
        assembler_registry=assembler_registry,
        outcome_registry=outcome_registry,
        runner=runner,
        manager=manager,
        event_bus=event_bus,
        publisher=publisher,
        scheduler=scheduler,
    )

def bootstrap_job_service_test_system() -> JobServiceTestSystem:
    # --- infrastructure fakes ---
    job_repo = FakeJobRepository()

    # --- side effects ---
    event_bus=FakeSyncEventBus()
    publisher = EventPublisher(event_bus=event_bus)

    # --- orchestration ---
    job_service = JobService(
        repo=job_repo,
        event_publisher=publisher
        )

    # --- event subscription
    event_bus.subscribe(TranscodeVerified, job_service)

    return JobServiceTestSystem(
        job_repo=job_repo,
        job_service=job_service,
        event_bus=event_bus,
        publisher=publisher,
    )