"""!
@file dependencies.py
@brief Dependency utilities for FastAPI authentication and user retrieval
@details Provides dependency functions for extracting and validating the current user from JWT tokens in API requests.
"""

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt

from database import get_db
from models.models import User
from auth.auth import SECRET_KEY, ALGORITHM

## @brief HTTP Bearer security scheme for FastAPI
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """!
    @brief Retrieve the current authenticated user from JWT credentials
    @details Decodes the JWT token, extracts the user ID, and fetches the user from the database. Raises HTTP 401 if invalid or not found.
    @param credentials HTTPAuthorizationCredentials: Bearer token credentials from the request
    @param db Session: SQLAlchemy database session
    @return User: The authenticated user object
    @throws HTTPException: If the token is invalid or user is not found
    """
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
