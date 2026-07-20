from typing import Dict
from .base_service import BaseService
from ..kernel.events import SystemEvent, EventType
from core.kernel.scheduler import TaskState

class StateManager(BaseService):
    def __init__(self):
        super().__init__("state_manager")
        self._states: Dict[str, TaskState] = {} # เก็บสถานะของทุก Task
        self.logger = None
        self.event_bus = None

    def on_initialize(self, container):
        self.logger = container.get("logger")
        self.event_bus = container.get("event_bus")

    def on_start(self): self.logger.info("State Manager Service started.")
    def on_stop(self): self.logger.info("State Manager Service stopped.")

    def transition(self, task_id: str, new_state: TaskState):
        """ทำการเปลี่ยนสถานะของ Task และแจ้งเตือนระบบ"""
        old_state = self._states.get(task_id, TaskState.PENDING)
        self._states[task_id] = new_state
        
        self.logger.debug(f"🔄 State Change: [{task_id}] {old_state.value} -> {new_state.value}")
        
        # ประกาศ Event ให้ Dashboard (Priority 6) มารอรับข้อมูล
        event = SystemEvent(
            type=EventType.STATE_CHANGED, 
            source=self.name, 
            data={"task_id": task_id, "from": old_state.value, "to": new_state.value}
        )
        self.event_bus.publish(event.type.value, event)

    def get_state(self, task_id: str) -> TaskState:
        return self._states.get(task_id, TaskState.PENDING)