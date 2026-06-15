"""DAT test router - core test functionality."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import User, DatTest, AnswerLog, SpendTime, TaskTime
from backend.routers.auth import get_current_user
from backend.services.dat_calculator import compute_dat_score
from backend.utils.visualization import generate_heatmap

router = APIRouter()


# --- Schemas ---

class DatSubmitRequest(BaseModel):
    word1: str = Field(default="", max_length=32)
    word2: str = Field(default="", max_length=32)
    word3: str = Field(default="", max_length=32)
    word4: str = Field(default="", max_length=32)
    word5: str = Field(default="", max_length=32)
    word6: str = Field(default="", max_length=32)
    word7: str = Field(default="", max_length=32)
    word8: str = Field(default="", max_length=32)
    word9: str = Field(default="", max_length=32)
    word10: str = Field(default="", max_length=32)
    spend_time: str = Field(default="")
    limited_time: str = Field(default="")


class DatResultResponse(BaseModel):
    dat_score: int
    effective_num: int
    picture_path: str
    percentage: float


# --- Routes ---

@router.get("/test-config")
@router.get("/test")  # Alias
async def get_test_config(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get test page configuration (limited time, etc.)."""
    # Log answer start
    log = AnswerLog(username=current_user.username, statue=0)
    db.add(log)
    await db.commit()

    # Get limited time
    result = await db.execute(
        select(TaskTime).where(TaskTime.task_name == "DAT")
    )
    task_time = result.scalar_one_or_none()
    limited_time = task_time.limited_time if task_time else 240

    return {
        "limited_time": limited_time,
        "username": current_user.username,
    }


@router.post("/calculate")
async def calculate_dat(
    data: DatSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit words and calculate DAT score."""
    words_dict = {
        "word1": data.word1, "word2": data.word2, "word3": data.word3,
        "word4": data.word4, "word5": data.word5, "word6": data.word6,
        "word7": data.word7, "word8": data.word8, "word9": data.word9,
        "word10": data.word10,
    }

    # Compute DAT score
    result = await compute_dat_score(words_dict)

    # Generate heatmap
    valid_words = result["valid_words"]
    dat_score = result["dat_score"]
    pic_path = generate_heatmap(valid_words, dat_score)

    # Calculate percentage (how many users scored lower)
    count_result = await db.execute(
        select(func.count(DatTest.id))
    )
    total = count_result.scalar() or 1  # Avoid division by zero

    lower_result = await db.execute(
        select(func.count(DatTest.id)).where(DatTest.dat_score < dat_score)
    )
    lower_count = lower_result.scalar() or 0
    percentage = round((lower_count / max(total, 1)) * 100, 1)

    # Save record
    record = DatTest(
        username=current_user.username,
        word1=data.word1, word2=data.word2, word3=data.word3,
        word4=data.word4, word5=data.word5, word6=data.word6,
        word7=data.word7, word8=data.word8, word9=data.word9,
        word10=data.word10,
        dat_score=dat_score,
        effective_num=result["effective_num"],
        picture_path=pic_path,
        spend_time=data.spend_time,
        limited_time=data.limited_time,
    )
    db.add(record)
    await db.commit()

    return {
        "dat_score": dat_score,
        "effective_num": result["effective_num"],
        "picture_path": pic_path,
        "percentage": percentage,
        "provider_name": result.get("provider_name", "unknown"),
    }


@router.get("/results")
async def get_results(
    page: int = 1,
    page_size: int = 20,
    search: str = "",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated test results."""
    query = select(DatTest)

    # Non-admin users can only see their own results
    if not current_user.is_superuser:
        query = query.where(DatTest.username == current_user.username)

    if search:
        if current_user.is_superuser:
            query = query.where(DatTest.username.contains(search))
        else:
            query = query.where(
                DatTest.username == current_user.username,
                DatTest.username.contains(search),
            )

    # Order by create_time desc
    query = query.order_by(DatTest.create_time.desc())

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Paginate
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    records = result.scalars().all()

    items = []
    for r in records:
        items.append({
            "id": r.id,
            "username": r.username,
            "create_time": r.create_time.isoformat() if r.create_time else "",
            "dat_score": r.dat_score,
            "effective_num": r.effective_num,
            "spend_time": r.spend_time,
            "word1": r.word1, "word2": r.word2, "word3": r.word3,
            "word4": r.word4, "word5": r.word5,
        })

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total + page_size - 1) // page_size),
        "show_search_box": current_user.is_superuser,
    }


