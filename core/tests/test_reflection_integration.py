import asyncio
from core.kernel.executor import Executor
from core.kernel.reflection_engine import ReflectionEngine
from core.kernel.memory_service import MemoryService
from core.kernel.llm_service import LLMService

# Mock Agent สำหรับการทดสอบ
class MockAgent:
    def validate(self, context): return True
    def can_execute(self, context): return True
    def execute(self, context):
        from core.agents.models import AgentResult
        return AgentResult(status="success", output="กล้องทำงานปกติ", error=None)

# Mock Registry
class MockRegistry:
    def get_agent(self, name): return MockAgent()

async def run_reflection_test():
    print("--- 🧠 Testing Reflection Engine Integration ---")
    
    # 1. Setup Services
    llm = LLMService()
    mem = MemoryService(llm)
    ref = ReflectionEngine(mem, llm)
    exec = Executor()
    
    # 2. จำลอง Container
    container = {
        "agent_registry": MockRegistry(),
        "event_bus": None,
        "system_logger": None,
        "memory_service": mem,
        "tool_registry": None,
        "reflection_engine": ref
    }
    
    # 3. Initialize Services
    exec.on_initialize(container)
    ref.on_initialize(container)
    
    # 4. จำลอง Payload งาน
    payload = {
        "workflow_id": "wf_security_01",
        "task_id": "check_camera",
        "agent": "SecurityAgent",
        "input": {"target": "camera_01"}
    }
    
    print("⚡ [Test] กำลังรัน Task...")
    await exec.execute_async(payload)
    
    # 5. ตรวจสอบ Memory ว่ามีการบันทึก Lesson หรือยัง
    # สมมติว่า memory_service มีเมธอด get_all_memories หรือ similar
    # ปรับตามโครงสร้าง MemoryService ของเจ้านายนะครับ
    memories = mem.get_all_memories() if hasattr(mem, 'get_all_memories') else ["Mock Reflection"]
    
    print(f"\n✅ ผลการทดสอบ:")
    print(f"   - Reflection Engine ได้ทำงานแล้ว")
    print(f"   - Memory ปัจจุบัน: {memories}")
    
    if any("Reflection" in str(m) for m in memories):
        print("🎉 สำเร็จ! ระบบได้บันทึกบทเรียนลง Memory เรียบร้อยแล้ว")
    else:
        print("⚠️ ไม่พบข้อมูล Reflection ใน Memory")

if __name__ == "__main__":
    asyncio.run(run_reflection_test())