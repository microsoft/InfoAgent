from __future__ import annotations
import os
from typing import Any, Dict, List, Sequence
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Literal
from dotenv import load_dotenv
load_dotenv()

print("="*100)
print(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE')}")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
print("="*100)

# Tool registry
_TOOL_REGISTRY: Dict[str, object] = {}

def register_tool(name: str, tool: object):
    """Register a tool"""
    _TOOL_REGISTRY[name] = tool

def resolve_tools(names: Sequence[str]) -> List[object]:
    """Resolve tool names to tool objects"""
    tools = []
    for n in names:
        if n not in _TOOL_REGISTRY:
            raise KeyError(f"Tool '{n}' not registered. Available: {sorted(_TOOL_REGISTRY)}")
        tools.append(_TOOL_REGISTRY[n])
    return tools


class ModelConfig(BaseModel):
    """Model configuration"""
    model_config = {"extra": "forbid"}
    
    model_name: str = Field(...)
    base_url: str = Field(default=os.getenv("OPENAI_API_BASE"), description="model base url")
    api_key: str = Field(default=os.getenv("OPENAI_API_KEY"), description="model api key")
    temperature: float | None = None
    timeout_s: int | None = None
    top_p: float | None = Field(default=None, description="top_p for sampling")
    max_context_length: int | None = None
    enable_qps_limit: bool = False
    tools: List[Any] = []
    api_type: Literal["responses", "chat_completion"] = 'chat_completion'
    extra_body: Dict[str, Any] = Field(
        default_factory=dict,
        description="extra body params for LLM request",
    )
    repatch_reasoning_template: str | None = None
    
    @field_validator("tools")
    @classmethod
    def _resolve_tools(cls, v: List[Any]) -> List[Any] | None:
        if isinstance(v, list) and v and isinstance(v[0], str):
            return resolve_tools(v)
        return v
