"""
时间管理模型：tasks, pomodoro_sessions, schedules
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum


class TaskPriority(str, enum.Enum):
    """任务优先级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, enum.Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(Base):
    """Todo任务表"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, index=True)
    due_date = Column(DateTime, index=True)
    completed_at = Column(DateTime)
    category = Column(String(50))  # 学习/工作/生活
    estimated_time = Column(Integer)  # 预计时长（分钟）
    actual_time = Column(Integer)  # 实际时长（分钟）
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    pomodoro_sessions = relationship("PomodoroSession", back_populates="task", cascade="all, delete-orphan")


class SessionType(str, enum.Enum):
    """番茄钟类型枚举"""
    FOCUS = "focus"
    BREAK = "break"


class PomodoroSession(Base):
    """番茄钟记录表"""
    __tablename__ = "pomodoro_sessions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"))
    duration = Column(Integer, default=25)  # 时长（分钟）
    session_type = Column(SQLEnum(SessionType), default=SessionType.FOCUS)
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime)
    is_completed = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # 关系
    task = relationship("Task", back_populates="pomodoro_sessions")


class Schedule(Base):
    """日程安排表"""
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False, index=True)
    category = Column(String(50))  # 会议/学习/生活/娱乐
    location = Column(String(200))
    reminder_minutes = Column(Integer)  # 提前提醒时间
    is_all_day = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
