from typing import Any, Optional # 🟢 1. เพิ่ม Import ที่ขาดหายไป
from core.kernel.base_service import BaseService
from core.kernel.event_bus import EventBus
from core.kernel.reasoning_engine import ReasoningEngine
from core.kernel.planning_engine import PlanningEngine
from core.kernel.knowledge_layer import KnowledgeLayer
from core.kernel.world_state_registry import WorldStateRegistry
from core.kernel.confidence_engine import ConfidenceEngine
from core.models.events import SystemEvent
from .event_bus import safe_event_handler

class CognitiveDecisionEngine(BaseService):
    """
    CDE v4.0: The Orchestrator
    หน้าที่: เป็นเพียง Traffic Controller ของระบบเท่านั้น (Decoupled Architecture)
    """

    def __init__(self):
        # 🟢 2. แก้ไขการเรียก super().__init__ ให้ตรงมาตรฐานโปรเจกต์
        super().__init__("cognitive_decision_engine")
        self.reasoning: Optional[ReasoningEngine] = None
        self.planning: Optional[PlanningEngine] = None
        self.knowledge: Optional[KnowledgeLayer] = None
        self.registry: Optional[WorldStateRegistry] = None
        self.conf: Optional[ConfidenceEngine] = None

    def on_initialize(self, container: Any) -> None:
        self.reasoning = container.get(ReasoningEngine)
        self.planning = container.get(PlanningEngine)
        self.knowledge = container.get(KnowledgeLayer)
        self.registry = container.get(WorldStateRegistry)
        self.conf = container.get(ConfidenceEngine)
        
        event_bus = container.get(EventBus)
        if event_bus:
            event_bus.subscribe("WORLD_STATE_UPDATED", self._on_world_updated)

    # 🟢 3. เพิ่มฟังก์ชันที่ระบบบังคับให้ครบ (Abstract methods)
    def on_start(self):
        self.logger.info("CognitiveDecisionEngine started.")

    def on_stop(self):
        self.logger.info("CognitiveDecisionEngine stopped.")

    # 🟢 4. เพิ่มฟังก์ชันที่ขาดไป ป้องกันการเกิด AttributeError
    def _get_active_mission(self) -> str:
        """คืนค่าภารกิจหลักที่ทำงานอยู่ ณ ปัจจุบัน"""
        return "DEFAULT_MISSION"

    @safe_event_handler
    def _on_world_updated(self, event: SystemEvent) -> None:
        payload = event.payload
        world = self.registry.get_state(payload.get("version_id")) if payload.get("version_id") else self.registry.get_current_state()
        if not world: 
            return

        # 1. Reasoning (Decision)
        mission = self._get_active_mission()
        thresholds = self.knowledge.get_thresholds(mission)
        confidence = self.conf.get_contextual_confidence(mission, world)
        
        strategy, reason = self.reasoning.select_strategy(
            world.resources.get("amount", 0),
            world.weather.get("condition", "unknown"),
            confidence, 
            thresholds, 
            world.resources.get("is_crisis", False)
        )
        
        # 2. Planning (Execution)
        plan_id = self.planning.execute_plan(strategy, world, payload.get("tick", 0))
        
        # 3. Knowledge & Telemetry
        self.knowledge.save_memory({"strategy": strategy, "plan_id": plan_id})
        self.planning.log_telemetry(payload.get("tick", 0), {"strategy": strategy, "plan_id": plan_id})