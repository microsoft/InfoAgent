from email import message
import os
from typing import Any, Dict, Tuple
import asyncio
import yaml
from retrac.graph import build_graph
from typing import AsyncIterator
import argparse
from langchain_core.messages import BaseMessage,convert_to_openai_messages

def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

async def graph_execution(config_path: str, question: str, **kwargs: Any) -> Dict[str, Any]:
    recursion_limit = int(os.getenv("RECURSION_LIMIT", "10000"))
    run_config = {"recursion_limit": recursion_limit}
    cfg = load_config(config_path)
    graph = build_graph(cfg)
    initial_state = {"question": question}
    app = graph.compile()
    state = await app.ainvoke(initial_state, config=run_config, **kwargs)
    return state

async def stream_graph_execution(
    graph,
    initial_state: Dict[str, Any],
    **kwargs: Any,
) -> AsyncIterator[Dict[str, Any]]:
    compiled_graph = graph.compile()

    recursion_limit = int(os.getenv("RECURSION_LIMIT", "10000"))
    run_config = {"recursion_limit": recursion_limit}

    state = initial_state.copy()

    async for event in compiled_graph.astream(state, config=run_config, **kwargs):
        yield event
        # same as your code: merge node outputs into state
        for node_name, node_output in event.items():
            if node_output is not None:
                state.update(node_output)


async def run_streaming(config_path: str, question: str) -> AsyncIterator[Dict[str, Any]]:
    cfg = load_config(config_path)
    graph = build_graph(cfg)
    initial_state = {"question": question}
    async for event in stream_graph_execution(graph, initial_state):
        yield event


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run Re-TRAC graph (streaming or non-streaming).")
    parser.add_argument(
        "--config",
        type=str,
        default="retrac/deep_research.yaml",
        help="Path to YAML config file.",
    )
    parser.add_argument(
        "--question",
        type=str,
        default="What is the capital of France?",
        help="Input question for the agent.",
    )
    parser.add_argument(
        "--non-streaming",
        action="store_true",
        help="Enable non-streaming output.",
    )

    args = parser.parse_args()

    if not args.non_streaming:
        message_ids = set()
        merged_state = {}
        async for event in run_streaming(args.config, args.question):
            for node_name, node_output in event.items():
                if node_output is not None:
                    merged_state.update(node_output)
            messages: list[BaseMessage] = merged_state.get("messages", [])
            for msg in messages:
                if hash(str(msg)) in message_ids: continue
                print(convert_to_openai_messages(msg))
                message_ids.add(hash(str(msg)))
        print(merged_state["output"])
            
    else:
        final_state = await graph_execution(args.config, args.question)
        print(final_state.get("output", ""))

if __name__ == "__main__":
    asyncio.run(main())