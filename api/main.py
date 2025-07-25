from fastapi import APIRouter
from api.routes.shorten import router as shorten_router
from api.routes.redirect import router as redirect_router
from api.routes.analytics import router as analytics_router
from api.routes.generate_flyer import router as generate_flyer_router

api_router = APIRouter()

api_router.include_router(analytics_router)
api_router.include_router(shorten_router)
api_router.include_router(redirect_router)
api_router.include_router(generate_flyer_router)
