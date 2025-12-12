from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Enum, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

DATABASE_URL = ""
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

#############################################
# TABLES
#############################################

# Admin table
class Admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    start_date = Column(DateTime, default=datetime.now)

# User table
class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    gender = Column(String(20))
    birthdate = Column(DateTime)
    bio = Column(Text)
    is_banned = Column(Boolean, default=False)
    ban_until = Column(DateTime)
    ban_admin_id = Column(Integer, ForeignKey("admin.admin_id"))
    ban_reason = Column(String(255))

    ban_admin = relationship("Admin")

# Author table
class Author(Base):
    __tablename__ = "author"
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    gender = Column(String(20))
    bio = Column(Text)
    is_banned = Column(Boolean, default=False)
    ban_until = Column(DateTime)
    ban_admin_id = Column(Integer, ForeignKey("admin.admin_id"))
    ban_reason = Column(String(255))

    ban_admin = relationship("Admin")
    novels = relationship("Novel", back_populates="author")

# Novel table
class Novel(Base):
    __tablename__ = "novel"
    novel_id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("author.author_id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    summary = Column(Text)
    status = Column(Enum("in-progress", "hiatus", "completed", name="novel_status"), default="in-progress", nullable=False)

    author = relationship("Author", back_populates="novels")
    chapters = relationship("Chapter", back_populates="novel", cascade="all, delete-orphan")
    images = relationship("Image", back_populates="novel", cascade="all, delete-orphan")

# Chapter table
class Chapter(Base):
    __tablename__ = "chapter"
    chapter_id = Column(Integer, primary_key=True, autoincrement=True)
    novel_id = Column(Integer, ForeignKey("novel.novel_id"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(100))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    status = Column(Enum("published", "draft", name="chapter_status"),default="draft", nullable=False)

    novel = relationship("Novel", back_populates="chapters")
    images = relationship("Image", back_populates="chapter", cascade="all, delete-orphan")

# Image table
class Image(Base):
    __tablename__ = "image"
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    novel_id = Column(Integer, ForeignKey("novel.novel_id"), nullable=True)
    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), nullable=True)
    author_id = Column(Integer, ForeignKey("author.author_id"), nullable=True)
    file_path = Column(String(255), nullable=False)
    image_type = Column(Enum("cover", "chapter", "other", name="image_type_enum"), default="cover")
    uploaded_at = Column(DateTime, default=datetime.now)

    novel = relationship("Novel", back_populates="images")
    chapter = relationship("Chapter", back_populates="images")
    author = relationship("Author")
class Tag(Base):
    __tablename__ = "tag"
    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

# Association table for many-to-many Novel ↔ Tag
class NovelTag(Base):
    __tablename__ = "novel_tag"
    novel_tag_id = Column(Integer, primary_key=True, autoincrement=True)
    novel_id = Column(Integer, ForeignKey("novel.novel_id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tag.tag_id"), nullable=False)

# Comment table (per chapter)
class Comment(Base):
    __tablename__ = "comment"
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Review table (per novel)
class Review(Base):
    __tablename__ = "review"
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    novel_id = Column(Integer, ForeignKey("novel.novel_id"), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Rating table (per novel)
class Rating(Base):
    __tablename__ = "rating"
    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    novel_id = Column(Integer, ForeignKey("novel.novel_id"), nullable=False)
    score = Column(Integer, nullable=False)  # 1-5 scale
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Bookmark table
class Bookmark(Base):
    __tablename__ = "bookmark"
    bookmark_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    novel_id = Column(Integer, ForeignKey("novel.novel_id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), nullable=True)
    progress = Column(Float, default=0.0)  # percentage or page
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# Reading history table
class ReadingHistory(Base):
    __tablename__ = "reading_history"
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    novel_id = Column(Integer, ForeignKey("novel.novel_id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), nullable=False)
    read_at = Column(DateTime, default=datetime.now)