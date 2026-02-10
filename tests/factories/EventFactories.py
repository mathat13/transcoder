import factory

from faker import Faker
import uuid

from domain import (
    JobCompleted,
    FileInfo,
    ExternalMediaIDs,
)

fake = Faker()

class JobCompletedEventFactory(factory.Factory):
    class Meta:
        model = JobCompleted

    job_id = factory.LazyFunction(lambda: uuid.uuid4())
    source_file = factory.LazyFunction(lambda: FileInfo.create(f"/media/{fake.file_name(extension='mkv')}"))
    transcode_file = factory.LazyFunction(lambda: FileInfo.create(f"/media/{fake.file_name(extension='mkv')}"))
    media_ids = factory.LazyFunction(lambda: ExternalMediaIDs.create(fake.random_int(min=10, max=50)))

