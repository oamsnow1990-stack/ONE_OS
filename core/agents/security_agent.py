from core.agents.base import BaseAgent
from core.agents.models import ExecutionContext, AgentResult

class SecurityAgent(BaseAgent):
    @property
    def name(self) -> str: return "SecurityAgent"
    
    def execute(self, context: ExecutionContext) -> AgentResult:
        context.logger.info("👀 [SecurityAgent] กำลังตรวจสอบความปลอดภัยผ่านกล้อง...")
        try:
            # เรียก Tool ตรวจจับการเคลื่อนไหว
            status = context.call_tool("motion_detector")
            
            if status == "MOTION_DETECTED":
                context.logger.warning("🚨 [SecurityAgent] พบการเคลื่อนไหว! ผู้บุกรุก!!")
                return AgentResult(status="success", output={"alert": "intruder_detected"})
                
            context.logger.info("✅ [SecurityAgent] สถานการณ์ปกติ ไม่มีผู้บุกรุก")
            return AgentResult(status="success", output={"alert": "clear"})
            
        except Exception as e:
            context.logger.error(f"❌ [SecurityAgent] เกิดข้อผิดพลาดกับกล้อง: {str(e)}")
            return AgentResult(status="failed", error=str(e))

    def undo(self, context: ExecutionContext) -> AgentResult:
        context.logger.info("⏪ [SecurityAgent] Undo: ยกเลิกการเฝ้าระวัง (ไม่มีสถานะต้องล้างค่า)")
        return AgentResult(status="success", output={"msg": "Undo clear"})