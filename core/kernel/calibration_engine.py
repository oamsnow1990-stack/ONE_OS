from core.kernel.base_service import BaseService
from core.utils.logger import get_logger

class CalibrationEngine(BaseService):
    name = "calibration_engine"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)
        self.simulation = None
        self.learning_rate = 0.5 # ปรับให้สูงขึ้นเพื่อให้เห็นผลการเรียนรู้ชัดเจนใน Test

    def on_initialize(self, container) -> None:
        self.simulation = container.get("simulation_engine")

    def on_start(self) -> None:
        self.logger.info("⚖️ [CalibrationEngine] ระบบปรับจูนพร้อมทำงาน")

    def on_stop(self) -> None:
        pass

    def calibrate(self, actual_latency: float, predicted_latency: float):
        """คำนวณ Error และปรับ Bias ของ Simulator"""
        error = actual_latency - predicted_latency
        adjustment = error * self.learning_rate
        
        new_bias = self.simulation.latency_bias + adjustment
        
        self.logger.info(f"📊 [Calibration] Error: {error:.2f} | ปรับ Bias: {self.simulation.latency_bias:.2f} -> {new_bias:.2f}")
        
        # สั่งอัปเดต Simulator
        self.simulation.apply_calibration(new_bias)