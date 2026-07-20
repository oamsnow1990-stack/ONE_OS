import asyncio
from core.kernel.service_registry import DIContainer
from core.kernel.logger import SystemLogger, LogLevel
from core.kernel.event_bus import EventBus
from core.kernel.scheduler import Scheduler 
from core.kernel.executor import Executor
from core.workflow.runtime import WorkflowRuntime
from core.kernel.persistence import PersistenceManager
from core.agents.registry import AgentRegistry
from core.kernel.state_manager import StateManager
from core.kernel.event_store import EventStore 
from core.kernel.memory_service import MemoryService
from core.tools.registry import ToolRegistry
from core.tools.motion_tool import MotionDetectionTool

# Import ของใหม่
from core.kernel.llm_service import LLMService
from core.agents.planner_agent import PlannerAgent
from core.agents.security_agent import SecurityAgent
from core.tests.test_rollback import FileAgent, MockOEL

async def test_planner_flow():
    print("--- 🧠 Testing LLM Planner Agent (Type-Based DI Fixed) ---")
    
    container = DIContainer()
    
    # 1. Register Services ด้วย Alias ที่ Service ภายในเรียกหา
    logger = SystemLogger(EventBus(), LogLevel.DEBUG)
    container.register("system_logger", logger)
    container.register("logger", logger)
    
    container.register(EventBus, EventBus())
    container.register("event_bus", container.get(EventBus)) # Alias สำหรับ EventStore
    
    container.register(EventStore, EventStore("events.log"))
    container.register(MemoryService, MemoryService())
    
    tool_reg = ToolRegistry()
    try: tool_reg.register(MotionDetectionTool())
    except: pass
    container.register(ToolRegistry, tool_reg)
    
    container.register(Scheduler, Scheduler())
    container.register(Executor, Executor())
    
    # WorkflowRuntime และ Persistence Alias
    container.register(WorkflowRuntime, WorkflowRuntime())
    container.register("workflow_runtime", container.get(WorkflowRuntime))
    
    container.register(PersistenceManager, PersistenceManager())
    container.register("persistence_manager", container.get(PersistenceManager))
    
    container.register(AgentRegistry, AgentRegistry())
    container.register("agent_registry", container.get(AgentRegistry))
    
    container.register(StateManager, StateManager())
    
    # MockOEL และ Alias "oel_engine"
    mock_oel = MockOEL()
    container.register(MockOEL, mock_oel)
    container.register("oel_engine", mock_oel) # <--- แก้ KeyError ตัวล่าสุด
    
    container.register(LLMService, LLMService())

    # 2. ลงทะเบียน Agents
    reg = container.get(AgentRegistry) 
    reg.register(FileAgent())
    reg.register(SecurityAgent())
    reg.register(PlannerAgent(container))

    # 3. เริ่มทำงาน
    container.resolve_and_start_all()

    # 4. ทดสอบ Workflow
    ai_workflow = {
        "workflow_id": "ai_master_plan",
        "tasks": [{"id": "master_task", "agent": "PlannerAgent", "input": {"goal": "ช่วยเช็กความปลอดภัยผ่านกล้องให้หน่อย"}}]
    }

    # ทดสอบ Execute
    await container.get(WorkflowRuntime).execute(ai_workflow)
    
    print("\n✅ AI Planner Test Finished.")

    # 5. ปิดระบบ
    container.stop_all()

if __name__ == "__main__":
    asyncio.run(test_planner_flow())