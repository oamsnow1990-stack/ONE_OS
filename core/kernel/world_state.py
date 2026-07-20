from dataclasses import dataclass, field
from typing import Optional
import hashlib

@dataclass(frozen=True)
class WorldState:
    """
    Immutable representation of the world state.
    บังคับค่าเริ่มต้น ป้องกัน NoneType ตลอดการส่งต่อข้อมูล
    """
    weather: str = "sunny"
    energy: int = 0  # 0-100
    timestamp: float = field(default_factory=float)

    def __post_init__(self):
        # Data Validation: ป้องกันค่าที่ผิดปกติหลุดเข้าสู่ Registry
        object.__setattr__(self, 'energy', max(0, min(100, self.energy)))
        
        # ป้องกันค่า None ที่อาจหลุดรอดจาก Source
        if self.weather is None:
            object.__setattr__(self, 'weather', "unknown")

    def get_hash(self) -> str:
        """สร้าง Fingerprint ของสถานะโลก สำหรับการ Debug และ History"""
        state_str = f"{self.weather}:{self.energy}:{self.timestamp}"
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]