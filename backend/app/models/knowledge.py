"""
知识库模型：interview_questions, resources, leetcode_problems
"""
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Boolean, JSON, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from ..database import Base
import enum


class Difficulty(str, enum.Enum):
    """难度枚举"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class InterviewQuestion(Base):
    """面试题表"""
    __tablename__ = "interview_questions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question = Column(String(500), nullable=False)
    answer = Column(Text)
    category = Column(String(50))  # JavaScript/算法/网络/操作系统等
    difficulty = Column(SQLEnum(Difficulty))
    tags = Column(JSON)
    is_mastered = Column(Boolean, default=False)
    review_count = Column(Integer, default=0)
    last_reviewed_at = Column(DateTime)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())


class ResourceType(str, enum.Enum):
    """资源类型枚举"""
    ARTICLE = "article"
    VIDEO = "video"
    COURSE = "course"
    TOOL = "tool"
    DOCUMENTATION = "documentation"


class Resource(Base):
    """技术资源收藏表"""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    url = Column(String(500))
    type = Column(SQLEnum(ResourceType))
    description = Column(Text)
    tags = Column(JSON)
    rating = Column(Integer)  # 1-5星
    is_favorite = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class LeetCodeProblem(Base):
    """LeetCode刷题记录表"""
    __tablename__ = "leetcode_problems"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(Integer, nullable=False)  # LeetCode题目ID
    title = Column(String(200), nullable=False)
    difficulty = Column(SQLEnum(Difficulty), index=True)
    category = Column(String(50))  # 数组/链表/动态规划等
    solution = Column(Text)  # 解题思路
    code = Column(Text)  # 代码实现
    time_complexity = Column(String(50))
    space_complexity = Column(String(50))
    is_solved = Column(Boolean, default=False)
    attempts = Column(Integer, default=1)
    last_attempted_at = Column(DateTime)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
