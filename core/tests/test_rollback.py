import asyncio
from core.kernel.service_registry import DIContainer
from core.kernel.logger import SystemLogger, LogLevel
from core.kernel.event_bus import EventBus
from core.kernel.scheduler import Scheduler
from core.kernel.executor import Executor
from core.workflow.runtime import WorkflowRuntime
from core.kernel.persistence import PersistenceManager
from core.agents.registry import AgentRegistry
from core.agents.base import BaseAgent
from core.agents.models import ExecutionContext, AgentResult
from core.kernel.state_manager import StateManager
from core.kernel.event_store import EventStore 
from core.kernel.memory_service import MemoryService
from core.tools.registry import ToolRegistry
from core.tools.math_tool import CalculatorTool
from core.tools.search_tool import WebSearchTool

# นำเข้า Agents และ Tools
from core.agents.security_agent import SecurityAgent
from core.tools.motion_tool import MotionDetectionTool

class MockOEL:
    def __init__(self): self.name = "oel_engine"
    def evaluate(self, condition: str) -> bool: return True

# -- Agents เดิมที่จำเป็น --
class FileAgent(BaseAgent):
    @property
    def name(self) -> str: return "FileAgent"
    def execute(self, context: ExecutionContext) -> AgentResult:
        context.logger.info(f"📁 [FileAgent] Action: Created Virtual File for {context.task_id}")
        return AgentResult(status="success", output={"path": "/virtual/data.txt"})
    def undo(self, context: ExecutionContext) -> AgentResult:
        context.logger.info(f"🗑️ [FileAgent] Undo: Deleted Virtual File for {context.task_id}")
        return AgentResult(status="success", output={"msg": "Cleanup complete"})

class FailAgent(BaseAgent):
    @property
    def name(self) -> str: return "FailAgent"
    def execute(self, context: ExecutionContext) -> AgentResult:
        context.logger.error(f"💥 [FailAgent] Planned failure on {context.task_id}!")
        return AgentResult(status="failed", error="Manual Triggered Failure", output={})

class SubWorkflowAgent(BaseAgent):
    _child_runtimes = {} 
    def __init__(self, container): self.container = container
    @property
    def name(self) -> str: return "SubWorkflowAgent"
    def execute(self, context: ExecutionContext) -> AgentResult:
        child_workflow = context.input_data.get("workflow")
        context.logger.info("🌀 [SubWorkflow] Launching Child Workflow...")
        child_runtime = WorkflowRuntime()
        child_runtime.on_initialize(self.container)
        child_runtime.on_start()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(child_runtime.execute(child_workflow))
        loop.close()
        wf_id = child_runtime.workflow_id
        SubWorkflowAgent._child_runtimes[wf_id] = child_runtime
        context.logger.info(f"✅🌀 [SubWorkflow] Child Workflow '{wf_id}' Completed.")
        return AgentResult(status="success", output={"child_workflow_id": wf_id})
    def undo(self, context: ExecutionContext) -> AgentResult:
        task_result = context.variables.get(context.task_id, {})
        wf_id = task_result.get("output", {}).get("child_workflow_id")
        if wf_id and wf_id in SubWorkflowAgent._child_runtimes:
            context.logger.warning(f"⏪🌀 [SubWorkflow] CASCADE ROLLBACK to Child '{wf_id}'...")
            child_runtime = SubWorkflowAgent._child_runtimes[wf_id]
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(child_runtime._trigger_rollback())
            loop.close()
            return AgentResult(status="success", output={"msg": "Cascade complete"})
        return AgentResult(status="failed", error="Child runtime not found")

async def test_rollback_flow():
    print("--- 🛡️ Testing Enterprise Nested Workflows ---")
    
    container = DIContainer()
    
    # ลงทะเบียน Services แบบระบุ Key ให้ชัดเจน (ป้องกัน KeyError)
    container.register("system_logger", SystemLogger(EventBus(), LogLevel.DEBUG))
    container.register("event_bus", EventBus())
    container.register("event_store", EventStore("events.log"))
    container.register("memory_service", MemoryService())
    
    tool_reg = ToolRegistry()
    try: tool_reg.register(MotionDetectionTool())
    except: pass
    container.register("tool_registry", tool_reg)
    
    container.register("scheduler", Scheduler())
    container.register("executor", Executor())
    container.register("workflow_runtime", WorkflowRuntime())
    container.register("persistence_manager", PersistenceManager())
    container.register("agent_registry", AgentRegistry())
    container.register("state_manager", StateManager())
    container.register("oel_engine", MockOEL())

    services_keys = ["event_store", "memory_service", "tool_registry", "agent_registry", 
                     "scheduler", "executor", "workflow_runtime", "persistence_manager", "state_manager"]
    
    for s_key in services_keys:
        s = container.get(s_key)
        if s:
            s.on_initialize(container)
            s.on_start()

    container.get("agent_registry").register(FileAgent())
    container.get("agent_registry").register(FailAgent())
    container.get("agent_registry").register(SubWorkflowAgent(container))
    container.get("agent_registry").register(SecurityAgent())

    child_workflow = {"workflow_id": "child_wf_01", "tasks": [{"id": "child_task_1", "agent": "FileAgent"}]}
    parent_workflow = {
        "workflow_id": "parent_wf_01",
        "tasks": [
            {"id": "parent_task_1", "agent": "SecurityAgent"}, 
            {"id": "parent_task_2", "agent": "SubWorkflowAgent", "depends_on": ["parent_task_1"], "input": {"workflow": child_workflow}},
            {"id": "parent_task_3", "agent": "FailAgent", "depends_on": ["parent_task_2"]}
        ]
    }

    await container.get("workflow_runtime").execute(parent_workflow)
    print("\n✅ Nested Rollback Test Finished.")

    for s_key in reversed(services_keys):
        s = container.get(s_key)
        if s: s.on_stop()

if __name__ == "__main__":
    asyncio.run(test_rollback_flow())