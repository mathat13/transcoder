from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime
import uuid

from infrastructure.persistence.db.shared.base import Base

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_type = Column(String, nullable=False)           # e.g. "movie" or "episode"
    source_path = Column(String, nullable=False)        # original file path
    output_path = Column(String, nullable=True)        # final transcoded file
    status = Column(String, nullable=False)          # current workflow state
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))