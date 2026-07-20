from dataclasses import dataclass, field
from typing import Any, Dict
import time
import itertools

# สร้างตัวนับ (Counter) สำหรับใช้เรียงลำดับเมื่อ Priority เท่ากัน
_counter = itertools.count()

@dataclass(order=True)
class SystemEvent:
    # --- 1. ฟิลด์บังคับ (Non-default arguments) ต้องอยู่ด้านบน ---
    priority: int 
    event_type: str = field(compare=False)
    
    # --- 2. ฟิลด์ทางเลือก (Default arguments) ต้องอยู่ด้านล่าง ---
    # ใช้เรียงลำดับเมื่อ priority เท่ากัน (Tie-breaker)
    sequence: int = field(default_factory=lambda: next(_counter))
    
    payload: Dict[str, Any] = field(default_factory=dict, compare=False)
    timestamp: float = field(default_factory=time.time, compare=False)