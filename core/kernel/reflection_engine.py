from core.kernel.base_service import BaseService
from core.utils.logger import get_logger

class ReflectionEngine(BaseService):
    name = "reflection_engine"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)
        self.telemetry = None
        self.calibration_engine = None # เพิ่มตัวแปรนี้

    def on_initialize(self, container) -> None:
        self.telemetry = container.get("telemetry_service")
        # เพิ่มการดึง CalibrationEngine จาก Container
        self.calibration_engine = container.get("calibration_engine")

    def on_start(self) -> None:
        self.logger.info("🧠 [ReflectionEngine] ระบบวิเคราะห์พร้อมทำงาน")

    def on_stop(self) -> None:
        pass

    def reflect_on_mission(self, mission_id: str):
        """วิเคราะห์ประสิทธิภาพและสั่ง Calibration โดยอัตโนมัติ"""
        record = self.telemetry.get_record(mission_id)
        
        if not record:
            self.logger.warning(f"❌ ไม่พบ Record สำหรับภารกิจ {mission_id}")
            return

        sim = record.get("simulation_metrics", {})
        exe = record.get("execution_result") 

        self.logger.info(f"🧠 [Reflection] เริ่มวิเคราะห์ภารกิจ {mission_id}...")

        if not exe:
            self.logger.info(f"⏳ ภารกิจ {mission_id} ยังไม่มี Execution Result")
            return

        # 1. เปรียบเทียบ Latency
        pred_latency = sim.get("latency", 0)
        actual_latency = exe.get("actual_latency", 0)
        
        delta = abs(pred_latency - actual_latency)
        self.logger.info(f"📊 [Calibration] Latency Diff: {delta:.2f}s")
        
        # 2. Trigger Calibration (ส่งค่าไปปรับ Bias)
        if self.calibration_engine:
            self.calibration_engine.calibrate(actual_latency, pred_latency)
        else:
            self.logger.error("❌ ไม่พบ CalibrationEngine ในระบบ")
        
        # 3. สรุปผล
        if delta > 1.0:
            self.logger.warning("⚠️ [Reflection] Simulation ไม่แม่นยำเกินเกณฑ์")
        else:
            self.logger.info("✅ [Reflection] Simulation แม่นยำในระดับที่ยอมรับได้")