"""!
@file database.py
@brief Database configuration and connection management for CodeRunner
@details This module sets up the SQLAlchemy database engine, session factory, and provides 
         database connection utilities for the FastAPI application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models.models import Base
from dotenv import load_dotenv

load_dotenv()

## @brief Retrieved from environment variable DATABASE_URL, with fallback to default PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

## @brief SQLAlchemy database engine
## @details Creates the database engine using the configured DATABASE_URL
engine = create_engine(DATABASE_URL)

## @brief SQLAlchemy session factory
## @details Configured with autocommit=False and autoflush=False for explicit transaction control
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Create all database tables based on the defined models
Base.metadata.create_all(bind=engine)


def get_db():
    """!
    @brief Database session dependency provider
    @details Creates a new database session for each request and ensures proper cleanup.
    @yield Session: SQLAlchemy database session
    @note The session is automatically closed after use, even if an exception occurs
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
