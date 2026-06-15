"""Admin router - user management, data analysis, task configuration."""

import io
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import User, DatTest, TaskTime
from backend.routers.auth import get_admin_user
from passlib.hash import bcrypt

router = APIRouter()


# --- Schemas ---

class TaskTimeUpdate(BaseModel):
    limited_time: int = Field(..., ge=10, le=3600)


class PasswordReset(BaseModel):
    username: str
    new_password: str = Field(..., min_length=6, max_length=128)


class MessageResponse(BaseModel):
    message: str


# --- Routes ---

@router.put("/task-time", response_model=MessageResponse)
async def update_task_time(
    data: TaskTimeUpdate,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Update DAT test time limit."""
    result = await db.execute(
        select(TaskTime).where(TaskTime.task_name == "DAT")
    )
    task_time = result.scalar_one_or_none()

    if task_time:
        task_time.limited_time = data.limited_time
    else:
        task_time = TaskTime(task_name="DAT", limited_time=data.limited_time)
        db.add(task_time)

    await db.commit()
    return MessageResponse(message=f"Time limit updated to {data.limited_time}s")


@router.post("/reset-password", response_model=MessageResponse)
async def reset_user_password(
    data: PasswordReset,
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Reset a user's password (admin only)."""
    result = await db.execute(
        select(User).where(User.username == data.username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = bcrypt.hash(data.new_password)
    await db.commit()

    return MessageResponse(
        message=f"Password for '{data.username}' reset successfully"
    )


@router.post("/upload-users")
async def upload_users(
    file: UploadFile = File(...),
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Batch upload users from an Excel file."""
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload .xlsx or .xls",
        )

    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))

    required_cols = ["username", "password"]
    if not all(col in df.columns for col in required_cols):
        raise HTTPException(
            status_code=400,
            detail="Excel file must contain 'username' and 'password' columns",
        )

    created = []
    skipped = []

    for _, row in df.iterrows():
        username = str(row["username"]).strip()
        password = str(row["password"]).strip()

        result = await db.execute(
            select(User).where(User.username == username)
        )
        existing = result.scalar_one_or_none()

        if existing:
            skipped.append(username)
        else:
            user = User(
                username=username,
                password_hash=bcrypt.hash(password),
                is_superuser=False,
            )
            db.add(user)
            created.append(username)

    await db.commit()

    msg = f"Uploaded {len(created)} users"
    if skipped:
        msg += f". Skipped {len(skipped)} existing users: {', '.join(skipped)}"

    return {"message": msg, "created": created, "skipped": skipped}


@router.get("/analysis")
async def get_analysis_data(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Get descriptive statistics and chart data."""
    result = await db.execute(
        select(DatTest.dat_score).where(DatTest.username != "")
    )
    scores = [row[0] for row in result.all()]

    if not scores:
        return {
            "stats": {"max": 0, "min": 0, "avg": 0, "median": 0,
                      "ptp": 0, "var": 0, "std": 0, "count": 0},
            "distribution": {},
        }

    scores_arr = np.array(scores, dtype=float)

    stats = {
        "max": int(np.max(scores_arr)),
        "min": int(np.min(scores_arr)),
        "avg": round(float(np.mean(scores_arr)), 2),
        "median": round(float(np.median(scores_arr)), 2),
        "ptp": round(float(np.ptp(scores_arr)), 2),
        "var": round(float(np.var(scores_arr)), 2),
        "std": round(float(np.std(scores_arr)), 2),
        "count": len(scores),
    }

    # Distribution for bar chart
    ranges = [("<30", 0, 30), ("30-40", 30, 40), ("40-50", 40, 50),
              ("50-60", 50, 60), ("60-70", 60, 70), (">70", 70, 200)]

    distribution = {}
    for label, lo, hi in ranges:
        count = int(np.sum((scores_arr >= lo) & (scores_arr < hi)))
        distribution[label] = count

    # Boxplot data
    boxplot_data = {
        "scores": sorted([int(s) for s in scores]),
    }

    # KDE / density data: gaussian kernel density estimate
    from scipy.stats import gaussian_kde
    kde_x = np.linspace(max(0, scores_arr.min() - 10), min(100, scores_arr.max() + 10), 200)
    try:
        kde = gaussian_kde(scores_arr)
        kde_y = kde(kde_x).tolist()
    except Exception:
        kde_y = [0] * len(kde_x)

    density_data = {
        "x": kde_x.tolist(),
        "y": kde_y,
    }

    # Cumulative distribution (for ECDF)
    sorted_scores = np.sort(scores_arr)
    cumulative_y = (np.arange(1, len(sorted_scores) + 1) / len(sorted_scores)).tolist()
    cumulative_data = {
        "x": sorted_scores.tolist(),
        "y": cumulative_y,
    }

    # Scatter data: (index, score) to show distribution
    scatter_data = {
        "x": list(range(len(scores))),
        "y": sorted([int(s) for s in scores]),
    }

    return {
        "stats": stats,
        "distribution": distribution,
        "boxplot_data": boxplot_data,
        "density_data": density_data,
        "cumulative_data": cumulative_data,
        "scatter_data": scatter_data,
    }


@router.get("/search")
async def search_records(
    q: str = "",
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Search DAT test records by username."""
    query = select(DatTest).order_by(DatTest.create_time.desc())
    if q:
        query = query.where(DatTest.username.contains(q))

    result = await db.execute(query.limit(100))
    records = result.scalars().all()

    return [
        {
            "id": r.id,
            "username": r.username,
            "create_time": r.create_time.isoformat() if r.create_time else "",
            "dat_score": r.dat_score,
            "effective_num": r.effective_num,
        }
        for r in records
    ]


@router.get("/export")
async def export_data(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Export all DAT records (alias: redirect to CSV export)."""
    from backend.routers.export import export_csv
    return await export_csv(admin, db)


@router.get("/users")
async def list_users(
    admin: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all users."""
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "is_superuser": u.is_superuser,
            "created_at": u.created_at.isoformat() if u.created_at else "",
        }
        for u in users
    ]
