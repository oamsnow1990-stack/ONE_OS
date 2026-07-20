import random
from typing import Any, Dict, List
from core.kernel.base_service import BaseService
from core.models.world_state import WorldState
from core.utils.logger import get_logger

class ScenarioGenerator(BaseService):
    name = "scenario_generator"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)

    def on_initialize(self, container: Any) -> None:
        self.logger.info("ScenarioGenerator initialized.")

    def on_start(self) -> None:
        self.logger.info("ScenarioGenerator started.")

    def on_stop(self) -> None:
        self.logger.info("ScenarioGenerator stopped.")

    def generate(self, strategy: str, world: WorldState, count: int = 3) -> List[Dict[str, Any]]:
        """ผลิตแผนทางเลือกตาม Strategy และสถานะโลกปัจจุบัน"""
        
        self.logger.info(f"⚙️ [Generator] รับคำสั่งผลิตแผนฉุกเฉิน {count} รูปแบบสำหรับกลยุทธ์: {strategy}")
        candidates = []
        
        for i in range(1, count + 1):
            # สร้าง ID แผนให้ไม่ซ้ำกันตาม Tick ของโลก
            plan_id = f"PLAN_{strategy}_TICK{world.tick}_V{i}"
            
            candidates.append({
                "plan_id": plan_id,
                "strategy": strategy,
                "description": f"แผนรับมือฉบับที่ {i} สำหรับสถานการณ์ {strategy}"
            })
            
        return candidates