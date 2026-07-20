from typing import Dict, List, Any
from core.kernel.base_service import BaseService
from .base import BaseTool

class ToolRegistry(BaseService):
    def __init__(self):
        super().__init__("tool_registry")
        self._tools: Dict[str, BaseTool] = {}

    def on_initialize(self, container: Any) -> None:
        pass

    def on_start(self) -> None:
        pass

    def on_stop(self) -> None:
        self._tools.clear()

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> BaseTool:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, str]]:
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]