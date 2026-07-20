from core.kernel.base_service import BaseService
from core.kernel.event_bus import EventBus
from core.utils.logger import get_logger
from typing import Any, Optional

class WorldClock(BaseService):
    name = "world_clock"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)
        self.current_tick: int = 0
        self.is_running: bool = False
        self.event_bus: Optional[EventBus] = None

    def on_initialize(self, container: Any) -> None:
        # ดึง EventBus มาใช้ประกาศเวลา
        self.event_bus = container.get(EventBus)

    def on_start(self) -> None:
        self.logger.info("⏱️ [WorldClock] นาฬิกาโลกถูกปลุก (Tick = 0)...")
        self.is_running = True

    def on_stop(self) -> None:
        self.is_running = False
        self.logger.info("🛑 [WorldClock] นาฬิกาโลกหยุดเดิน...")

    def tick(self) -> None:
        """ขยับเวลา 1 Tick และส่ง Event บอกทั้งระบบ"""
        if not self.is_running:
            return

        self.current_tick += 1
        
        # ประกาศว่าเวลาเดินหน้าไปแล้ว (Priority = 50 เป็นเรื่องปกติ)
        if self.event_bus:
            self.event_bus.publish(
                event_type="TIME_TICK",
                payload={"tick": self.current_tick},
                priority=50 
            )