from core.kernel.context_engine import ContextEngine
from core.kernel.memory_service import MemoryService
from core.kernel.world_model_service import WorldModelService
from core.kernel.llm_service import LLMService
from core.kernel.goal_manager_service import GoalManagerService 

def run_integration_test():
    print("--- 🔍 Testing Context Integration ---")
    
    # 1. Setup Services
    llm = LLMService()
    mem = MemoryService(llm)
    wm = WorldModelService()
    gm = GoalManagerService()
    
    # 1.1 จำลองการ Initialize (ใส่ Container เปล่าๆ เข้าไป)
    # ถ้าในอนาคตมี config หรือ logger จะได้ผ่านจุดนี้ไปได้
    class MockContainer:
        def get(self, key): return None
    container = MockContainer()
    
    gm.on_initialize(container)
    
    # 2. ตั้ง Goal และใส่ข้อมูลจำลอง
    gm.set_goal("Make the house safe for the day") # <--- สำคัญมาก: เพิ่มตรงนี้ครับ
    mem.remember("User prefers notification via LINE.")
    wm.add_entity("camera_01", "sensor", {"capability": "motion"})
    
    # 3. สร้าง Context Engine
    ctx = ContextEngine(mem, wm, gm)
    
    # 4. ลองดึง Context
    context_data = ctx.get_planner_context("wf_001", "เช็คกล้อง")
    
    print("\n✅ Context Retrieved:")
    print(f"   - Active Goal: {context_data['goal_status']['active_goal']}")
    print(f"   - Memory: {context_data['recent_experience']}")
    print(f"   - World Context: {context_data['world_context']}")
    
    # 5. ลองส่งให้ LLM
    plan = llm.generate_plan("เช็คกล้อง", context=context_data)
    print(f"\n✅ Plan Generated: {plan}")

if __name__ == "__main__":
    run_integration_test()