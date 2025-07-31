from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Enum, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

# Defines the DifficultyEnum for problem difficulty levels
class DifficultyEnum(enum.Enum):
    easy = 1
    medium = 2
    hard = 3

# Defines the StatusEnum for submission status
class StatusEnum(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    wrong_answer = "wrong_answer"
    error = "error"

# Defines the User Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="user")

# Defines the Problem Table
class Problem(Base):
    __tablename__ = 'problems'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum(DifficultyEnum), nullable=False)
    example_input = Column(Text, nullable=True)
    example_output = Column(Text, nullable=True)

    test_cases = relationship("TestCase", back_populates="problem")
    submissions = relationship("Submission", back_populates="problem")

# Defines the Submission Table
class Submission(Base):
    __tablename__ = 'submissions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    submitted_code = Column(Text, nullable=False)
    language = Column(String(30), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending, nullable=False)
    execution_time_ms = Column(Float)
    memory_usage_mb = Column(Float)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")

# Defines the TestCase Table
class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False)

    problem = relationship("Problem", back_populates="test_cases")
