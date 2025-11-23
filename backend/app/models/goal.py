"""
目标与复盘模型：goals, key_results, habit_logs, monthly_reviews
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date, Boolean, DECIMAL, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum


class GoalType(str, enum.Enum):
    """目标类型枚举"""
    OKR = "okr"
    HABIT = "habit"


class GoalStatus(str, enum.Enum):
    """目标状态枚举"""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Goal(Base):
    """OKR目标表"""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(SQLEnum(GoalType))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    quarter = Column(String(10))  # 2024Q4
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(SQLEnum(GoalStatus), default=GoalStatus.ACTIVE)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    key_results = relationship("KeyResult", back_populates="goal", cascade="all, delete-orphan")
    habit_logs = relationship("HabitLog", back_populates="goal", cascade="all, delete-orphan")


class KeyResult(Base):
    """关键结果表"""
    __tablename__ = "key_results"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False)
    description = Column(String(300), nullable=False)
    target_value = Column(DECIMAL(10, 2))  # 目标值
    current_value = Column(DECIMAL(10, 2), default=0)  # 当前值
    unit = Column(String(20))  # 单位：个/次/小时
    progress = Column(Integer, default=0)  # 进度百分比
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    goal = relationship("Goal", back_populates="key_results")


class HabitLog(Base):
    """习惯打卡表"""
    __tablename__ = "habit_logs"
    __table_args__ = (
        UniqueConstraint('goal_id', 'log_date', name='unique_habit_date'),
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False)
    log_date = Column(Date, nullable=False)
    is_completed = Column(Boolean, default=True)
    note = Column(String(200))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # 关系
    goal = relationship("Goal", back_populates="habit_logs")


class MonthlyReview(Base):
    """月度复盘表"""
    __tablename__ = "monthly_reviews"
    __table_args__ = (
        UniqueConstraint('user_id', 'year', 'month', name='unique_user_month'),
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    summary = Column(Text)
    achievements = Column(Text)  # 本月成果
    problems = Column(Text)  # 遇到的问题
    improvements = Column(Text)  # 改进计划
    study_hours = Column(DECIMAL(6, 1))
    tasks_completed = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
