from dataclasses import dataclass, field
from typing import Optional, Any
import hashlib
from datetime import datetime

@dataclass(frozen=True)
class WorldState:
    """
    Production-Grade WorldState Model
    รองรับการทำ Immutable และ Data Validation
    """
    weather: str = "sunny"
    energy: int = 0
    # เผื่อไว้สำหรับการขยายตัวของระบบในอนาคต
    resources: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # 1. ป้องกันค่า Null หรือ None ที่ไม่พึงประสงค์
        if self.weather is None:
            object.__setattr__(self, 'weather', "sunny")
        
        # 2. ทำ Data Sanitization (จำกัดค่า Energy 0-100)
        object.__setattr__(self, 'energy', max(0, min(100, self.energy)))

    def get_hash(self) -> str:
        """สร้าง Fingerprint สำหรับตรวจสอบสถานะโลก (Registry)"""
        state_str = f"{self.weather}|{self.energy}|{self.timestamp.isoformat()}"
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]