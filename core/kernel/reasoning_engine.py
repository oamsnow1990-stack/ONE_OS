from typing import Dict, Tuple, Optional, Any
from core.models.decision_models import MissionProfile
from core.kernel.base_service import BaseService

class ReasoningEngine(BaseService):
    """ทำหน้าที่ประมวลผล Strategy และ Decision Logic เพียงอย่างเดียว"""
    
    def __init__(self):
        # ต้องเรียก super().__init__ และส่งค่า name เข้าไปเพื่อให้ BaseService ทำงานได้ถูกต้อง
        super().__init__(name="reasoning_engine")

    # 🟢 ฟังก์ชันมาตรฐานตามที่ BaseService บังคับ (ประกาศเพียงรอบเดียว)
    def on_initialize(self, container: Any) -> None:
        self.logger.info("ReasoningEngine initialized.")

    def on_start(self) -> None:
        self.logger.info("ReasoningEngine started.")

    def on_stop(self) -> None:
        self.logger.info("ReasoningEngine stopped.")

    def select_strategy(self, resources: float, weather: str, confidence: float, 
                        thresholds: Dict[str, float], is_crisis: bool) -> Tuple[str, str]:
        if is_crisis:
            return "EMERGENCY_MODE", "CRITICAL: Crisis detected"
        if resources <= 0:
            return "SYSTEM_SLEEP", "CRITICAL: Energy 0%"
        if resources <= 20:
            return "ECO-MODE", f"WARNING: Low Battery ({resources}%)"
        if weather == "storm":
            return "SAFE_MODE", f"Context: {weather}"
        
        # แก้ไข Logic: เช็ค Confidence ต่ำกว่าเกณฑ์ก่อน
        if confidence < thresholds["SAFE"]:
            return "SAFE_MODE", f"Low Conf ({confidence:.2f})"
        
        # เช็ค Confidence สูงเกินเกณฑ์
        if confidence > thresholds["AGGRESSIVE"]:
            return "AGGRESSIVE_MODE", f"High Conf ({confidence:.2f})"
        
        # กรณีปกติ
        return "NORMAL_MODE", "Stable Operation"