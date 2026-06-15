"""Model configuration router."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.models import User
from backend.routers.auth import get_admin_user, get_current_user
from backend.services.embedding import (
    list_providers, set_active_provider, get_active_provider,
    register_provider, get_provider, unregister_provider,
    AliQwenProvider, register_api_provider, register_custom_provider,
    GenericOpenAIProvider,
)

router = APIRouter()


class SwitchModelRequest(BaseModel):
    model_name: str


class SetApiKeyRequest(BaseModel):
    model_name: str
    api_key: str = Field(..., min_length=1)


class CustomProviderRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="显示名称")
    base_url: str = Field(..., min_length=1, description="API 基础 URL（如 https://api.openai.com/v1）")
    model_id: str = Field(..., min_length=1, description="模型 ID（如 text-embedding-3-small）")
    dimension: int = Field(..., gt=0, le=8192, description="向量维度")
    api_key: str = Field(..., min_length=1)


class DeleteProviderRequest(BaseModel):
    model_name: str


class MessageResponse(BaseModel):
    message: str


# Built-in API providers (no key stored, user provides key each time)
BUILTIN_TEMPLATES = [
    {
        "kind": "openai-3-small",
        "name": "openai-3-small",
        "description": "OpenAI text-embedding-3-small (1536维)",
        "dimension": 1536,
        "requires_key": True,
    },
    {
        "kind": "openai-3-large",
        "name": "openai-3-large",
        "description": "OpenAI text-embedding-3-large (3072维)",
        "dimension": 3072,
        "requires_key": True,
    },
    {
        "kind": "siliconflow-bge",
        "name": "siliconflow-bge",
        "description": "硅基流动 BGE-large-zh-v1.5 (1024维)",
        "dimension": 1024,
        "requires_key": True,
    },
    {
        "kind": "siliconflow-qwen3",
        "name": "siliconflow-qwen3",
        "description": "硅基流动 Qwen3-Embedding-4B (2560维)",
        "dimension": 2560,
        "requires_key": True,
    },
    {
        "kind": "ali-qwen-v4",
        "name": "ali-qwen-v4",
        "description": "阿里百炼 text-embedding-v4 (1024维)",
        "dimension": 1024,
        "requires_key": True,
    },
]


@router.get("")
async def get_models():
    """List active providers and available templates."""
    providers = list_providers()
    active = get_active_provider()
    return {
        "models": providers,
        "active_model": active.model_name if active else None,
        "templates": BUILTIN_TEMPLATES,
    }


@router.get("/templates")
async def get_templates():
    """List built-in model templates that can be activated."""
    return {"templates": BUILTIN_TEMPLATES}


@router.post("/activate", response_model=MessageResponse)
async def activate_model(
    data: SetApiKeyRequest,
    current_user: User = Depends(get_admin_user),
):
    """Activate a built-in model with API key."""
    # Check if it's ali-qwen (non-standard API)
    if data.model_name == "ali-qwen-v4":
        existing = get_provider("ali-qwen-v4")
        if existing:
            existing.set_api_key(data.api_key)
        else:
            register_provider(AliQwenProvider(api_key=data.api_key))
        return MessageResponse(message="阿里百炼 text-embedding-v4 已激活")

    # Try built-in OpenAPI-compatible providers
    provider = register_api_provider(data.model_name, data.api_key)
    if provider is None:
        raise HTTPException(status_code=404, detail=f"未知模型: {data.model_name}")

    return MessageResponse(message=f"{provider.description} 已激活")


@router.post("/custom", response_model=MessageResponse)
async def add_custom_provider(
    data: CustomProviderRequest,
    current_user: User = Depends(get_admin_user),
):
    """Add a custom OpenAI-compatible embedding provider."""
    name_slug = data.name.lower().replace(" ", "-")
    provider = register_custom_provider(
        name=name_slug,
        url=data.base_url,
        model_id=data.model_id,
        dimension=data.dimension,
        api_key=data.api_key,
    )
    return MessageResponse(message=f"自定义模型 '{provider.description}' 已添加")


@router.post("/delete", response_model=MessageResponse)
async def delete_provider(
    data: DeleteProviderRequest,
    current_user: User = Depends(get_admin_user),
):
    """Remove a non-built-in provider."""
    if data.model_name == "word2vec":
        raise HTTPException(status_code=400, detail="不能删除 Word2Vec 默认模型")
    ok = unregister_provider(data.model_name)
    if not ok:
        raise HTTPException(status_code=404, detail="模型不存在或无法删除")
    return MessageResponse(message=f"模型 '{data.model_name}' 已移除")


@router.post("/switch", response_model=MessageResponse)
async def switch_model(
    data: SwitchModelRequest,
    current_user: User = Depends(get_current_user),
):
    """Switch active embedding model."""
    success = set_active_provider(data.model_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"模型 '{data.model_name}' 未激活或不存在")
    p = get_active_provider()
    return MessageResponse(message=f"已切换到 {p.description}")


@router.get("/cache-stats")
async def get_cache_stats(current_user: User = Depends(get_admin_user)):
    from backend.services.vector_cache import get_cache_stats
    return await get_cache_stats()
