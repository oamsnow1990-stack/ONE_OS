import asyncio
from core.kernel.learning_engine import LearningEngine
from core.kernel.reflection_engine import ReflectionEngine
from core.kernel.skill_registry_service import SkillRegistryService
from core.kernel.memory_service import MemoryService
from core.kernel.llm_service import LLMService

class MockLogger:
    def info(self, msg): print(f"Log: {msg}")

async def run_learning_test():
    print("--- 🧠 Starting Full Learning Loop Test ---")
    
    # 1. Setup Services
    llm = LLMService()
    mem = MemoryService(llm)
    reg = SkillRegistryService()
    learn = LearningEngine(reg, mem)
    ref = ReflectionEngine(mem, llm)
    
    # 2. Inject dependencies
    container = {"system_logger": MockLogger(), "learning_engine": learn}
    ref.on_initialize(container)
    learn.on_initialize(container)
    reg.on_initialize(container)
    
    workflow_id = "security_sweep"
    template = [{"agent": "SecurityAgent", "task": "sweep"}]
    result = {"status": "success", "template": template}
    
    # 3. รัน 3 รอบเพื่อให้ครบ Threshold ของ LearningEngine
    print(f"⚡ เริ่มรันการจำลองความสำเร็จ 3 ครั้ง...")
    for i in range(1, 4):
        print(f"\n⚡ รอบที่ {i}:")
        ref.reflect(workflow_id, result, "success")
        
    # 4. ตรวจสอบว่า Skill ถูกสร้างไหม
    skill = reg.find_skill(workflow_id)
    if skill:
        print(f"\n🎉 สำเร็จ! ระบบได้สร้าง Skill ใหม่ชื่อ: {skill.name}")
    else:
        print("\n❌ ยังไม่พบ Skill ใหม่")

if __name__ == "__main__":
    asyncio.run(run_learning_test())