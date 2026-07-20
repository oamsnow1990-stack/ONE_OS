from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime
import uuid

# 1. นิยามประเภท Event แยกออกมา (เปลี่ยนชื่อเป็น EventType เพื่อไม่ให้ซ้ำ)
class EventType(Enum):
    SYSTEM_BOOT = "SYSTEM_BOOT"
    SYSTEM_READY = "SYSTEM_READY"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_FINISHED = "workflow.finished"
    TASK_STARTED = "task.started"
    TASK_FINISHED = "task.finished"
    # 🟢 เพิ่ม State Change Event สำหรับ State Machine
    STATE_CHANGED = "state_changed" 

# 2. Dataclass สำหรับบรรจุข้อมูล
@dataclass
class SystemEvent:
    type: EventType  # อ้างอิง Enum EventType ที่ถูกต้อง
    source: str
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "type": self.type.value, # ดึงค่า string จาก Enum
            "source": self.source,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "parent_id": self.parent_id,
        }

    def __repr__(self) -> str:
        return f"SystemEvent(type={self.type.value}, source={self.source})"