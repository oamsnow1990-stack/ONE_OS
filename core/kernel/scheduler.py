import queue
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Any
from .base_service import BaseService

# 🟢 Phase 2: Workflow State Machine - ครอบคลุมทุกสถานะตามโจทย์
class TaskState(Enum):
    PENDING = "PENDING"
    READY = "READY"             # พร้อมรัน (ผ่าน dependency แล้ว)
    RUNNING = "RUNNING"
    WAITING = "WAITING"         # รอ Dependency หรือทรัพยากร
    RETRYING = "RETRYING"       # อยู่ในกระบวนการ Retry
    FAILED = "FAILED"           # ล้มเหลวถาวร
    ROLLING_BACK = "ROLLING_BACK" # กำลังทำ Undo / Rollback
    COMPLETED = "COMPLETED"     # สำเร็จ
    CANCELLED = "CANCELLED"     # ถูกยกเลิกโดยผู้ใช้หรือระบบ
    PAUSED = "PAUSED"           # หยุดพักชั่วคราว
    ROLLBACK_FAILED = "ROLLBACK_FAILED"
    
@dataclass
class Task:
    id: str
    priority: int = 5
    action: Any = None
    dependencies: List[str] = field(default_factory=list)
    
    # ระบบติดตามสถานะและการ Retry
    state: TaskState = TaskState.PENDING
    max_retries: int = 3
    current_retry: int = 0
    error_message: str = ""

    def __lt__(self, other):
        # Priority Queue: น้อยกว่าคือ Priority สูงกว่า (เลขน้อย รันก่อน)
        return self.priority < other.priority

class Scheduler(BaseService):
    def __init__(self):
        super().__init__("scheduler")
        self.task_queue = queue.PriorityQueue()
        self.logger = None

    def on_initialize(self, container):
        self.logger = container.get("logger")

    def on_start(self):
        self.logger.info("Scheduler Service started.")

    def on_stop(self):
        self.logger.info("Scheduler Service stopped.")

    def schedule(self, task: Task):
        """รับ Task เข้าสู่คิวและกำหนดสถานะตั้งต้น"""
        # ถ้า Task มี dependencies ให้ตั้งเป็น WAITING ไว้ก่อนได้ (ถ้าต้องการขยายในอนาคต)
        if task.dependencies:
            task.state = TaskState.WAITING
        else:
            task.state = TaskState.READY
            
        self.task_queue.put(task)
        if self.logger:
            self.logger.debug(f"Task scheduled: {task.id} [State: {task.state.value}]")

    def run_next(self) -> Task:
        """หยิบ Task ถัดไปที่พร้อมรัน"""
        if not self.task_queue.empty():
            task = self.task_queue.get()
            
            # ตรวจสอบก่อนรัน: ถ้าถูก Cancelled หรืออื่นๆ ไม่ต้องรัน
            if task.state == TaskState.CANCELLED:
                return self.run_next()
                
            task.state = TaskState.RUNNING
            return task
        return None