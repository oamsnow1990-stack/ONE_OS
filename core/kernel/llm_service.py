import numpy as np
import json
from typing import Any, Dict, Optional, List
from .base_service import BaseService, ServiceState
from .llm_interface import ILLMProvider 

class LLMService(BaseService, ILLMProvider):
    def __init__(self):
        super().__init__("llm_service")
        self.logger = None

    def on_initialize(self, container: Any) -> None:
        try:
            self.logger = container.get("system_logger")
        except Exception:
            print("⚠️ [LLMService] ไม่พบ SystemLogger ใน Container")

    def on_start(self) -> None:
        self.state = ServiceState.RUNNING
        if self.logger:
            self.logger.info("🚀 [LLMService] Start working...")

    def on_stop(self) -> None:
        self.state = ServiceState.STOPPED
        if self.logger:
            self.logger.info("🛑 [LLMService] Stopped.")

    def generate_plan(self, goal: str, context: Optional[Dict[str, Any]] = None) -> dict:
        """สร้างแผนงานโดยรับ Context เข้ามาช่วยตัดสินใจ"""
        if self.logger:
            self.logger.info(f"🧠 [LLM Planner] วิเคราะห์เป้าหมาย: '{goal}'")
        
        if context and self.logger:
            self.logger.info(f"🔍 [LLM Planner] กำลังใช้ Context: {list(context.keys())}")

        if "กล้อง" in goal or "ความปลอดภัย" in goal:
            return {
                "workflow_id": "auto_security_plan",
                "tasks": [{"id": "task_1", "agent": "SecurityAgent"}]
            }
        
        return {
            "workflow_id": "auto_default_plan",
            "tasks": [{"id": "task_1", "agent": "FileAgent"}]
        }

    def regenerate_plan(self, goal: str, error_log: str, context: Optional[Dict[str, Any]] = None) -> dict:
        """แก้ไขแผนงานโดยรับ Context และ Error Log"""
        if self.logger:
            self.logger.warning(f"🧠 [LLM Planner] แก้ไขแผนจาก Error: {error_log}")
        
        return {
            "workflow_id": "auto_recovery_plan",
            "tasks": [{"id": "recovery_task", "agent": "FileAgent"}]
        }

    def get_embedding(self, text: str) -> List[float]:
        """แปลงข้อความเป็น Vector สำหรับระบบ Memory"""
        # ปรับแก้ตรงนี้: เช็ค logger ก่อนใช้งาน
        if self.logger:
            self.logger.info(f"🧠 [LLM Embedding] กำลังสร้าง Vector")
        
        # ใช้ numpy สุ่มค่าสำหรับการทดสอบ (Mock)
        return np.random.rand(768).tolist()