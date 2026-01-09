from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, composite
import datetime
import uuid

from infrastructure.persistence.db.shared.base import Base

from domain import (
    ExternalMediaIDs,
)

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    radarr_id: Mapped[int] = mapped_column(Integer, nullable=False)
    source_path = Column(String, nullable=False)        # original file path
    transcode_path = Column(String, nullable=False)        # final transcoded file
    status = Column(String, nullable=False)          # current workflow state
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    external_media_ids = composite(ExternalMediaIDs, radarr_id)