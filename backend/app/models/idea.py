"""
灵感捕捉模型：ideas, media_records
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from ..database import Base
import enum


class IdeaType(str, enum.Enum):
    """灵感类型枚举"""
    QUICK_NOTE = "quick_note"
    PROJECT_IDEA = "project_idea"
    BOOK_REVIEW = "book_review"
    MOVIE_REVIEW = "movie_review"


class IdeaPriority(str, enum.Enum):
    """灵感优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Idea(Base):
    """灵感笔记表"""
    __tablename__ = "ideas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200))
    content = Column(Text, nullable=False)
    type = Column(SQLEnum(IdeaType))
    priority = Column(SQLEnum(IdeaPriority))
    feasibility = Column(String(50))  # 可行性评估
    tags = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class MediaType(str, enum.Enum):
    """媒体类型枚举"""
    BOOK = "book"
    MOVIE = "movie"
    COURSE = "course"


class MediaStatus(str, enum.Enum):
    """媒体状态枚举"""
    WANT = "want"
    READING = "reading"
    FINISHED = "finished"


class MediaRecord(Base):
    """读书/电影记录表"""
    __tablename__ = "media_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(SQLEnum(MediaType))
    title = Column(String(200), nullable=False)
    author = Column(String(100))
    rating = Column(Integer)  # 1-5星
    status = Column(SQLEnum(MediaStatus), default=MediaStatus.WANT)
    review = Column(Text)
    notes = Column(Text)
    tags = Column(JSON)
    finished_at = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
