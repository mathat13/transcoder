import factory
from faker import Faker
import datetime

from domain.aggregate_roots.Job import Job
from domain.value_objects.JobStatus import JobStatus
from domain.value_objects.FileInfo import FileInfo

fake = Faker()

class JobFactory(factory.Factory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n + 1)
    job_type = "episode"
    source_path = FileInfo(fake.file_path(extension="mkv"))
    output_path = source_path.transcoded_path
    status = JobStatus.pending
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year(tzinfo=datetime.timezone.utc))
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_year(tzinfo=datetime.timezone.utc))