@router.get("/result/{record_id}")
async def get_result_detail(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a single DAT result detail."""
    query = select(DatTest).where(DatTest.id == record_id)
    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    # Non-admin can only see their own records
    if not current_user.is_superuser and record.username != current_user.username:
        raise HTTPException(status_code=403, detail="Access denied")

    # Calculate percentage
    count_result = await db.execute(select(func.count(DatTest.id)))
    total = count_result.scalar() or 1

    lower_result = await db.execute(
        select(func.count(DatTest.id)).where(DatTest.dat_score < record.dat_score)
    )
    lower_count = lower_result.scalar() or 0
    percentage = round((lower_count / max(total, 1)) * 100, 1)

    words = [
        record.word1, record.word2, record.word3, record.word4, record.word5,
        record.word6, record.word7, record.word8, record.word9, record.word10,
    ]

    return {
        "id": record.id,
        "username": record.username,
        "create_time": record.create_time.isoformat() if record.create_time else "",
        "words": words,
        "dat_score": record.dat_score,
        "effective_num": record.effective_num,
        "picture_path": record.picture_path,
        "spend_time": record.spend_time,
        "limited_time": record.limited_time,
        "percentage": percentage,
    }


@router.get("/result/{record_id}/heatmap-data")
async def get_heatmap_data(
    record_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get heatmap matrix data for a record (for ECharts frontend rendering)."""
    query = select(DatTest).where(DatTest.id == record_id)
    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")

    if not current_user.is_superuser and record.username != current_user.username:
        raise HTTPException(status_code=403, detail="Access denied")

    # Collect valid words
    all_words = [
        record.word1, record.word2, record.word3, record.word4, record.word5,
        record.word6, record.word7, record.word8, record.word9, record.word10,
    ]
    non_empty = [w for w in all_words if w]

    from backend.services.embedding import get_provider
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity

    w2v = get_provider("word2vec")
    if w2v is None or w2v.model is None:
        return {"words": non_empty, "matrix": []}

    # Filter words in vocabulary
    valid_words = [w for w in non_empty if w in w2v.model]

    if len(valid_words) < 2:
        return {"words": valid_words, "matrix": []}

    # Compute distance matrix
    vectors = np.stack([w2v.model[w] for w in valid_words])
    sim_matrix = cosine_similarity(vectors)
    dist_matrix = (1 - sim_matrix) * 100

    # Build lower-triangle matrix for ECharts heatmap
    # ECharts uses [x, y, value] format
    heatmap_data = []
    n = len(valid_words)
    for i in range(n):
        for j in range(i + 1, n):
            heatmap_data.append([j, i, round(float(dist_matrix[i, j]), 1)])

    return {
        "words": valid_words,
        "matrix": heatmap_data,
    }


@router.get("/limited-time")
async def get_limited_time(db: AsyncSession = Depends(get_db)):
    """Get the current DAT test time limit."""
    result = await db.execute(
        select(TaskTime).where(TaskTime.task_name == "DAT")
    )
    task_time = result.scalar_one_or_none()
    return {
        "limited_time": task_time.limited_time if task_time else 240,
    }


@router.post("/save-spend-time")
async def save_spend_time(
    spend_time: str = "",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Save the time a user spent on the test."""
    record = SpendTime(username=current_user.username, spend_time=spend_time)
    db.add(record)
    await db.commit()
    return {"message": "OK"}
