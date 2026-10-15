from sqlalchemy import Column, Integer, String, Text, ForeignKey
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    is_verified = Column(Integer, default=0)
    verification_token = Column(String(255), nullable=True)


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_text = Column(Text)
    result = Column(Text)