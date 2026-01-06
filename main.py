from fastapi import FastAPI

from app.users_operations import users_crud_router
from app.recos_operations import recos_crud_router
from app.auth import auth_router

app = FastAPI(title="YWT")

app.include_router(users_crud_router)
app.include_router(recos_crud_router)
app.include_router(auth_router)