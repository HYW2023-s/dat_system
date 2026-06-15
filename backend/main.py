"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.config import FRONTEND_DIR, STATIC_DIR
from backend.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: initialize database
    await init_db()
    from backend.services.embedding import load_model_on_startup
    load_model_on_startup()

    # Create default admin if not exists
    from backend.database import async_session
    from backend.models import ensure_default_admin
    async with async_session() as session:
        await ensure_default_admin(session)

    # Create default task time if not exists
    async with async_session() as session:
        from backend.models import ensure_default_task_time
        await ensure_default_task_time(session)

    yield
    # Shutdown: nothing to clean up


app = FastAPI(
    title="DAT System",
    description="Divergent Association Task - Measure divergent thinking",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from backend.routers import auth, dat, admin, export

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(dat.router, prefix="/api/dat", tags=["dat"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(export.router, prefix="/api/export", tags=["export"])

# Mount static files for frontend
frontend_path = Path(FRONTEND_DIR)
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    # Serve frontend HTML pages
    from fastapi.responses import FileResponse, RedirectResponse

    # Map routes to HTML files
    ROUTE_MAP = {
        "": "index.html",
        "login": "pages/login.html",
        "register": "pages/register.html",
        "introduction": "pages/introduction.html",
        "test": "pages/test.html",
        "results": "pages/results.html",
        "result": "pages/result-detail.html",
        "analysis": "pages/analysis.html",
        "admin": "pages/admin/dashboard.html",
        "admin/upload-user": "pages/admin/upload-user.html",
        "admin/task-config": "pages/admin/task-config.html",
    }

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend static files as fallback."""
        # Check route map first (strip query string in actual request)
        mapped = ROUTE_MAP.get(full_path)
        if mapped:
            mapped_path = frontend_path / mapped
            if mapped_path.exists():
                return FileResponse(mapped_path)

        # Try direct file path
        file_path = frontend_path / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)

        # Try with .html extension
        html_path = frontend_path / f"{full_path}.html"
        if html_path.exists():
            return FileResponse(html_path)

        # Try in pages/ directory
        pages_path = frontend_path / "pages" / f"{full_path}.html"
        if pages_path.exists():
            return FileResponse(pages_path)

        # Fallback to index.html
        index_path = frontend_path / "index.html"
        if index_path.exists():
            return FileResponse(index_path)

        return {"detail": "Not found"}, 404
