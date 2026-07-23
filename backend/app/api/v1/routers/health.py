"""Health check endpoint — verifies API, DB, and Redis connectivity."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis_client import ping_redis

router = APIRouter(tags=["system"])


@router.get("/health")
async def health(db: AsyncSession = Depends(get_db)) -> dict:
    # DB check
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    redis_ok = await ping_redis()

    status = "ok" if (db_ok and redis_ok) else "degraded"
    return {
        "success": True,
        "data": {"status": status, "db": db_ok, "redis": redis_ok},
        "message": "OK",
    }
