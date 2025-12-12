from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Text, CheckConstraint, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
############################################
DATABASE_URL = ""
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#############################################
# TABLES
#############################################

class User(Base):
    __tablename__ = "USER"
    userID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    gender = Column(String(100))
    birthdate = Column(DateTime, nullable=False)
    bio = Column(Text)
    isBanned = Column(Boolean,default=False)
    banUntil = Column(DateTime)
    banAdminID = Column(Integer, ForeignKey("ADMIN.adminID"))
    banReason = Column(Text)



