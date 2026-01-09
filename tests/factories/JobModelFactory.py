import factory
from faker import Faker
import datetime
import uuid

from domain import ExternalMediaIDs

from infrastructure import JobModel

fake = Faker()

class JobModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = JobModel
        sqlalchemy_session = None  # we will inject the test DB session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    external_media_ids = factory.LazyFunction(lambda: ExternalMediaIDs.create(fake.random_int(min=10, max=50)))
    source_path = factory.LazyFunction(lambda: fake.file_path(extension="mkv"))
    transcode_path = factory.LazyFunction(lambda: fake.file_path(extension="mkv"))
    status = "pending"
    created_at = factory.LazyFunction(lambda: fake.date_time_this_year(tzinfo=datetime.timezone.utc))
    updated_at = factory.LazyFunction(lambda: fake.date_time_this_year(tzinfo=datetime.timezone.utc))