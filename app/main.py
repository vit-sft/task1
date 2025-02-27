from fastapi import FastAPI

from controllers import auth_controller
from controllers import posts_controller

from middlewares import cors_middleware
from db.context import auto_create_db

# Initialize the database
auto_create_db()

app = FastAPI()

cors_middleware.add(app)

app.include_router(auth_controller.router)
app.include_router(posts_controller.router)

