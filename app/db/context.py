from typing import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from models.db import Base
from constants import DB_CONNECTION_STRING


if not DB_CONNECTION_STRING:
    raise Exception("DB connection string not provided")

engine = create_engine(DB_CONNECTION_STRING, echo=False, pool_pre_ping=True, pool_recycle=3600) #reconect after 1 hour
session_maker = sessionmaker(bind=engine, expire_on_commit=False)

def create_db() -> None:
    """
    Creates the database tables by calling `Base.metadata.create_all(engine)`.
    """
    Base.metadata.create_all(engine)


def get_db() -> Generator[Session, Any, None]:
    """
    Returns a generator that yields a SQLAlchemy session. This session should be used for all database interactions within the current request context.
    """
    with session_maker() as session:
        yield session
        

def auto_create_db():
    """
    Automatically creates the database if it doesn't already exist.

    For SQLite, the database file is created automatically when connecting if it doesn't exist.
    This function simply calls create_db() to create the tables in the database.
    
    For other database engines like MySQL, it attempts to connect first, and if that fails,
    it will create the database before creating the tables.
    """
    if DB_CONNECTION_STRING.startswith('sqlite:'):
        # For SQLite, just create the tables - the database file is created automatically
        create_db()
    else:
        try:
            # For other database engines, try to connect first
            con = engine.connect()
            create_db()
            con.close()

        except Exception as _:
            connection_string, db_name = DB_CONNECTION_STRING.rsplit("/", 1)
            
            # For MySQL, we need to handle potential query parameters in the connection string
            if "?" in db_name:
                db_name = db_name.split("?")[0]
                
            tmp_engine = create_engine(connection_string)
            with tmp_engine.begin() as session:
                # This is MySQL-compatible syntax
                session.exec_driver_sql(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")

            create_db()
