"""
Finance-only FastAPI service entrypoint.
Exposes authentication and financial calculation APIs without the agent features.
"""
import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from common.logger import setup_logger
from api.auth_api import router as auth_router
from api.financial.attendance_api import router as attendance_router
from api.financial.overtime_api import router as overtime_router
from api.financial.work_time_api import router as work_time_router

logger = setup_logger("finance-app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Simple lifecycle hooks for startup/shutdown logging."""
    logger.info("=" * 60)
    logger.info("Finance API service starting")
    logger.info("=" * 60)
    yield
    logger.info("Finance API service stopped")


app = FastAPI(
    title="Finance Management API",
    description="Financial attendance and overtime services",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register finance + auth endpoints only
app.include_router(auth_router)
app.include_router(overtime_router)
app.include_router(attendance_router)
app.include_router(work_time_router)


@app.get("/api/health", tags=["health"])
async def health():
    """Basic health check."""
    return {"status": "ok", "service": "finance-api"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
