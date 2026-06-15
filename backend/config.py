"""Application configuration."""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "frontend"
MODELS_DIR = BASE_DIR / "models"
STATIC_DIR = BASE_DIR / "frontend"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
(STATIC_DIR / "assets" / "img").mkdir(parents=True, exist_ok=True)

# Database
DATABASE_URL = f"sqlite+aiosqlite:///{DATA_DIR}/dat.db"
DATABASE_SYNC_URL = f"sqlite:///{DATA_DIR}/dat.db"

# JWT
SECRET_KEY = os.environ.get("DAT_SECRET_KEY", "dat-system-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# Default admin
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "123456"

# Model
WORD2VEC_MODEL_PATH = MODELS_DIR / "w2v.wv"
FONT_PATH = MODELS_DIR / "SIMHEI.TTF"

# Server
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

# DAT task
DEFAULT_LIMITED_TIME = 240  # 4 minutes in seconds
