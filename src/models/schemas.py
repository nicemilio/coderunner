from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, regex=r'^\w+$')
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, regex=r'^\w+$')
    password: str


class UserResponse(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=30, regex=r'^\w+$')
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
