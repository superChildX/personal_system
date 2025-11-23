"""
经历记录模型：experiences
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date, Enum as SQLEnum
from sqlalchemy.sql import func
from ..database import Base
import enum


class ExperienceType(str, enum.Enum):
    """经历类型枚举"""
    INTERNSHIP = "internship"
    COMPETITION = "competition"
    AWARD = "award"
    ACTIVITY = "activity"


class Experience(Base):
    """经历记录表"""
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(SQLEnum(ExperienceType), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    organization = Column(String(200))
    role = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(Text)
    achievements = Column(Text)  # 成果与收获
    certificate_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
