"""!
@file user_service.py
@brief User service layer for database operations
@details Provides service functions for user management including creation, retrieval, and authentication.
         Acts as an abstraction layer between the API routes and the database models.
"""

from sqlalchemy.orm import Session
from models.models import User 
from auth.auth import hash_password, verify_password

def get_user_by_username(db: Session, username: str):
    """!
    @brief Retrieve a user by username
    @details Queries the database to find a user with the specified username
    @param db Session: SQLAlchemy database session
    @param username str: The username to search for
    @return User|None: User object if found, None otherwise
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """!
    @brief Retrieve a user by email address
    @details Queries the database to find a user with the specified email address
    @param db Session: SQLAlchemy database session
    @param email str: The email address to search for
    @return User|None: User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, username: str, email: str, password: str):
    """!
    @brief Create a new user in the database
    @details Creates a new user with hashed password, saves to database, and returns the created user
    @param db Session: SQLAlchemy database session
    @param username str: The desired username for the new user
    @param email str: The email address for the new user
    @param password str: The plain text password (will be hashed before storage)
    @return User: The newly created user object with assigned ID
    @note The password is automatically hashed before storage for security
    """
    hashed_password = hash_password(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    """!
    @brief Authenticate a user with username and password
    @details Retrieves user by username and verifies the provided password against the stored hash
    @param db Session: SQLAlchemy database session
    @param username str: The username for authentication
    @param password str: The plain text password to verify
    @return User|False: User object if authentication successful, False otherwise
    @retval User: Valid user object when credentials are correct
    @retval False: When user not found or password is incorrect
    """
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, str(user.hashed_password)):
        return False
    return user
