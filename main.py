from fastapi import FastAPI

from models import User, Link
from api.links_routes import router as link_router
from api.auth_routes import router as user_router


app = FastAPI()

app.include_router(link_router)
app.include_router(user_router)