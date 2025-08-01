"""!
@file router.py
@brief Authentication API routes for user registration, login and profile access
@details Provides FastAPI router endpoints for user authentication including registration,
         login, and accessing current user profile information.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import UserCreate, UserLogin, UserResponse, Token
from auth.user_service import get_user_by_username, get_user_by_email, create_user, authenticate_user
from auth.auth import create_access_token
from dependencies import get_current_user
from models.models import User
router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=400, 
            detail="Username already registered"
        )
    
    # Check if email exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    # Create user
    db_user = create_user(db, user_data.username, user_data.email, user_data.password)
    
    # Create token
    access_token = create_access_token(data={"sub": db_user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(db_user)
    }


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """!
    @brief Authenticate user and generate access token
    @details Validates user credentials and returns an access token upon successful authentication
    @param user_credentials UserLogin: Login credentials containing username and password
    @param db Session: SQLAlchemy database session
    @return Token: Access token, token type, and user information
    @throws HTTPException: 401 if credentials are incorrect
    """
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """!
    @brief Get current authenticated user information
    @details Returns the profile information of the currently authenticated user
    @param current_user User: The authenticated user from JWT token (injected by dependency)
    @return UserResponse: Current user's profile information
    @note Requires valid JWT token in Authorization header
    """
    return UserResponse.model_validate(current_user)
