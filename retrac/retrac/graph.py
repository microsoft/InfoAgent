from __future__ import annotations
from typing import Any, Dict, List, Optional, Literal
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from .config import ModelConfig
from .components import create_llm_node

class WebCycleResearchConfig(BaseModel):
    """Web cycle research configuration"""
    model: ModelConfig
    system_prompt: str
    continue_prompt: str
    summary_prompt: str
    max_cycles: int
    max_turns: int


class WebCycleResearchState(TypedDict, total=False):
    """Web cycle research graph state"""
    question: str
    output: Optional[str]
    messages: List[BaseMessage]
    tool_input: List[BaseMessage]
    cycle_histories: List[List[BaseMessage]]
    process_details: Dict[str, Any]
    error: list[str]


def _has_tool_calls(msg: BaseMessage) -> bool:
    return isinstance(msg, AIMessage) and bool(getattr(msg, "tool_calls", None))


def build_graph(cfg: dict) -> StateGraph:
    """Build web_cycle_research graph"""
    domain_cfg = WebCycleResearchConfig.model_validate(cfg)
    g = StateGraph(WebCycleResearchState)
    
    tool_node = ToolNode(domain_cfg.model.tools, messages_key="tool_input")
    llm_node = create_llm_node(
        model_cfg=domain_cfg.model,
    )
    
    def init_graph(state: WebCycleResearchState) -> Dict[str, Any]:
        patch: Dict[str, Any] = {}

        print(f"State: {state}")
        print(f"Domain config: {domain_cfg}")

        assert "question" in state and state["question"] is not None, "question is required"

        if "messages" not in state or not state.get("messages"):
            patch["messages"] = [
                SystemMessage(content=domain_cfg.system_prompt), 
                HumanMessage(content=state["question"])
            ]
        if "tool_input" not in state or state.get("tool_input") is None:
            patch["tool_input"] = []
        if "cycle_histories" not in state or state.get("cycle_histories") is None:
            patch["cycle_histories"] = []
        if "process_details" not in state or state.get("process_details") is None:
            patch["process_details"] = {'rollouts':[]}
        return patch

    async def end_cycle(state: WebCycleResearchState) -> WebCycleResearchState:
        """End a cycle using summary strategy"""
        summary_prompt = domain_cfg.summary_prompt
        summary = await llm_node(
            {'messages': state["messages"] + [HumanMessage(content=summary_prompt.format(input=state["question"]))]}
        )
        cycle_histories = state["cycle_histories"] + [[summary.get('messages', [None])[-1]]]

        if summary.get('messages'):
            state["messages"] = summary['messages']

        state["process_details"]['rollouts'].append({
            'messages': state["messages"],
        })
        
        return {"cycle_histories": cycle_histories, "process_details": state["process_details"], "messages": state["messages"]}
    
    def cycle_check(state: WebCycleResearchState) -> Literal["final", "start_cycle"]:
        if len(state["cycle_histories"]) >= domain_cfg.max_cycles:
            return "final"
        else:
            return "start_cycle"
    
    async def start_cycle(state: WebCycleResearchState) -> WebCycleResearchState:
        """Start a new cycle using summary strategy"""
        if len(state["cycle_histories"]) == 0:  # first cycle
            return {}
        
        messages = [
            SystemMessage(content=domain_cfg.system_prompt + "\nAlso there are some summary for the previous attempts you have made, you can use them to help you answer the question."), 
            HumanMessage(content=state["question"])
        ]
        contents_without_think = []
        for cycle_history in state["cycle_histories"]:
            contents = [message.text if isinstance(message, BaseMessage) else str(message.content) for message in cycle_history]
            # Remove reasoning part if exists
            contents_without_think += [content.split("</think>")[-1] if "</think>" in content else content for content in contents]
        
        last_summary = contents_without_think[-1]
        messages += [HumanMessage(content=domain_cfg.continue_prompt.format(last_summary=last_summary))]
        return {"messages": messages}

    def decide(state: WebCycleResearchState) -> Literal["tools", "end_cycle"]:
        """Decide next step: execute tools if tool calls exist, otherwise end cycle"""
        last: AIMessage = state["messages"][-1]
        dlast = dict(last)
        usage_metadata = dlast.get('usage_metadata', {})
        tool_calls_num = sum([1 if isinstance(message, ToolMessage) else 0 for message in state["messages"]])
        max_context = domain_cfg.model.max_context_length
        
        # Check if limits exceeded
        if (max_context is not None and usage_metadata.get("total_tokens", 0) > max_context) or tool_calls_num > domain_cfg.max_turns:
            return "end_cycle"

        # Default strategy: execute tools if tool calls exist, otherwise end cycle
        return "tools" if _has_tool_calls(last) else "end_cycle"

    def prep_tools(state: WebCycleResearchState) -> Dict[str, Any]:
        return {"tool_input": [state["messages"][-1]]}

    def merge_tool_output(state: WebCycleResearchState) -> Dict[str, Any]:
        tool_msgs = state.get("tool_input", [])
        if not tool_msgs:
            return {"tool_input": []}
        new_messages = list(state["messages"]) + list(tool_msgs)
        return {"messages": new_messages, "tool_input": []}

    def final(state: WebCycleResearchState) -> Dict[str, Any]:
        return {"output": state["messages"][-1].text}

    g.add_node("init_graph", init_graph)
    g.add_node("llm", llm_node)
    g.add_node("tools", tool_node)
    g.add_node("start_cycle", start_cycle)
    g.add_node("tools_prep", prep_tools)
    g.add_node("end_cycle", end_cycle)
    g.add_node("tools_merge", merge_tool_output)
    g.add_node("final", final)

    g.set_entry_point("init_graph")
    g.add_edge("init_graph", "start_cycle")
    g.add_edge("start_cycle", "llm")
    g.add_conditional_edges("llm", decide, {"tools": "tools_prep", "end_cycle": "end_cycle"})
    g.add_edge("tools_prep", "tools")
    g.add_edge("tools", "tools_merge")
    g.add_edge("tools_merge", "llm")
    g.add_conditional_edges("end_cycle", cycle_check, {"final": "final", "start_cycle": "start_cycle"})
    g.add_edge("final", END)

    return g
