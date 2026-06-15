"""Model configuration router - manage embedding model selection and API keys."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import User
from backend.routers.auth import get_admin_user, get_current_user
from backend.services.embedding import (
    list_providers,
    set_active_provider,
    get_active_provider,
    register_provider,
    get_provider,
    AliQwenProvider,
)

router = APIRouter()


class SwitchModelRequest(BaseModel):
    model_name: str = Field(..., description="Model identifier to switch to")


class SetApiKeyRequest(BaseModel):
    model_name: str = Field(..., description="Model name")
    api_key: str = Field(..., description="API key")


class MessageResponse(BaseModel):
    message: str


@router.get("")
async def get_models():
    """List all available embedding models and their status."""
    providers = list_providers()
    active = get_active_provider()
    return {
        "models": providers,
        "active_model": active.model_name if active else None,
    }


@router.post("/switch", response_model=MessageResponse)
async def switch_model(
    data: SwitchModelRequest,
    current_user: User = Depends(get_current_user),
):
    """Switch the active embedding model."""
    success = set_active_provider(data.model_name)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{data.model_name}' not found or not configured",
        )
    provider = get_active_provider()
    return MessageResponse(
        message=f"Switched to {provider.description}"
    )


@router.post("/apikey", response_model=MessageResponse)
async def set_api_key(
    data: SetApiKeyRequest,
    current_user: User = Depends(get_admin_user),
):
    """Set or update an API key for a model (admin only)."""
    # Map model names to provider classes
    if data.model_name == "ali-qwen-v4":
        provider = get_provider("ali-qwen-v4")
        if provider is None:
            # Register it on first use
            provider = AliQwenProvider(api_key=data.api_key)
            register_provider(provider)
        else:
            provider.set_api_key(data.api_key)
        return MessageResponse(
            message=f"API key set for {provider.description}"
        )

    raise HTTPException(
        status_code=404,
        detail=f"Model '{data.model_name}' does not support API keys or is not available",
    )


@router.get("/cache-stats")
async def get_cache_stats(
    current_user: User = Depends(get_admin_user),
):
    """Get embedding cache statistics."""
    from backend.services.vector_cache import get_cache_stats
    return await get_cache_stats()
