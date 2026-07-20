from dataclasses import dataclass, field
from typing import Dict, Any, List
import time

@dataclass(frozen=True) # Immutable: เมื่อเป็นข้อมูลโลก ห้ามแก้ตรงๆ ต้องสร้างเวอร์ชันใหม่เท่านั้น
class WorldState:
    version: int = 0
    timestamp: float = field(default_factory=time.time)
    
    # --- Schema: Digital Twin ---
    # โลกภายนอกและสถานะอุปกรณ์
    environment: Dict[str, Any] = field(default_factory=lambda: {"temp": 30, "light": "day", "weather": "clear"})
    user: Dict[str, Any] = field(default_factory=lambda: {"location": "home", "status": "active"})
    devices: Dict[str, Any] = field(default_factory=lambda: {"door": "closed", "camera": "online"})
    
    # ระบบ AI และงาน
    agents: Dict[str, Any] = field(default_factory=dict)
    goals: List[Dict[str, Any]] = field(default_factory=list)
    
    # ข้อมูลวิเคราะห์และคาดการณ์
    threats: List[Dict[str, Any]] = field(default_factory=list)
    resources: Dict[str, Any] = field(default_factory=lambda: {"cpu": 0, "ram": 0, "battery": 100})
    history: List[str] = field(default_factory=list)
    predictions: List[Dict[str, Any]] = field(default_factory=list)

    # Note: ในส่วนของ Dataclass เราจะไม่ใส่ logic การ return ค่าใดๆ
    # logic การจัดการโลก (Manager) จะไปอยู่ที่ WorldStateManager ครับ