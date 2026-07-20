import asyncio
import time
from typing import Dict, Any
from core.kernel.base_service import BaseService
from core.kernel.events import SystemEvent, EventType
from core.kernel.scheduler import TaskState
from core.workflow.resolver import VariableResolver
from core.workflow.dag import DAGBuilder
from core.workflow.analyzer import StaticAnalyzer

class WorkflowRuntime(BaseService):
    def __init__(self):
        super().__init__("workflow_runtime")
        self.scheduler = None
        self.oel = None
        self.logger = None
        self.event_bus = None
        self.persistence = None
        self.executor = None 
        self.state_manager = None
        self.context = {}
        
        self.workflow_id = None
        self.layers = []
        self.current_layer_idx = 0
        self.compensation_stack = [] 

    def on_initialize(self, container):
        self.scheduler = container.get("scheduler")
        self.oel = container.get("oel_engine")
        self.logger = container.get("logger")
        self.event_bus = container.get("event_bus")
        self.executor = container.get("executor")
        self.state_manager = container.get("state_manager")
        self.persistence = container.get("persistence_manager")
        
        self.context = self.persistence.load() or {}
        self.event_bus.subscribe(EventType.TASK_FINISHED.value, self._on_task_finished)

    def on_start(self): self.logger.info("Workflow Runtime Service is Online.")
    def on_stop(self): self.logger.info("Workflow Runtime Service is Shutting Down.")

    def _on_task_finished(self, event: SystemEvent):
        task_id = event.data.get("task_id")
        result = event.data.get("result", {})
        status = result.get("status")
        
        # 🟢 GUARD CLAUSE: เพิ่ม ROLLBACK_FAILED ป้องกันลูปนรก
        current_state = self.state_manager.get_state(task_id)
        if current_state in [TaskState.ROLLING_BACK, TaskState.CANCELLED, TaskState.ROLLBACK_FAILED]:
            return 

        if status == "success":
            self.context[task_id] = result
            self.state_manager.transition(task_id, TaskState.COMPLETED)
            
            undo_info = result.get("undo_action")
            if isinstance(undo_info, dict) and "agent" in undo_info:
                self.compensation_stack.append({
                    "task_id": task_id,
                    "agent": undo_info.get("agent")
                })
            self.persistence.save(self.context)
            
        elif status in ["failed", "error"]:
            self.state_manager.transition(task_id, TaskState.FAILED)

    async def execute(self, workflow_json: Dict[str, Any]):
        is_valid, errors = StaticAnalyzer.analyze(workflow_json)
        if not is_valid:
            self.logger.error(f"❌ Workflow Rejected: {errors}")
            return
            
        self.workflow_id = workflow_json.get("workflow_id", f"wf_{int(time.time())}")
        self.layers = DAGBuilder.build(workflow_json.get("tasks", []))
        self.current_layer_idx = 0
        await self._schedule_next_layer()

    async def _schedule_next_layer(self):
        if self.current_layer_idx < len(self.layers):
            current_layer = self.layers[self.current_layer_idx]
            self.logger.info(f"🚀 [Parallel] Executing Layer {self.current_layer_idx}")
            
            tasks_to_run = []
            for task_data in current_layer:
                resolved_data = VariableResolver.resolve(task_data, self.context)
                task_id = resolved_data["id"]
                
                self.state_manager.transition(task_id, TaskState.RUNNING)
                
                if not self.oel.evaluate(resolved_data.get("condition", "True")):
                    self.state_manager.transition(task_id, TaskState.CANCELLED)
                    continue

                action_payload = {
                    "workflow_id": self.workflow_id,
                    "task_id": task_id,
                    "agent": resolved_data.get("agent"),
                    "input": resolved_data.get("input", {}),
                    "variables": self.context,
                    "timeout": resolved_data.get("timeout", 30)
                }
                tasks_to_run.append(self.executor.execute_async(action_payload))

            results = await asyncio.gather(*tasks_to_run, return_exceptions=True)
            
            if any(isinstance(r, dict) and r.get("status") in ["failed", "error"] for r in results):
                self.logger.error("🛑 Critical Failure. Aborting workflow and triggering Rollback.")
                await self._trigger_rollback()
                return

            self.current_layer_idx += 1
            await self._schedule_next_layer()
        else:
            self.logger.info("✅ All Layers Completed. Workflow Finished.")

    async def _trigger_rollback(self):
        self.logger.warning("🔄 Initiating Rollback Sequence...")
        is_fully_recovered = True # 🟢 ตัวแปรเช็กว่ากู้คืนสมบูรณ์ไหม
        
        while self.compensation_stack:
            item = self.compensation_stack.pop()
            task_id = item["task_id"]
            agent_name = item["agent"]
            
            self.logger.info(f"⏪ Executing Rollback for: {task_id}")
            
            try:
                self.state_manager.transition(task_id, TaskState.ROLLING_BACK)
                
                undo_payload = {
                    "workflow_id": self.workflow_id,
                    "task_id": task_id,
                    "agent": agent_name,
                    "mode": "undo",
                    "variables": self.context
                }
                result = await self.executor.execute_async(undo_payload)
                
                # 🟢 เช็กว่า Undo สำเร็จจริงไหม?
                if result and result.get("status") == "success":
                    self.state_manager.transition(task_id, TaskState.CANCELLED)
                else:
                    self.state_manager.transition(task_id, TaskState.ROLLBACK_FAILED)
                    self.logger.error(f"🚨 COMPENSATION_FAILED: Rollback failed on agent '{agent_name}' for task '{task_id}'")
                    is_fully_recovered = False
            except Exception as e:
                self.state_manager.transition(task_id, TaskState.ROLLBACK_FAILED)
                self.logger.error(f"🚨 COMPENSATION_FAILED: System error during rollback for '{task_id}': {e}")
                is_fully_recovered = False
        
        # 🟢 สรุปผลการกู้ภัยตอนจบ
        if is_fully_recovered:
            self.logger.info("✅ Rollback Sequence Finished (Fully Recovered).")
        else:
            self.logger.critical("🛑 WORKFLOW COMPENSATION FAILED: System is left in an inconsistent state!")