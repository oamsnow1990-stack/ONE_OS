import time
import random
from core.kernel.base_service import BaseService
from core.utils.logger import get_logger

class ExecutorService(BaseService):
    name = "executor_service"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)
        self.telemetry = None

    def on_initialize(self, container) -> None:
        self.telemetry = container.get("telemetry_service")

    # --- เพิ่ม Method ที่ขาดไปเพื่อให้รันได้ ---
    def on_start(self) -> None:
        self.logger.info("⚙️ [ExecutorService] พร้อมรับคำสั่งรันงาน")

    def on_stop(self) -> None:
        pass

    def execute_mission(self, mission_id: str, plan_id: str):
        """รันงานจริงและส่งผลลัพธ์กลับสู่ Telemetry"""
        self.logger.info(f"⚙️ [Executor] เริ่มรันภารกิจ {mission_id} (แผน: {plan_id})...")
        
        # จำลองการทำงานจริง
        time.sleep(0.5) 
        actual_latency = round(random.uniform(0.1, 1.5), 2)
        
        result = {
            "success": True,
            "actual_latency": actual_latency,
            "executed_at": time.time()
        }
        
        self.logger.info(f"🏁 [Executor] ภารกิจเสร็จสิ้น | Latency จริง: {actual_latency}s")
        
        # ส่งผลลัพธ์กลับ Telemetry
        if self.telemetry:
            self.telemetry.update_record(mission_id, result)
        else:
            self.logger.error("❌ ไม่พบ Telemetry Service สำหรับบันทึกผลลัพธ์")