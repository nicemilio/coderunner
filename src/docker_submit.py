from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import UserCreate, UserLogin, UserResponse, Token
from auth.user_service import get_user_by_username, get_user_by_email, create_user, authenticate_user
from auth.auth import create_access_token
from dependencies import get_current_user
from models.models import User
router = APIRouter()
import shutil
from docker_runner import run_in_docker

app = FastAPI()

@app.post("/submit/")
async def submit_script(file: UploadFile = File(...)):
    target_path = "uploads/user_script.py"
    with open(target_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = run_in_docker(target_path)
    return result