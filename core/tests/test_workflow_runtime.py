import json
from core.workflow.runtime import WorkflowRuntime
from core.workflow.dag import DAGBuilder  # 1. เพิ่ม DAGBuilder
from core.kernel.scheduler import Scheduler
from core.kernel.service_registry import DIContainer
from core.kernel.logger import SystemLogger, LogLevel
from core.kernel.event_bus import EventBus

class MockOEL:
    name = "oel_engine" 
    
    def evaluate(self, condition: str) -> bool:
        print(f"🧠 [OEL] Evaluating: {condition}")
        return True

def test_workflow_execution():
    # 1. Setup DI Container
    container = DIContainer()
    
    # 2. Register Services
    event_bus = EventBus()
    logger = SystemLogger(event_bus, LogLevel.DEBUG)
    scheduler = Scheduler()
    
    container.register(logger)
    container.register(event_bus)
    container.register(scheduler)
    container.register(MockOEL())

    # 3. Initialize & Start
    scheduler.on_initialize(container)
    scheduler.on_start()

    runtime = WorkflowRuntime()
    runtime.on_initialize(container)
    runtime.on_start()

    # 4. Workflow JSON (เพิ่มความซับซ้อนของ dependency เพื่อทดสอบ DAG)
    workflow_data = {
        "workflow_id": "analyze_ai_trends_2026",
        "tasks": [
            {"id": "search_step", "action": "youtube_search", "priority": 10},
            {"id": "analyze_step", "action": "oel_analyze", "priority": 8, "depends_on": ["search_step"]},
            {"id": "report_step", "action": "write_report", "priority": 5, "depends_on": ["analyze_step"]}
        ]
    }

    # 5. Execute ผ่าน DAG Builder ก่อน (นี่คือการอัปเกรด Runtime!)
    print(f"📦 Building DAG for Workflow: {workflow_data['workflow_id']}")
    execution_layers = DAGBuilder.build(workflow_data["tasks"])
    
    for i, layer in enumerate(execution_layers):
        print(f"🔹 Executing Layer {i}: {[t['id'] for t in layer]}")
        # ในอนาคต runtime.execute จะรับ execution_layers ไปรันแบบขนานได้เลย
        runtime.execute({"tasks": layer})

    # 6. ตรวจผล
    print(f"\n📦 Tasks in Scheduler Queue: {scheduler.get_queue_size()}")

if __name__ == "__main__":
    test_workflow_execution()