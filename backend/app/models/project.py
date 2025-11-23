"""
项目管理模型：projects, project_images
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum


class ProjectStatus(str, enum.Enum):
    """项目状态枚举"""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(Base):
    """项目表"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(ProjectStatus), default=ProjectStatus.IN_PROGRESS, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    github_url = Column(String(255))
    demo_url = Column(String(255))
    tech_stack = Column(JSON)  # 存储技术栈数组
    highlights = Column(Text)  # 项目亮点
    summary = Column(Text)  # 开发总结
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan")


class ProjectImage(Base):
    """项目截图表"""
    __tablename__ = "project_images"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=False)
    caption = Column(String(200))
    display_order = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # 关系
    project = relationship("Project", back_populates="images")
