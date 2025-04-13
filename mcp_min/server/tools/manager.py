from __future__ import annotations as _annotations

from collections.abc import Callable
from typing import Any

from ..exceptions import ToolError
from .base import Tool


class ToolManager:
    """Manages FastMCP tools."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def get_tool(self, name: str) -> Tool | None:
        """Get tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> list[Tool]:
        """List all registered tools."""
        return list(self._tools.values())

    def add_tool(
        self,
        fn: Callable[..., Any],
        name: str | None = None,
        description: str | None = None,
    ) -> Tool:
        """Add a tool to the server."""
        tool = Tool.from_function(fn, name=name, description=description)
        existing = self._tools.get(tool.name)
        if existing:
            return existing
        self._tools[tool.name] = tool
        return tool

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
        context: Any = None,
    ) -> Any:
        """Call a tool by name with arguments."""
        tool = self.get_tool(name)
        if not tool:
            raise ToolError(f"Unknown tool: {name}")

        return await tool.run(arguments, context=context)
