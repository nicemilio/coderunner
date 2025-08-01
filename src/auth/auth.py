"""!
@file auth.py
@brief Authentication utilities for password hashing and JWT token management
@details Provides functions for secure password hashing using bcrypt and JWT token creation
         for user authentication in the CodeRunner application.
"""

from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
import os

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set. The application cannot start without it.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

## @brief Password hashing context using bcrypt
## @details Configured with bcrypt scheme for secure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """!
    @brief Hash a plain text password using bcrypt
    @details Creates a secure hash of the provided password using the configured bcrypt context
    @param password str: The plain text password to hash
    @return str: The hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """!
    @brief Verify a plain text password against a hashed password
    @details Compares the plain text password with the stored hash to authenticate users
    @param plain_password str: The plain text password to verify
    @param hashed_password str: The stored hashed password to compare against
    @return bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """!
    @brief Create a JWT access token with expiration
    @details Generates a JWT token containing the provided data with automatic expiration time
    @param data dict: The payload data to include in the token (typically user ID)
    @return str: The encoded JWT token string
    @note Token expires after ACCESS_TOKEN_EXPIRE_MINUTES (30 minutes by default)
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
