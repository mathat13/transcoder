from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
import datetime

from infrastructure.persistence.base import Base

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String, nullable=False)           # e.g. "movie" or "episode"
    source_path = Column(String, nullable=False)        # original file path
    output_path = Column(String, nullable=True)        # final transcoded file
    status = Column(String, default="pending")          # current workflow state
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))