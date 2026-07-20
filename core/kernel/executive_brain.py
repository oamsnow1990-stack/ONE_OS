from typing import List, Any
from core.kernel.base_service import BaseService
from core.utils.logger import get_logger 
from core.models.decision_models import DecisionRecord

class ExecutiveBrain(BaseService):
    name = "executive_brain"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)
        self._processed = 0
        self.simulation = None
        self.decision = None
        self.telemetry = None

    def on_initialize(self, container) -> None:
        self.simulation = container.get("simulation_engine")
        self.decision = container.get("decision_engine")
        self.telemetry = container.get("telemetry_service")

    def on_start(self) -> None:
        self.logger.info("👑 [ExecutiveBrain] CEO ของระบบพร้อมตรวจดูคิวงานแล้ว")

    def on_stop(self) -> None:
        self.logger.info("👑 [ExecutiveBrain] CEO ออฟไลน์")

    def run_mission(self, mission_id: str, profile: Any, scenarios: List[Any], world_state: Any) -> DecisionRecord:
        """รันภารกิจ Think-Before-Act พร้อม Context โลกจริง"""
        
        # 1. Simulation Phase
        evaluation_results = []
        for s in scenarios:
            try:
                res = self.simulation.predict(s, world_state)
                evaluation_results.append(res)
            except Exception as e:
                scenario_id = getattr(s, 'id', 'unknown')
                self.logger.error(f"❌ Simulation Error for {scenario_id}: {e}")

        if not evaluation_results:
            raise RuntimeError("Mission Failed: No valid simulation results.")

        # 2. Decision Phase (ส่ง world_state.version เพิ่มเติมเข้าไป)
        try:
            decision_record = self.decision.decide(
                mission_id, 
                evaluation_results, 
                profile, 
                world_state.version
            )
        except Exception as e:
            self.logger.error(f"❌ Decision Engine Error: {e}")
            raise

        # 3. Telemetry Phase
        try:
            self.telemetry.record(decision_record)
        except Exception as e:
            self.logger.warning(f"⚠️ Telemetry Logging Failed: {e}")

        self._processed += 1
        return decision_record