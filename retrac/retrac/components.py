from __future__ import annotations
import asyncio
import time
from typing import Any, Callable, Dict
import logging
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, AIMessage
from openai import BadRequestError
from langchain_core.messages.tool import ToolCall
from .config import ModelConfig

logger = logging.getLogger(__name__)

RETRY_ATTEMPTS = int(os.getenv("LLM_RETRY_ATTEMPTS", 5))
RETRY_INTERVAL = int(os.getenv("LLM_RETRY_INTERVAL", 10))
LLM_QPS_LIMIT = int(os.getenv("LLM_QPS_LIMIT", 40))


# QPS limiter
_async_qps_limit_states = {}

def async_qps_limiter(qps: int = LLM_QPS_LIMIT):
    """Async QPS limiter decorator"""
    def decorator(func):
        state_key = f"async_qps_limiter_{id(func)}"
        
        async def wrapper(*args, **kwargs):
            if state_key not in _async_qps_limit_states:
                _async_qps_limit_states[state_key] = {
                    "lock": asyncio.Lock(),
                    "call_times": [],
                    "qps": qps
                }
            
            state = _async_qps_limit_states[state_key]
            async with state["lock"]:
                current_time = time.monotonic()
                state["call_times"] = [
                    call_time for call_time in state["call_times"]
                    if current_time - call_time < 1.0
                ]
                
                if len(state["call_times"]) >= state["qps"]:
                    oldest_call = min(state["call_times"])
                    wait_time = 1.0 - (current_time - oldest_call)
                    if wait_time > 0:
                        await asyncio.sleep(wait_time)
                        current_time = time.monotonic()
                        state["call_times"] = [
                            call_time for call_time in state["call_times"]
                            if current_time - call_time < 1.0
                        ]
                
                state["call_times"].append(current_time)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def create_llm_node(
    model_cfg: ModelConfig,
    key: str = "messages",
) -> Callable[[Dict[str, Any]], Dict[str, Any]]:

    tools = model_cfg.tools
    api_type = model_cfg.api_type

    async def _llm_ainvoke(
        state: Dict[str, Any],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if key not in state:
            raise KeyError(f"State must contain '{key}' field")
        if not state.get(key):
            raise ValueError(f"State '{key}' field cannot be empty")

        msgs = state[key]
        if any(not isinstance(m, BaseMessage) for m in msgs):
            bad = next(type(m).__name__ for m in msgs if not isinstance(m, BaseMessage))
            raise TypeError(f"state['{key}'] must be List[BaseMessage], found {bad}")
        
        extra_body: Dict[str, Any] = {}
        if model_cfg.extra_body:
            extra_body.update(model_cfg.extra_body)
        if kwargs.get("extra_body"):
            extra_body.update(kwargs["extra_body"])
        if extra_body:
            kwargs["extra_body"] = extra_body

        use_responses_api = (api_type == "responses")
        
        llm = ChatOpenAI(
            model=model_cfg.model_name,
            base_url=model_cfg.base_url,
            api_key=model_cfg.api_key,
            temperature=model_cfg.temperature,
            top_p=model_cfg.top_p,
            timeout=model_cfg.timeout_s,
            use_responses_api=use_responses_api,
            use_previous_response_id=use_responses_api,
            **kwargs
        )
        if tools:
            llm = llm.bind_tools(tools)

        error = state.get("error", [])
        for llm_attempt_idx in range(RETRY_ATTEMPTS):
            try:
                resp: AIMessage = await llm.ainvoke(msgs)
                logger.debug("LLM invocation successful, response length: %s", len(resp.text or ""))

                if "<tool_call>finish</tool_call>" in resp.text:
                    logger.error("Finish tool call found in response: %s", resp.text)
                    finish_tool_call: ToolCall = ToolCall(name="finish", args={}, id=None)
                    resp.tool_calls.append(finish_tool_call)

                elif "</tool_call>" in resp.text:
                    logger.error("Tool call not parsed correctly, response: %s", resp.text, exc_info=True)
                    error.append("Tool call not parsed correctly")
                    continue

                return {key: msgs + [resp]}
            except Exception as e:
                msg = str(e)
                logger.error("LLM invocation failed: %s", msg, exc_info=True)
                error.append(f"LLM invocation failed on attempt [{llm_attempt_idx}/{RETRY_ATTEMPTS}] : {msg}")
                if isinstance(e, BadRequestError) and "context length" in msg:
                    break
                await asyncio.sleep(RETRY_INTERVAL)

        return {"error": error}

    async def llm_ainvoke(
        state: Dict[str, Any],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        return await _llm_ainvoke(state, **kwargs)

    @async_qps_limiter(qps=LLM_QPS_LIMIT)
    async def qps_limited_llm_ainvoke(
        state: Dict[str, Any],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        return await _llm_ainvoke(state, **kwargs)

    return llm_ainvoke if not model_cfg.enable_qps_limit else qps_limited_llm_ainvoke
