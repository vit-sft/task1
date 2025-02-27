from sqlalchemy import Delete
from sqlalchemy import Update
from sqlalchemy.sql.functions import current_timestamp

from models.db import User
from db.context import session_maker


def add(email: str, password: str)-> User:
    with session_maker.begin() as session:
        user = User()
        user.email = email
        user.password = password

        session.add(user)
        session.flush()

        return user
    
def get_by_id(id: int) -> User | None:
    with session_maker() as session:
        return session.query(User).where(
            User.id == id          
        ).first()

def get_by_email(email: str) -> User | None:
    with session_maker.begin() as session:
        return session.query(User).where(
            User.email == email          
        ).first()
