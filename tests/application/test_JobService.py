from uuid import uuid4

from domain import (
    JobCreated,
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    JobFailed,
    JobStatus,
    OperationContext,
    FileInfo,
    ExternalMediaIDs,
)

from application import (
    EventPublisher,
    JobService,
    EventEnvelope,
    TranscodeVerified,
)

from tests import (
    FakeJobRepository,
    FakeSyncEventBus,
    JobFactory,
)

def test_JobService_emits_correct_events_on_status_transition():
    bus = FakeSyncEventBus()
    repo = FakeJobRepository()
    publisher = EventPublisher(bus)
    svc = JobService(repo, publisher)

    handled = []

    def handler(envelope):
        handled.append(envelope)

    bus.subscribe(JobCreated, handler)
    bus.subscribe(JobMovedToProcessing, handler)
    bus.subscribe(JobMovedToVerifying, handler)
    bus.subscribe(JobCompleted, handler)
    bus.subscribe(JobFailed, handler)

    # Add created job event check here!

    pending_job = JobFactory(status=JobStatus.pending)
    svc._transition_job(pending_job, JobStatus.processing)
    assert isinstance(pending_job.events[0], JobMovedToProcessing)

    processing_job = JobFactory(status=JobStatus.processing)
    svc._transition_job(processing_job, JobStatus.verifying)
    assert isinstance(processing_job.events[0], JobMovedToVerifying)

    verifying_job = JobFactory(status=JobStatus.verifying)
    svc._transition_job(verifying_job, JobStatus.success)
    assert isinstance(verifying_job.events[0], JobCompleted)

    # Test failure transitions
    verifying_job = JobFactory(status=JobStatus.verifying)
    svc._transition_job(verifying_job, JobStatus.error)
    assert isinstance(verifying_job.events[0], JobFailed)

    processing_job = JobFactory(status=JobStatus.processing)
    svc._transition_job(processing_job, JobStatus.error)
    assert isinstance(processing_job.events[0], JobFailed)

def test_JobService_call_method_with_TranscodeVerified_event_emits_JobCompleted_on_success():
    bus = FakeSyncEventBus()
    repo = FakeJobRepository()
    publisher = EventPublisher(bus)
    svc = JobService(repo, publisher)

    handled = []

    def handler(envelope):
        handled.append(type(envelope.event))

    job = JobFactory(status=JobStatus.verifying)
    repo.save(job)

    bus.subscribe(JobCompleted, handler)
    bus.subscribe(TranscodeVerified, svc)

    envelope = EventEnvelope(
        event=TranscodeVerified(job_id=job.id, transcode_file=job.transcode_file),
        context=OperationContext.create()
    )

    bus.publish(envelope)

    assert handled == [
        JobCompleted,
    ]

def test_JobService_emit_emits_events_correctly():
    bus = FakeSyncEventBus()
    publisher = EventPublisher(bus)
    svc = JobService(None, publisher)
    job = JobFactory()
    context = OperationContext.create()
    job.events = [JobCompleted(job_id=uuid4(),
                                source_file=FileInfo("/input.mp4"),
                                transcode_file=FileInfo("/transcode.mp4"),
                                media_ids=ExternalMediaIDs.create(6),
                                ),
                  JobMovedToProcessing(job_id=None),
                  JobMovedToVerifying(job_id=None,transcode_file=None),
                  ]
    svc._emit(job, context)

    assert bus.unpublished == [JobCompleted,
                  JobMovedToProcessing,
                  JobMovedToVerifying,
                  ]
    

