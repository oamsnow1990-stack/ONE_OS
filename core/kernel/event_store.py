import json
from typing import Any
from .base_service import BaseService
from .events import SystemEvent

class EventStore(BaseService):
    """ระบบ Audit Log: บันทึกทุกความเคลื่อนไหวลงไฟล์"""
    def __init__(self, log_file: str = "events.log"):
        super().__init__("event_store")
        self.log_file = log_file
        self.event_bus = None
        self.logger = None

    def on_initialize(self, container: Any) -> None:
        self.event_bus = container.get("event_bus")
        self.logger = container.get("logger")
        
        # 🟢 ติดตั้งเครื่องดักฟังทุก Event ในระบบ
        if hasattr(self.event_bus, "subscribe_all"):
            self.event_bus.subscribe_all(self._log_event)

    def on_start(self) -> None:
        self.logger.info(f"Event Store Service started. Logging to: {self.log_file}")
        # เขียนเส้นคั่นเวลาเริ่มระบบใหม่เพื่อให้ดู Log ง่ายขึ้น
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({"type": "system.store_started", "message": "--- NEW SESSION ---"}) + "\n")

    def on_stop(self) -> None:
        self.logger.info("Event Store Service stopped.")

    def _log_event(self, event: Any):
        """รับ Event แล้วเขียนลงไฟล์แบบ JSON Line"""
        try:
            # ตรวจสอบว่าเป็น SystemEvent หรือไม่ จะได้ดึงข้อมูลได้ถูกต้อง
            if isinstance(event, SystemEvent):
                log_data = event.to_dict()
            elif isinstance(event, dict):
                log_data = event
            else:
                log_data = {"raw_event": str(event)}

            # ใช้โหมด 'a' (append) เพื่อต่อท้ายไฟล์ไปเรื่อยๆ
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_data) + "\n")
        except Exception as e:
            if self.logger:
                self.logger.error(f"EventStore failed to write log: {e}")