import asyncio
from unittest.mock import Mock

from core.agents.planner_agent import PlannerAgent
from core.agents.models import ExecutionContext
from core.kernel.learning_engine import LearningEngine
from core.kernel.reflection_engine import ReflectionEngine
from core.kernel.skill_registry_service import SkillRegistryService
from core.kernel.memory_service import MemoryService
from core.kernel.llm_service import LLMService
from core.kernel.context_engine import ContextEngine
from core.kernel.persistence import PersistenceService
from core.kernel.executive_brain import ExecutiveBrain
from core.kernel.goal_manager_service import GoalManagerService
from core.kernel.event_bus import EventBusService # 🟢 1. Import Event Bus

class MockRuntime:
    async def execute(self, plan): pass

class MockLogger:
    def info(self, msg): print(f"Log: {msg}")
    def warning(self, msg): print(f"Warn: {msg}")
    def error(self, msg): print(f"Err: {msg}")
    def debug(self, msg): pass

def run_full_system_test(): 
    print("\n--- 🌐 Starting Full System Integration Test (Autonomous Mode) ---\n")
    
    # 1. Setup Services
    llm = LLMService()
    mem = MemoryService(llm)
    persistence = PersistenceService(data_dir="test_data") 
    reg = SkillRegistryService()
    event_bus = EventBusService() # 🟢 2. สร้าง Event Bus
    mock_world_model = Mock()
    goal_manager = GoalManagerService()
    
    ctx = ContextEngine(memory_service=mem, world_model_service=mock_world_model, goal_manager_service=goal_manager)
    learn = LearningEngine(reg, mem)
    ref = ReflectionEngine(mem, llm)
    runtime = MockRuntime()
    ceo_brain = ExecutiveBrain() 
    
    # 2. Setup Container
    container = {
        "llm_service": llm,
        "workflow_runtime": runtime,
        "context_engine": ctx,
        "persistence_service": persistence,
        "skill_registry": reg,
        "learning_engine": learn,
        "reflection_engine": ref,
        "world_model_service": mock_world_model,
        "goal_manager_service": goal_manager,
        "event_bus": event_bus, # 🟢 3. ใส่เข้าไปใน Container เพื่อให้ CEO เรียกใช้
        "system_logger": MockLogger()
    }
    
    # Init services
    persistence.on_initialize(container)
    event_bus.on_initialize(container) # 🟢 Init Event Bus
    goal_manager.on_initialize(container)
    planner = PlannerAgent(container)
    ref.on_initialize(container)
    learn.on_initialize(container)
    reg.on_initialize(container)
    ceo_brain.on_initialize(container) 
    
    print("\n==============================================")
    print(" 📩 Scenario A: โหลดงานเข้าคิวปกติ (Task Queue)")
    print("==============================================")
    
    goal_manager.submit_goal("clean_room", priority=2) 
    goal_manager.submit_goal("download_files", priority=3)
    ceo_brain.process_all_goals(planner)
    
    print("\n==============================================")
    print(" 📡 Scenario B: เซนเซอร์ตรวจจับเหตุฉุกเฉิน (Reactive/Autonomous)")
    print("==============================================")
    
    # 🟢 จำลองว่าไม่มีใครสั่งงาน แต่มือถือหรือกล้องแจ้งเตือนเข้ามา
    event_bus.publish("SECURITY_ALERT", {"msg": "Intruder detected at front door!"})
    
    # สั่ง CEO เคลียร์คิว (ซึ่งตอนนี้จะมีงานด่วนแทรกเข้ามาแล้ว)
    ceo_brain.process_all_goals(planner)
    
if __name__ == "__main__":
    run_full_system_test()