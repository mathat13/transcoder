import factory
from factory import Faker, SubFactory, List
from typing import List as TypingList

from infrastructure import (
    Language,
    Quality1,
    Revision,
    Quality,
    SelectOption,
    Field,
    Specification,
    CustomFormat,
    MediaInfo,
    GetMovieFileResponse,
)

# --------------------
# Simple models
# --------------------

class LanguageFactory(factory.Factory):
    class Meta:
        model = Language

    id = factory.Sequence(lambda n: n + 1)
    name = Faker("language_name")


class Quality1Factory(factory.Factory):
    class Meta:
        model = Quality1

    id = factory.Sequence(lambda n: n + 1)
    name = Faker("word")
    source = Faker("word")
    resolution = Faker("random_int", min=480, max=4320)
    modifier = Faker("word")


class RevisionFactory(factory.Factory):
    class Meta:
        model = Revision

    version = Faker("random_int", min=1, max=10)
    real = Faker("random_int", min=0, max=5)
    isRepack = Faker("boolean")


class QualityFactory(factory.Factory):
    class Meta:
        model = Quality

    quality = SubFactory(Quality1Factory)
    revision = SubFactory(RevisionFactory)


class SelectOptionFactory(factory.Factory):
    class Meta:
        model = SelectOption

    value = Faker("random_int", min=0, max=100)
    name = Faker("word")
    order = Faker("random_int", min=0, max=10)
    hint = Faker("sentence")
    dividerAfter = Faker("boolean")


class FieldFactory(factory.Factory):
    class Meta:
        model = Field

    order = Faker("random_int", min=0, max=10)
    name = Faker("word")
    label = Faker("word")
    unit = Faker("word")
    helpText = Faker("sentence")
    helpTextWarning = Faker("sentence")
    helpLink = Faker("url")
    value = Faker("word")
    type = Faker("word")
    advanced = Faker("boolean")
    selectOptions = List([SubFactory(SelectOptionFactory) for _ in range(2)])
    selectOptionsProviderAction = Faker("word")
    section = Faker("word")
    hidden = Faker("word")
    privacy = Faker("word")
    placeholder = Faker("word")
    isFloat = Faker("boolean")


class SpecificationFactory(factory.Factory):
    class Meta:
        model = Specification

    id = factory.Sequence(lambda n: n + 1)
    name = Faker("word")
    implementation = Faker("word")
    implementationName = Faker("word")
    infoLink = Faker("url")
    negate = Faker("boolean")
    required = Faker("boolean")
    fields = List([SubFactory(FieldFactory) for _ in range(2)])
    presets = List([Faker("word") for _ in range(2)])


class CustomFormatFactory(factory.Factory):
    class Meta:
        model = CustomFormat

    id = factory.Sequence(lambda n: n + 1)
    name = Faker("word")
    includeCustomFormatWhenRenaming = Faker("boolean")
    specifications = List([SubFactory(SpecificationFactory) for _ in range(1)])


class MediaInfoFactory(factory.Factory):
    class Meta:
        model = MediaInfo

    id = factory.Sequence(lambda n: n + 1)
    audioBitrate = Faker("random_int", min=64, max=512)
    audioChannels = Faker("random_int", min=1, max=8)
    audioCodec = Faker("word")
    audioLanguages = Faker("language_name")
    audioStreamCount = Faker("random_int", min=1, max=5)
    videoBitDepth = Faker("random_int", min=8, max=12)
    videoBitrate = Faker("random_int", min=1000, max=50000)
    videoCodec = Faker("word")
    videoFps = Faker("random_int", min=24, max=120)
    videoDynamicRange = Faker("word")
    videoDynamicRangeType = Faker("word")
    resolution = Faker("word")
    runTime = Faker("time")
    scanType = Faker("word")
    subtitles = Faker("language_name")


# --------------------
# Root response model
# --------------------

class GetMovieFileResponseFactory(factory.Factory):
    class Meta:
        model = GetMovieFileResponse

    id = factory.Sequence(lambda n: n + 1)
    movieId = Faker("random_int", min=1, max=10000)
    relativePath = Faker("file_path")
    path = Faker("file_path")
    size = Faker("random_int", min=1_000_000, max=50_000_000_000)
    dateAdded = Faker("iso8601")
    sceneName = Faker("sentence", nb_words=3)
    releaseGroup = Faker("word")
    edition = Faker("word")
    languages = List([SubFactory(LanguageFactory) for _ in range(2)])
    quality = SubFactory(QualityFactory)
    customFormats = List([SubFactory(CustomFormatFactory) for _ in range(1)])
    customFormatScore = Faker("random_int", min=-100, max=100)
    indexerFlags = Faker("random_int", min=0, max=10)
    mediaInfo = SubFactory(MediaInfoFactory)
    originalFilePath = Faker("file_path")
    qualityCutoffNotMet = Faker("boolean")