import factory
from faker import Faker
import datetime
import uuid

from domain import (
    Job,
    JobStatus,
    FileInfo,
    ExternalMediaIDs,
)

fake = Faker()

class JobFactory(factory.Factory):
    class Meta:
        model = Job

    id = factory.LazyFunction(lambda: uuid.uuid4())
    external_media_ids = factory.LazyFunction(lambda: ExternalMediaIDs.create(fake.random_int(min=10, max=50)))
    source_file = factory.LazyFunction(lambda: FileInfo.create(f"/media/{fake.file_name(extension='mkv')}"))
    transcode_file = factory.LazyFunction(lambda: FileInfo.create(f"/media/{fake.file_name(extension='mkv')}"))
    status = JobStatus.pending
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year(tzinfo=datetime.timezone.utc))
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_year(tzinfo=datetime.timezone.utc))
