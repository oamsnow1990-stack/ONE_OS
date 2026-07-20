from typing import Dict, Optional, Any
from threading import Lock
from core.kernel.base_service import BaseService
from core.models.world_state import WorldState
from core.utils.logger import get_logger

class WorldStateRegistry(BaseService):
    def __init__(self):
        super().__init__("world_state_registry")
        self.logger = get_logger(self.name)
        self._registry: Dict[str, WorldState] = {}
        self._current_version: Optional[str] = None
        self._lock = Lock()

    # --- บังคับ Implementation ตาม BaseService ---
    def on_initialize(self, container: Any) -> None:
        self.logger.debug("Initializing WorldStateRegistry...")

    def on_start(self) -> None:
        self.logger.info("WorldStateRegistry started.")

    def on_stop(self) -> None:
        self.logger.info("WorldStateRegistry stopped.")

    # --- Business Logic ---
    def register_state(self, state: WorldState) -> str:
        with self._lock:
            # ใช้ getattr หรือ get_hash ของ state (ตรวจสอบว่า WorldState มีเมธอดนี้)
            version_id = getattr(state, "get_hash", lambda: str(id(state)))()
            self._registry[version_id] = state
            self._current_version = version_id
            self.logger.debug(f"💾 [Registry] State registered: {version_id}")
            return version_id

    def get_current_state(self) -> Optional[WorldState]:
        with self._lock:
            if not self._current_version or self._current_version not in self._registry:
                return None
            return self._registry[self._current_version]

    def get_state(self, version_id: Optional[str] = None) -> Optional[WorldState]:
        """
        เมธอดใหม่: ใช้สำหรับดึง State ตาม ID หรือดึงล่าสุดหาก ID เป็น None
        """
        with self._lock:
            # ถ้าไม่มีการระบุ ID ให้ส่งคืน State ล่าสุด
            if not version_id:
                return self.get_current_state()
            
            # ส่งคืน State ที่ระบุ ถ้าไม่มีจะคืนค่า None (ป้องกัน Crash)
            return self._registry.get(version_id)

    def get_state_by_id(self, version_id: str) -> Optional[WorldState]:
        """
        Alias สำหรับดึงข้อมูลตาม ID โดยเฉพาะ
        """
        return self.get_state(version_id)