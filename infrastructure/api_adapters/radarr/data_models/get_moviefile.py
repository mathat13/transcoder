from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict
from typing import Optional

class RadarrBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

class Language(RadarrBaseModel):
    id: int
    name: str


class Quality1(RadarrBaseModel):
    id: int
    name: str
    source: str
    resolution: int
    modifier: str


class Revision(RadarrBaseModel):
    version: int
    real: int
    isRepack: bool


class Quality(RadarrBaseModel):
    quality: Quality1
    revision: Revision


class SelectOption(RadarrBaseModel):
    value: int
    name: str
    order: int
    hint: str
    dividerAfter: bool


class Field(RadarrBaseModel):
    order: int
    name: str
    label: str
    unit: str
    helpText: str
    helpTextWarning: str
    helpLink: str
    value: str
    type: str
    advanced: bool
    selectOptions: List[SelectOption]
    selectOptionsProviderAction: str
    section: str
    hidden: str
    privacy: str
    placeholder: str
    isFloat: bool


class Specification(RadarrBaseModel):
    id: int
    name: str
    implementation: str
    implementationName: str
    infoLink: str
    negate: bool
    required: bool
    fields: List[Field]
    presets: List[str]


class CustomFormat(RadarrBaseModel):
    id: int
    name: str
    includeCustomFormatWhenRenaming: bool
    specifications: List[Specification]


class MediaInfo(RadarrBaseModel):
    id: Optional[int] = None
    audioBitrate: int
    audioChannels: float
    audioCodec: str
    audioLanguages: str
    audioStreamCount: int
    videoBitDepth: int
    videoBitrate: int
    videoCodec: str
    videoFps: float
    videoDynamicRange: str
    videoDynamicRangeType: str
    resolution: str
    runTime: str
    scanType: str
    subtitles: str


class GetMovieFileResponse(RadarrBaseModel):
    id: int
    movieId: int
    relativePath: str
    path: str
    size: int
    dateAdded: str
    sceneName: str
    releaseGroup: str
    edition: str
    languages: List[Language]
    quality: Quality
    customFormats: List[CustomFormat]
    customFormatScore: int
    indexerFlags: int
    mediaInfo: MediaInfo
    originalFilePath: str
    qualityCutoffNotMet: bool

