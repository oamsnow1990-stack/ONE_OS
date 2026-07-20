from typing import Any, Dict, Optional
from core.kernel.base_service import BaseService
from core.kernel.experience_store import ExperienceStore
from core.kernel.confidence_engine import ConfidenceEngine
from core.kernel.simulation_engine import SimulationEngine

class LearningEngine(BaseService):
    name = "learning_engine"

    def __init__(self):
        super().__init__(self.name)
        self.experience: Optional[ExperienceStore] = None
        self.conf: Optional[ConfidenceEngine] = None
        self.sim: Optional[SimulationEngine] = None

    def on_initialize(self, container: Any) -> None:
        self.experience = container.get(ExperienceStore)
        self.conf = container.get(ConfidenceEngine)
        self.sim = container.get(SimulationEngine)
        self.logger.info(f"{self.__class__.__name__} initialized.")

    def on_start(self) -> None:
        self.logger.info("🎓 [LearningEngine] ระบบปรับจูนสมอง พร้อมทำงาน")
        self.logger.info(f"{self.__class__.__name__} started.")

    def on_stop(self) -> None:
        self.logger.info(f"{self.__class__.__name__} stopped.")

    def run_calibration(self):
        """วิเคราะห์ประวัติและปรับ Weights พร้อม Adaptive Difficulty"""
        if not self.experience or not self.conf: 
            return
        
        success_rates = self.experience.get_recent_success_rates(limit=50)
        if not success_rates: 
            return
        
        avg_success = sum(success_rates) / len(success_rates)
        
        # 1. Adaptive Difficulty: ถ้า AI เก่งเกินไป ให้เพิ่มความยาก
        if self.sim and avg_success > 0.8:
            new_diff = self.sim.difficulty_factor + 0.1
            self.sim.set_difficulty(new_diff)
        
        # 2. ปรับ Confidence Weights
        if avg_success < 0.5:
            # ระบบเริ่มรวน: เน้น Error Detection
            self.conf.update_weights({
                "history": 0.40,
                "prediction_error": 0.30 
            })
        else:
            # ระบบเสถียร: ผ่อนคลาย
            self.conf.update_weights({
                "history": 0.60,
                "prediction_error": 0.10
            })