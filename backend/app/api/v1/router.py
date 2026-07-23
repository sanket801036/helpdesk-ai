"""Aggregates all v1 routers into a single APIRouter."""
from fastapi import APIRouter

from app.api.v1.routers import auth, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router, prefix="/auth")

# Future phases register their routers here:
# api_router.include_router(tickets.router, prefix="/tickets")
