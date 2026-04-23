import factory
from faker import Faker
from uuid import uuid4

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

    id = factory.LazyFunction(lambda: uuid4())
    source_file = factory.LazyFunction(
        lambda: FileInfo.from_path(f"/media/{fake.file_name(extension='mkv')}"))
    transcode_output_file = factory.LazyFunction(
        lambda: FileInfo.from_path(f"/transcode/{fake.file_name(extension='mkv')}"))
    media_ids = factory.LazyFunction(
        lambda: ExternalMediaIDs.from_radarr(fake.random_int(min=10, max=50)))
    status = JobStatus.pending

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return model_class._create_for_test(**kwargs)
    
