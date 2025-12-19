import factory
from faker import Faker
import datetime
import uuid

from domain import (
    Job,
    JobStatus,
    FileInfo
)

fake = Faker()

class JobFactory(factory.Factory):
    class Meta:
        model = Job

    id = factory.LazyFunction(lambda: uuid.uuid4())
    job_type = "episode"
    source_path = factory.LazyFunction(lambda: FileInfo(f"/media/{fake.file_name(extension='mkv')}"))
    output_path = factory.LazyFunction(lambda: FileInfo(f"/media/{fake.file_name(extension='mkv')}"))
    status = JobStatus.pending
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year(tzinfo=datetime.timezone.utc))
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_year(tzinfo=datetime.timezone.utc))
