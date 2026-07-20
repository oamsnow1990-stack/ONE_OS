from typing import Dict, Any
from core.kernel.base_service import BaseService
from core.utils.logger import get_logger

class ConfidenceEngine(BaseService):
    name = "confidence_engine"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)
        # ค่า Default Weights
        self.weights = {'history': 0.6, 'context': 0.2, 'novelty': 0.1, 'prediction_error': 0.1}

    def on_initialize(self, container: Any) -> None:
        pass

    def on_start(self) -> None:
        self.logger.info("🛡️ [ConfidenceEngine] ระบบพร้อมทำงาน (Dynamic Weighting: Active)")

    def update_weights(self, new_weights: Dict[str, float]):
        self.weights.update(new_weights)
        self.logger.info(f"⚖️ [ConfidenceEngine] Weights อัปเดตใหม่: {self.weights}")

    def get_contextual_confidence(self, mission: Any, world: Any, last_error: float = 0.0) -> float:
        weather = world.weather.get("condition", "sunny")
        
        # 🟢 Dynamic Weight Shift Logic
        # ถ้าเจอ Storm: ลด Hist เพิ่ม Ctx ทันที เพื่อให้ AI ฟังเสียงพายุมากกว่าอดีต
        current_weights = self.weights.copy()
        
        if weather == "storm":
            current_weights = {
                'history': 0.30,          # ลดน้ำหนักอดีตลง
                'context': 0.50,          # เพิ่มน้ำหนัก Context ให้ความสำคัญกับพายุสูงสุด
                'novelty': 0.10,
                'prediction_error': 0.10
            }
        
        # คำนวณ Confidence ตาม Weights ที่ปรับแล้ว
        # (สมมติโมเดลการคำนวณเบื้องต้น)
        base_conf = 0.9
        error_penalty = last_error * current_weights['prediction_error']
        history_val = 0.9 * current_weights['history']
        context_val = (0.5 if weather == "storm" else 0.9) * current_weights['context']
        
        final_confidence = (history_val + context_val + (0.9 * current_weights['novelty'])) - error_penalty
        
        return round(min(1.0, max(0.0, final_confidence)), 2)

    def on_stop(self) -> None:
        pass