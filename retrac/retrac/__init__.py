from .config import register_tool
from .tools import search, visit

register_tool("search", search)
register_tool("visit", visit)

__all__ = ["register_tool"]
