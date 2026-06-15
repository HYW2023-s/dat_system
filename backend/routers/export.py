"""Data export router - CSV and Excel export."""

import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Header
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.database import get_db
from backend.models import DatTest, User
from backend.routers.auth import decode_token

router = APIRouter()


async def verify_export_auth(
    token: Optional[str] = Query(None),
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Authenticate via URL token or Bearer header."""
    token_str = None
    if token:
        token_str = token
    elif authorization and authorization.startswith("Bearer "):
        token_str = authorization[7:]

    if not token_str:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = decode_token(token_str)
        username = payload.get("sub")
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user and user.is_superuser:
            return user
    except Exception:
        pass
    raise HTTPException(status_code=401, detail="Not authenticated")


@router.get("/csv")
async def export_csv(
    user: User = Depends(verify_export_auth),
    db: AsyncSession = Depends(get_db),
):
    """Export all DAT test records as CSV."""
    result = await db.execute(select(DatTest).order_by(DatTest.create_time.desc()))
    records = result.scalars().all()

    output = io.StringIO()
    output.write("ID,Username,Create Time,"
                 "Word1,Word2,Word3,Word4,Word5,Word6,Word7,Word8,Word9,Word10,"
                 "DAT Score,Effective Words,Spend Time,Limited Time\n")

    for r in records:
        create_time = r.create_time.isoformat() if r.create_time else ""
        output.write(
            f'"{r.id}","{r.username}","{create_time}",'
            f'"{r.word1}","{r.word2}","{r.word3}","{r.word4}","{r.word5}",'
            f'"{r.word6}","{r.word7}","{r.word8}","{r.word9}","{r.word10}",'
            f'{r.dat_score},{r.effective_num},"{r.spend_time}","{r.limited_time}"\n'
        )

    output.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=dat_export_{timestamp}.csv"},
    )


@router.get("/xlsx")
async def export_xlsx(
    user: User = Depends(verify_export_auth),
    db: AsyncSession = Depends(get_db),
):
    """Export all DAT test records as Excel."""
    import openpyxl

    result = await db.execute(select(DatTest).order_by(DatTest.create_time.desc()))
    records = result.scalars().all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "DAT Results"

    headers = [
        "ID", "Username", "Create Time",
        "Word1", "Word2", "Word3", "Word4", "Word5",
        "Word6", "Word7", "Word8", "Word9", "Word10",
        "DAT Score", "Effective Words", "Spend Time", "Limited Time",
    ]
    ws.append(headers)

    for r in records:
        ws.append([
            r.id, r.username, str(r.create_time) if r.create_time else "",
            r.word1, r.word2, r.word3, r.word4, r.word5,
            r.word6, r.word7, r.word8, r.word9, r.word10,
            r.dat_score, r.effective_num, r.spend_time, r.limited_time,
        ])

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=dat_export_{timestamp}.xlsx"},
    )
