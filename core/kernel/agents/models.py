from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time

@dataclass
class AgentResult:
    """มาตรฐานผลลัพธ์ที่ทุก Agent ต้องตอบกลับ (Step 5)"""
    status: str            # "success", "failed", "error"
    output: Any            # ผลลัพธ์จากการทำงาน
    metadata: Dict = field(default_factory=dict)
    cost: float = 0.0      # ค่าใช้จ่าย (เช่น API Cost)
    latency: float = 0.0   # เวลาที่ใช้ประมวลผล
    error: Optional[str] = None

@dataclass
class ExecutionContext:
    """ข้อมูลแวดล้อมทั้งหมดที่ Agent จำเป็นต้องรู้ (Step 4)"""
    workflow_id: str
    task_id: str
    input_data: Any
    variables: Dict[str, Any]
    
    # Dependencies (DI จะเป็นคนยัดไส้เข้ามาให้)
    logger: Any = None
    memory: Any = None
    tools: Any = None  # ToolRegistry (อนาคต)
    runtime: Any = None