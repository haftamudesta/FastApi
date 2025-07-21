from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func

from backend.db.database import Base


class StoryJob(Base):
    __tablename__ = "story_jobs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True)
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    story_id = Column(String, nollable=True)
    error = Column(String, nollable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
