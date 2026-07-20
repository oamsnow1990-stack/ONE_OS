from typing import Any, Dict, Optional
from core.kernel.base_service import BaseService
from core.kernel.experience_store import ExperienceStore
from core.kernel.learning_engine import LearningEngine
from core.models.decision_models import MissionProfile

class KnowledgeLayer(BaseService):
    """รวม Memory และ Learning เข้าด้วยกันเพื่อให้ CDE เรียกใช้ง่ายขึ้น"""
    
    def __init__(self):
        super().__init__("knowledge_layer")
        self.experience: Optional[ExperienceStore] = None
        self.learning: Optional[LearningEngine] = None

    def on_initialize(self, container: Any) -> None:
        self.experience = container.get(ExperienceStore)
        self.learning = container.get(LearningEngine)
        self.logger.info("KnowledgeLayer initialized.")

    def on_start(self) -> None:
        self.logger.info("KnowledgeLayer started.")

    def on_stop(self) -> None:
        self.logger.info("KnowledgeLayer stopped.")

    def get_thresholds(self, mission: MissionProfile) -> Dict[str, float]:
        if self.learning:
            return self.learning.get_optimal_thresholds(mission)
        return {"SAFE": 0.60, "AGGRESSIVE": 0.85}

    def save_memory(self, data: Dict):
        if self.experience:
            self.experience.save(data)