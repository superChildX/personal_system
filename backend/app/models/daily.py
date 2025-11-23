"""
每日记录模型：daily_records, daily_tasks
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date, Boolean, DECIMAL, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class DailyRecord(Base):
    """每日记录表"""
    __tablename__ = "daily_records"
    __table_args__ = (
        UniqueConstraint('user_id', 'record_date', name='unique_user_date'),
    )
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    record_date = Column(Date, nullable=False, index=True)
    study_hours = Column(DECIMAL(4, 1))  # 学习时长
    sleep_hours = Column(DECIMAL(3, 1))  # 睡眠时长
    exercise_done = Column(Boolean, default=False)  # 是否运动
    mood_rating = Column(Integer)  # 心情指数 1-5
    tasks_completed = Column(Integer, default=0)  # 完成任务数
    tasks_total = Column(Integer, default=0)  # 总任务数
    summary = Column(Text)  # 今日总结
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    
    # 关系
    daily_tasks = relationship("DailyTask", back_populates="daily_record", cascade="all, delete-orphan")


class DailyTask(Base):
    """每日任务明细表"""
    __tablename__ = "daily_tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    daily_record_id = Column(Integer, ForeignKey("daily_records.id", ondelete="CASCADE"), nullable=False)
    task_description = Column(String(200), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    
    # 关系
    daily_record = relationship("DailyRecord", back_populates="daily_tasks")
