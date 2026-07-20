import asyncio
import time
from typing import Dict, Any
from .base_service import BaseService
from ..kernel.events import SystemEvent, EventType
from core.agents.models import ExecutionContext, AgentResult

class Executor(BaseService):
    def __init__(self):
        super().__init__("executor")
        self.registry = None
        self.event_bus = None
        self.logger = None
        self.memory = None 
        self.tool_registry = None
        self.reflection = None # 🟢 เพิ่ม Reflection Engine Instance

    def on_initialize(self, container: Any) -> None:
        self.registry = container.get("agent_registry")
        self.event_bus = container.get("event_bus")
        self.logger = container.get("system_logger") 
        self.memory = container.get("memory_service")
        self.tool_registry = container.get("tool_registry")
        self.reflection = container.get("reflection_engine") # 🟢 ดึงจาก Container

    def on_start(self) -> None:
        if self.logger:
            self.logger.info("🚀 Async Executor Service started.")

    def on_stop(self) -> None:
        if self.logger:
            self.logger.info("🛑 Async Executor Service stopped.")

    async def execute_async(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        task_id = payload.get("task_id", "unknown_task")
        timeout = payload.get("timeout", 30)
        is_rollback = payload.get("mode") == "undo"
        
        prefix = "⏪ [Rollback]" if is_rollback else "⚡ [Parallel]"
        if self.logger:
            self.logger.info(f"{prefix} Starting task: {task_id} (Timeout: {timeout}s)")
        
        try:
            return await asyncio.wait_for(
                self._run_task_with_retries(task_id, payload), 
                timeout=timeout
            )
        except asyncio.TimeoutError:
            if self.logger:
                self.logger.error(f"⏱️ Task '{task_id}' TIMED OUT after {timeout} seconds!")
            return {"status": "failed", "error": f"Timeout after {timeout}s"}

    async def _run_task_with_retries(self, task_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        max_retries = 3 
        current_attempt = 0
        
        if self.event_bus:
            start_event = SystemEvent(type=EventType.TASK_STARTED, source=self.name, data={"task_id": task_id})
            self.event_bus.publish(start_event.type.value, start_event)

        while current_attempt <= max_retries:
            result_dict = await asyncio.to_thread(self._execute_agent_sync, task_id, payload)
            
            if result_dict.get("status") == "success":
                # 🟢 [Milestone 7 Integration] สั่ง Reflection Engine ให้ทำหน้าที่ "ทบทวนบทเรียน"
                if self.reflection:
                    self.reflection.reflect(
                        payload.get("workflow_id", "unknown"), 
                        result_dict, 
                        "Task execution successful"
                    )

                if self.event_bus:
                    finish_event = SystemEvent(type=EventType.TASK_FINISHED, source=self.name, data={"task_id": task_id, "result": result_dict})
                    self.event_bus.publish(finish_event.type.value, finish_event)
                return result_dict
            
            current_attempt += 1
            if current_attempt <= max_retries:
                if self.logger:
                    self.logger.warning(f"⚠️ Task '{task_id}' failed. Retry ({current_attempt}/{max_retries})...")
                await asyncio.sleep(1)
            else:
                if self.logger:
                    self.logger.error(f"❌ Task '{task_id}' FAILED after retries.")
                if self.event_bus:
                    finish_event = SystemEvent(type=EventType.TASK_FINISHED, source=self.name, data={"task_id": task_id, "result": result_dict})
                    self.event_bus.publish(finish_event.type.value, finish_event)
                return result_dict

    def _execute_agent_sync(self, task_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # ... (โค้ดส่วนนี้ถูกต้องแล้ว ไม่ต้องแก้ครับ) ...
        agent_name = payload.get("agent")
        if not agent_name:
            return {"status": "failed", "error": "No agent specified."}

        try:
            context = ExecutionContext(
                workflow_id=payload.get("workflow_id", "unknown"),
                task_id=task_id,
                input_data=payload.get("input", {}),
                variables=payload.get("variables", {}),
                logger=self.logger,
                memory=self.memory,
                tool_registry=self.tool_registry
            )
            
            agent = self.registry.get_agent(agent_name)
            is_rollback = payload.get("mode") == "undo"

            if agent and agent.validate(context) and agent.can_execute(context):
                start_time = time.time()
                
                if is_rollback:
                    agent_result = agent.undo(context)
                else:
                    agent_result = agent.execute(context)
                
                if agent_result:
                    agent_result.latency = round(time.time() - start_time, 4)
                    return {
                        "status": agent_result.status,
                        "output": agent_result.output,
                        "error": agent_result.error,
                        "undo_action": {"agent": agent_name}
                    }
            
            return {"status": "failed", "error": "Execution or Validation failed"}
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Execution Error on {task_id}: {str(e)}")
            return {"status": "error", "error": str(e)}