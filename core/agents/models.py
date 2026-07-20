from dataclasses import dataclass
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Skill:
    """โครงสร้างข้อมูลสำหรับเก็บทักษะ (Skill)"""
    name: str
    description: str
    preconditions: Dict[str, Any]  # เงื่อนไขที่จะใช้ Skill นี้ได้
    workflow_template: List[Dict[str, Any]] # ลำดับงาน (Tasks)
    usage_count: int = 0
    success_rate: float = 1.0

@dataclass
class AgentResult:
    """โครงสร้างข้อมูลผลลัพธ์จาก Agent"""
    status: str
    output: Dict[str, Any] = None
    error: Optional[str] = None
    latency: float = 0.0

@dataclass
class ExecutionContext:
    """Context สำหรับส่งให้ Agent ใช้งาน"""
    workflow_id: str
    task_id: str
    input_data: Dict[str, Any]
    variables: Dict[str, Any]
    logger: Any
    memory: Any          # 🟢 MemoryService
    tool_registry: Any   # 🟢 ToolRegistry

    # 🧠 Memory Helpers
    def save_memory(self, key: str, value: Any):
        """บันทึกข้อมูลลง Memory ของ Workflow ปัจจุบัน"""
        self.memory.set(self.workflow_id, key, value)

    def get_memory(self, key: str, default: Any = None) -> Any:
        """ดึงข้อมูลจาก Memory ของ Workflow ปัจจุบัน"""
        return self.memory.get(self.workflow_id, key, default)

    # 🛠️ Tool Helpers
    def call_tool(self, name: str, **kwargs) -> Any:
        """เรียกใช้ Tool ที่ลงทะเบียนไว้"""
        tool = self.tool_registry.get_tool(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")
        return tool.execute(**kwargs)