import factory
from factory import SubFactory
from faker import Faker

from presentation.api.use_cases.jobs.external.radarr.commands.create_job.ingress.request import (
    Movie,
    MovieFile,
    CreateJobRequest,
)

from integrations import RadarrWebhookPayload

fake = Faker()

class MovieFactory(factory.Factory):
    class Meta:
        model = Movie
    
    id = factory.LazyFunction(lambda: fake.random_int(min=1, max=100))


class MovieFileFactory(factory.Factory):
    class Meta:
        model = MovieFile
    
    sourceFile = factory.LazyFunction(lambda: f"/source/{fake.file_name(extension='mkv')}")

class CreateJobRequestFactory(factory.Factory):
    class Meta:
        model = CreateJobRequest

    movie = SubFactory(MovieFactory)
    movieFile = SubFactory(MovieFileFactory)
    eventType = factory.LazyFunction(lambda: "Download")

class RadarrWebhookPayloadFactory(factory.Factory):
    model = RadarrWebhookPayload

    eventType = factory.LazyFunction(lambda: "Download")