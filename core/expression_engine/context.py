from dataclasses import dataclass, field
from typing import Dict, Any
# 1. เพิ่มการ Import เข้ามาครับ
from core.expression_engine.registry.variable_registry import VariableRegistry

@dataclass
class ExecutionContext:
    runtime: Dict[str, Any] = field(default_factory=dict)
    workflow: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, Any] = field(default_factory=dict)
    
    # 2. เปลี่ยนจาก Dict เป็น VariableRegistry
    # field(default_factory=VariableRegistry) จะสร้างตัวแปรใหม่ให้โดยอัตโนมัติ
    variables: VariableRegistry = field(default_factory=VariableRegistry)