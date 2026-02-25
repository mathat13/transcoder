import factory

from faker import Faker
import uuid

from domain import (
    JobMovedToProcessing,
    JobMovedToVerifying,
    JobCompleted,
    FileInfo,
    ExternalMediaIDs,
    OperationContext,
    Event,
)

from application import (
    TranscodeVerified,
    EventEnvelope,
)

fake = Faker()

# --- Domain Events ---

class JobMovedToProcessingEventFactory(factory.Factory):
    class Meta:
        model = JobMovedToProcessing

    job_id = factory.LazyFunction(lambda: uuid.uuid4())

class JobMovedToVerifyingEventFactory(factory.Factory):
    class Meta:
        model = JobMovedToVerifying

    job_id = factory.LazyFunction(lambda: uuid.uuid4())
    transcode_file = factory.LazyFunction(lambda: FileInfo.create(f"/media/{fake.file_name(extension='mkv')}"))

class JobCompletedEventFactory(factory.Factory):
    class Meta:
        model = JobCompleted

    job_id = factory.LazyFunction(lambda: uuid.uuid4())
    source_file = factory.LazyFunction(lambda: FileInfo.create(f"/media/{fake.file_name(extension='mkv')}"))
    transcode_file = factory.LazyFunction(lambda: FileInfo.create(f"/media/{fake.file_name(extension='mkv')}"))
    media_ids = factory.LazyFunction(lambda: ExternalMediaIDs.create(fake.random_int(min=10, max=50)))


# --- Application Events ---
class TranscodeVerifiedEventFactory(factory.Factory):
    class Meta:
        model = TranscodeVerified

    job_id = factory.LazyFunction(lambda: uuid.uuid4())
    transcode_file = factory.LazyFunction(lambda: FileInfo.create(f"/media/{fake.file_name(extension='mkv')}"))

class EventEnvelopeFactory(factory.Factory):

    class Meta:
        model = EventEnvelope

    # Requires event for instantiation
    event: Event
    context = factory.LazyFunction(lambda: OperationContext.create())

