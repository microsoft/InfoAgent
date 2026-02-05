import json
import asyncio
import aiohttp
import os
from typing import Dict
from pydantic import BaseModel, Field
from langchain.tools import tool
import http.client
import openai

import dotenv
dotenv.load_dotenv()


TOOL_SERVER_URL = None # for custom tool server
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")

MODEL_FOR_VISIT_SUMMARIZE = os.getenv("MODEL_FOR_VISIT_SUMMARIZE")
BASE_URL_FOR_VISIT_SUMMARIZE = os.getenv("BASE_URL_FOR_VISIT_SUMMARIZE")
API_KEY_FOR_VISIT_SUMMARIZE = os.getenv("API_KEY_FOR_VISIT_SUMMARIZE")

print("="*100)
print(f"SERPER_API_KEY: {SERPER_API_KEY}")
print(f"JINA_API_KEY: {JINA_API_KEY}")
print(f"MODEL_FOR_VISIT_SUMMARIZE: {MODEL_FOR_VISIT_SUMMARIZE}")
print(f"BASE_URL_FOR_VISIT_SUMMARIZE: {BASE_URL_FOR_VISIT_SUMMARIZE}")
print(f"API_KEY_FOR_VISIT_SUMMARIZE: {API_KEY_FOR_VISIT_SUMMARIZE}")
print("="*100)

SUMMARIZE_PROMPT = """Please process the following webpage content and user goal to extract relevant
information:
## **Webpage Content**
{webpage_content}
## **User Goal**
{goal}
## **Task Guidelines**
1. **Content Scanning for Rationale**: Locate the specific sections/data directly
related to the user's goal within the webpage content
2. **Key Extraction for Evidence**: Identify and extract the most relevant
information from the content, output the full original context as far as possible
3. **Summary Output for Summary**: Organize into a concise paragraph with logical
flow, prioritizing clarity
**Final Output Format using JSON format has "rational", "evidence", "summary"
fields**
"""

class SearchInput(BaseModel):
    query: list[str] = Field(description="The list of search query strings")

class VisitInput(BaseModel):
    url: list[str] = Field(description="List of URLs to visit")
    goal: str = Field(description="The goal or question to answer from the URLs")

async def serper_search(query: str) -> Dict:
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "https://google.serper.dev/search",
            json={"q": query},
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
        )
        response.raise_for_status()
        result = await response.json()
    return {"items": result["organic"]}  

async def jina_browse(url: str) -> Dict:
    url = f"https://r.jina.ai/{url}"
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}"
    }
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, headers=headers)
        response.raise_for_status()
        result = await response.text()
    return result

async def jina_visit(urls: list[str], goal: str) -> Dict:
    webpage_content = "\n".join(await asyncio.gather(*[jina_browse(url) for url in urls]))
    prompt = SUMMARIZE_PROMPT.format(webpage_content=webpage_content, goal=goal)
    client = openai.AsyncOpenAI(
        base_url=BASE_URL_FOR_VISIT_SUMMARIZE,
        api_key=API_KEY_FOR_VISIT_SUMMARIZE,
    )
    response = await client.chat.completions.create(
        model=MODEL_FOR_VISIT_SUMMARIZE,
        messages=[{"role": "user", "content": prompt}],
    )
    return {"semanticDocument": f"The useful information in {urls} for user goal {goal} as follows: {response.choices[0].message.content}"}

async def _search(query: str) -> Dict:
    payload = {
        "query": query,
        "provider": 'google',
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{TOOL_SERVER_URL}/search",
            json=payload,
        )
        if response.status == 429:
            print(f"[429] query={query}")
        response.raise_for_status()
        result = await response.json()
    return result


async def _visit(urls: list[str], goal: str) -> Dict:
    payload = {"urls": urls, "goal": goal, "style": 'tongyi'}
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f"{TOOL_SERVER_URL}/visit",
            json=payload,
        )
        response.raise_for_status()
        result = await response.json()
    return result


@tool("search", args_schema=SearchInput, description="Search the web for information about a query using google search.")
async def search(query: list[str]) -> str:
    """Search the web for information about a query using google search."""

    search_func = _search if TOOL_SERVER_URL else serper_search
    batch_results = await asyncio.gather(*[search_func(q) for q in query], return_exceptions=True)

    success_results = [result for result in batch_results if not isinstance(result, BaseException)]
    if len(success_results) == 0:
        return f"Failed to get items for queries {query}. All queries failed."

    outputs = []

    for batch_result in success_results:
        search_results = []
        if 'items' not in batch_result:
            search_results.append(f"Failed to get items for query {query}. Returned result: {batch_result}")
        for item in batch_result['items']:
            item.pop("error_message", None)
            search_results.append(item)
        outputs.append(json.dumps(search_results, ensure_ascii=False))
    
    return '\n'.join(outputs)


@tool("visit", args_schema=VisitInput, description="Visit multiple URLs and extract information based on a goal.")
async def visit(url: list[str], goal: str) -> str:
    """Visit multiple URLs and extract information based on a goal."""
    visit_func = _visit if TOOL_SERVER_URL else jina_visit
    result = await visit_func(url, goal)
    return result['semanticDocument']


if __name__ == "__main__":
    async def test_search_tools(query: list[str]) -> str:
        result = await search.ainvoke({"query": query})
        print(result)

    asyncio.run(test_search_tools(["Elden Ring","Golden Tree"]))

    async def test_visit_tools(urls: list[str], goal: str) -> str:
        result = await visit.ainvoke({"url": urls, "goal": goal})
        print(result)

    asyncio.run(test_visit_tools(["https://en.wikipedia.org/wiki/Elden_Ring"], "Who is the main character of Elden Ring?"))

   