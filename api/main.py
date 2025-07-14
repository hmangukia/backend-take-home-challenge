from fastapi import APIRouter
from api.routes.shorten import router as shorten_router

api_router = APIRouter()

api_router.include_router(shorten_router)