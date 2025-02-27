from fastapi import APIRouter
from fastapi import Query
from fastapi import Path
from fastapi import HTTPException

from models import db
from models import dto
from services import post_service
from utils import dependencies

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/add-post", response_model=dto.GetUser)
def add_post(text: str, user: dependencies.user_dependency) -> db.User:
    post_service.add(text, user.id)

@router.delete("/delete-post", response_model=dto.GetUser)
def delete_post(id: int, user: dependencies.user_dependency) -> db.User:
    post_service.delete_post(id, user.id)

@router.get("/get-posts", response_model=list[dto.GetPost])
def get_posts(user: dependencies.user_dependency) -> list[db.Post]:
    return post_service.get_posts(user.id)