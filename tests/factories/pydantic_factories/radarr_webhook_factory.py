import factory
from factory import SubFactory
from faker import Faker

from presentation import (
    Movie,
    MovieFile,
    RadarrWebhookCreateJobRequest,
)

fake = Faker()

class MovieFactory(factory.Factory):
    class Meta:
        model = Movie
    
    id = factory.LazyFunction(lambda: fake.random_int(min=1, max=100))


class MovieFileFactory(factory.Factory):
    class Meta:
        model = MovieFile
    
    sourceFile = factory.LazyFunction(lambda: f"/source/{fake.file_name(extension='mkv')}")

class RadarrWebhookCreateJobRequestFactory(factory.Factory):
    class Meta:
        model = RadarrWebhookCreateJobRequest

    movie = SubFactory(MovieFactory)
    movieFile = SubFactory(MovieFileFactory)