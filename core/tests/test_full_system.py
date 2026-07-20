import asyncio
import os
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
from core.kernel.scheduler import TaskState

# 🟢 Mock Agents และ Engine ที่จำเป็น
class SearchAgent(BaseAgent):
    @property
    def name(self) -> str: return "SearchAgent"
    def execute(self, context: ExecutionContext) -> AgentResult:
        query = context.input_data.get("keyword", "n/a")
        context.logger.info(f"🔎 [SearchAgent] Starting: {query}")
        import time; time.sleep(1.5) 
        return AgentResult(status="success", output={"url": f"http://{query}.com"})

class AnalyzeAgent(BaseAgent):
    @property
    def name(self) -> str: return "AnalyzeAgent"
    def execute(self, context: ExecutionContext) -> AgentResult:
        return AgentResult(status="success", output={"summary": "Merge complete"})

class MockOEL:
    def __init__(self): self.name = "oel_engine"
    def evaluate(self, condition: str) -> bool: return True

async def test_full_system():
    if os.path.exists("workflow_state.json"): os.remove("workflow_state.json")

    print("--- 🏁 Starting ONE_OS State Machine Parallel Test ---")
    
    container = DIContainer()
    container.register(SystemLogger(EventBus(), LogLevel.DEBUG))
    container.register(EventBus())
    container.register(Scheduler())
    container.register(Executor())
    container.register(WorkflowRuntime())
    container.register(PersistenceManager())
    container.register(AgentRegistry())
    container.register(StateManager())
    container.register(MockOEL())

    services = [
        container.get("agent_registry"), 
        container.get("scheduler"), 
        container.get("executor"), 
        container.get("workflow_runtime"), 
        container.get("persistence_manager"),
        container.get("state_manager")
    ]
    
    for s in services:
        s.on_initialize(container)
        s.on_start()

    container.get("agent_registry").register(SearchAgent())
    container.get("agent_registry").register(AnalyzeAgent())

    workflow_data = {
        "tasks": [
            {"id": "search_yt", "agent": "SearchAgent", "input": {"keyword": "youtube"}},
            {"id": "search_google", "agent": "SearchAgent", "input": {"keyword": "google"}},
            {"id": "merge_results", "agent": "AnalyzeAgent", "depends_on": ["search_yt", "search_google"]}
        ]
    }

    await container.get("workflow_runtime").execute(workflow_data)
    
    print("\n✅ State Machine Test Finished.")
    
    for s in reversed(services):
        s.on_stop()

if __name__ == "__main__":
    asyncio.run(test_full_system())