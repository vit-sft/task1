from enum import StrEnum

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.sql.functions import current_timestamp

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    email = Column("email", String(256), unique=True)
    password = Column("password", String(256))
    updated_at = Column("updated_at", DateTime(), default=current_timestamp())
    created_at = Column("created_at", DateTime(), default=current_timestamp())

# one to one relationship
class Post(Base):
    __tablename__ = 'posts'
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    text = Column("text", Text())
    user_id = Column("user_id", Integer(), ForeignKey('users.id'))
    updated_at = Column("updated_at", DateTime(), default=current_timestamp())
    created_at = Column("created_at", DateTime(), default=current_timestamp())