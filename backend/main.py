from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users_operations import users_crud_router
from app.recos_operations import recos_crud_router
from app.auth import auth_router

app = FastAPI(title="YWT")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ywt-production.up.railway.app",
        "https://ywt-tau.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_crud_router)
app.include_router(recos_crud_router)
app.include_router(auth_router)
