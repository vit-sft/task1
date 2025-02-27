from sqlalchemy import Delete
from sqlalchemy import Update
from sqlalchemy.sql.functions import current_timestamp

from models.db import User, Post
from db.context import session_maker


def add(text: str, user_id: int)-> User:
    with session_maker.begin() as session:
        post = Post()
        post.text = text
        post.user_id = user_id

        session.add(post)
        session.flush()

        return post
    
def get_posts(user_id: int) -> list[Post]:
    with session_maker.begin() as session:
        return session.query(Post).where(
            Post.user_id == user_id          
        ).all()

def delete_post(id: int, user_id: int) -> None:
    with session_maker.begin() as session:
        return session.query(Post).where(
            Post.id == id,
            Post.user_id == user_id
        ).delete()
