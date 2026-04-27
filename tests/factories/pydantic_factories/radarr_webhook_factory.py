import factory
from factory import SubFactory
from faker import Faker

from presentation import (
    Movie,
    MovieFile,
    RadarrWebhookCreateRequest,
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

class RadarrWebhookCreateRequestFactory(factory.Factory):
    class Meta:
        model = RadarrWebhookCreateRequest

    movie = SubFactory(MovieFactory)
    movieFile = SubFactory(MovieFileFactory)