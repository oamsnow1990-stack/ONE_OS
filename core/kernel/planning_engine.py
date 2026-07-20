from typing import Any, Optional, Dict # 🟢 แก้ไข: เพิ่ม Optional และ Dict เข้ามาครับ
from core.kernel.base_service import BaseService
from core.kernel.scenario_generator import ScenarioGenerator
from core.kernel.telemetry_service import TelemetryService

class PlanningEngine(BaseService):
    """ทำหน้าที่สร้างแผนงานและบันทึก telemetry"""
    name = "planning_engine"

    def __init__(self):
        super().__init__(self.name)
        self.generator: Optional[ScenarioGenerator] = None
        self.telemetry: Optional[TelemetryService] = None

    # 🟢 เพิ่มฟังก์ชันมาตรฐานตามที่ BaseService บังคับ
    def on_initialize(self, container: Any) -> None:
        self.generator = container.get(ScenarioGenerator)
        self.telemetry = container.get(TelemetryService)
        self.logger.info("PlanningEngine initialized.")

    def on_start(self) -> None:
        self.logger.info("PlanningEngine started.")

    def on_stop(self) -> None:
        self.logger.info("PlanningEngine stopped.")

    def execute_plan(self, strategy: str, world: Any, tick: int) -> Optional[str]:
        if not self.generator: return None
        candidates = self.generator.generate(strategy, world, count=1)
        if not candidates: return None
        return candidates[0].get('plan_id', 'UNKNOWN')

    def log_telemetry(self, tick: int, data: Dict):
        if self.telemetry:
            self.telemetry.render_control_room(tick, data)