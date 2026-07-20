from typing import Any, Optional, Dict
import uuid
import heapq
from dataclasses import dataclass, field
from datetime import datetime
from core.kernel.base_service import BaseService

@dataclass
class GoalItem:
    description: str
    priority: int = 2  # 0=Critical, 1=High, 2=Normal, 3=Low
    goal_id: str = field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:6]}")
    status: str = "pending"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __lt__(self, other):
        return self.priority < other.priority

class GoalManagerService(BaseService):
    def __init__(self):
        super().__init__("goal_manager")
        self.queue = [] # Priority Queue 
        self.history = {}
        self.logger = None
        self._current_goal = None     # 🟢 track goal ปัจจุบัน
        self._total_received = 0      # 🟢 track จำนวนเป้าหมายทั้งหมด

    def on_initialize(self, container: Any) -> None:
        self.logger = container.get("system_logger")
        if self.logger:
            self.logger.info("🗂️ [GoalManager] ระบบคิวงานและลำดับความสำคัญ (Task Queue) พร้อมทำงาน")

    def on_start(self): pass
    def on_stop(self): pass

    def submit_goal(self, description: str, priority: int = 2) -> GoalItem:
        """รับงานใหม่เข้าคิว"""
        goal = GoalItem(description=description, priority=priority)
        heapq.heappush(self.queue, goal)
        self.history[goal.goal_id] = goal
        self._total_received += 1     # 🟢 บันทึกยอดรวม
        
        pri_labels = {0: "🔴 CRITICAL", 1: "🟠 HIGH", 2: "🟢 NORMAL", 3: "🔵 LOW"}
        if self.logger:
            self.logger.info(f"📥 [GoalManager] รับคำสั่งเข้าคิว: '{description}' [{pri_labels.get(priority, 'UNKNOWN')}]")
        return goal

    def get_next_goal(self) -> Optional[GoalItem]:
        """ดึงงานที่สำคัญที่สุดออกมาทำ"""
        if self.queue:
            goal = heapq.heappop(self.queue)
            self._current_goal = goal # 🟢 track goal ปัจจุบัน
            return goal
        return None

    def mark_goal_done(self):
        """ล้างค่าเป้าหมายปัจจุบันเมื่อทำงานเสร็จ"""
        self._current_goal = None     # 🟢 clear เมื่อเสร็จ

    def get_goal_context(self) -> Dict[str, Any]:
        """
        ส่งบริบทของ goal queue ปัจจุบันให้ ContextEngine
        PlannerAgent ใช้ข้อมูลนี้ตัดสินใจว่าควรทำอะไรต่อ
        """
        current = self._current_goal
        
        # PriorityQueue ของเราใช้ List กับ heapq สามารถวนลูปอ่านค่าแบบ Thread-safe ได้เลย
        pending = [
            {"id": g.goal_id, "name": g.description, "priority": g.priority}
            for g in self.queue
        ]
        
        return {
            "current_goal": {
                "id":       current.goal_id       if current else None,
                "name":     current.description   if current else None,
                "priority": current.priority      if current else None,
            },
            "pending_count": len(pending),
            "pending_goals": pending,
            "total_goals":   self._total_received,
        }