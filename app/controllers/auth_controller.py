from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from utils import formating
from models import db
from models import dto
from services import user_service
from services import jwt_service
from utils.bcrypt_hashing import HashLib
from utils import dependencies
from constants import COOKIES_KEY_NAME
from constants import SESSION_TIME


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=dto.GetUser)
async def signup(user: dto.CreateUser):
    NOW = datetime.now(timezone.utc)

    email = formating.format_string(user.email)
    
    if not email:
        raise HTTPException(
            detail="Email can not be empty",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    if not user.password:
        raise HTTPException(
            detail="Password can not be empty",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    exist_user = user_service.get_by_email(email)
    if exist_user:
        raise HTTPException(
            detail=f"User '{email}' exist",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    created_user = user_service.create(
        email,
        user.password
    )

    exp_date = NOW + SESSION_TIME
    token = jwt_service.encode(created_user.id, exp_date)

    return token

@router.post("/login", status_code=status.HTTP_200_OK, response_model=str)
async def login(dto: dto.LoginUser, res: Response):
    NOW = datetime.now(timezone.utc)
    
    email = formating.format_string(dto.email)
    
    user = user_service.get_by_email(email)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    
    if HashLib.validate(dto.password, user.password) is False:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
    
    exp_date = NOW + SESSION_TIME
    token = jwt_service.encode(user.id, exp_date)
    return token
