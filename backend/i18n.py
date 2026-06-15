"""Backend i18n helper — lightweight, no external dependencies."""

from typing import Optional

from fastapi import Header

TRANSLATIONS = {
    # models_api.py response messages
    "model.ali_activated": {
        "zh": "阿里百炼 text-embedding-v4 已激活",
        "en": "Aliyun text-embedding-v4 activated",
    },
    "model.activated": {
        "zh": "{desc} 已激活",
        "en": "{desc} activated",
    },
    "model.custom_added": {
        "zh": "自定义模型 '{desc}' 已添加",
        "en": "Custom model '{desc}' added",
    },
    "model.cannot_delete_default": {
        "zh": "不能删除 Word2Vec 默认模型",
        "en": "Cannot remove the default Word2Vec model",
    },
    "model.not_found": {
        "zh": "模型不存在或无法删除",
        "en": "Model not found or cannot be removed",
    },
    "model.removed": {
        "zh": "模型 '{name}' 已移除",
        "en": "Model '{name}' removed",
    },
    "model.not_activated": {
        "zh": "模型 '{name}' 未激活或不存在",
        "en": "Model '{name}' not activated or does not exist",
    },
    "model.switched": {
        "zh": "已切换到 {desc}",
        "en": "Switched to {desc}",
    },
    # visualization.py
    "viz.distance_label": {
        "zh": "语义距离",
        "en": "Semantic Distance",
    },
    "viz.title": {
        "zh": "DAT 语义距离矩阵       得分: {score}",
        "en": "DAT Semantic Distance Matrix       Score: {score}",
    },
}


def t(key: str, lang: str = "zh", **kwargs) -> str:
    """Look up translation, fall back to zh if key missing in target lang."""
    entry = TRANSLATIONS.get(key, {})
    val = entry.get(lang) or entry.get("zh") or key
    if kwargs:
        val = val.format(**kwargs)
    return val


def get_request_lang(x_lang: Optional[str] = Header(None, alias="X-Lang")) -> str:
    """FastAPI dependency: extract language from X-Lang header."""
    if x_lang in ("zh", "en"):
        return x_lang
    return "zh"
