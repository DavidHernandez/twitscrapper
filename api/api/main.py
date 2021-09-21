from fastapi import FastAPI

from .routers import search, status, user

api = FastAPI()

api.include_router(search.router)
api.include_router(status.router)
api.include_router(user.router)
