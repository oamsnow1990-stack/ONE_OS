import heapq
import threading
import functools  # 🟢 1. เพิ่ม functools สำหรับทำ Decorator
from typing import Callable, Dict, List, Any
from core.kernel.base_service import BaseService
from core.models.events import SystemEvent

# 🟢 2. เพิ่ม Decorator เข้ามา เพื่อให้ไฟล์อื่นๆ (เช่น cognitive_decision_engine) เรียกใช้ได้
def safe_event_handler(func):
    """
    Decorator ป้องกันไม่ให้ระบบแครชหากเกิด Error ภายใน Event Handler
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"⚠️ [SafeEventHandler] Error in '{func.__name__}': {e}")
            return None
    return wrapper

class EventBus(BaseService):
    def __init__(self):
        super().__init__("event_bus")
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_queue: List[SystemEvent] = []
        self._lock = threading.Lock()  # ป้องกัน Race Condition

    def on_initialize(self, container: Any) -> None:
        self.logger.debug("Bus initializing...")

    def on_start(self) -> None:
        self.logger.info("Bus started.")

    def on_stop(self) -> None:
        self.logger.info("Bus stopped.")

    def subscribe(self, event_type: str, callback: Callable) -> None:
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            
            # ป้องกันการ Add Callback ซ้ำซ้อน (Duplicate Subscriptions)
            if callback not in self._subscribers[event_type]:
                self._subscribers[event_type].append(callback)

    # 🟢 3. แก้ไขให้ payload มีค่า Default เป็น None เพื่อรองรับการเรียก publish("EVENT_NAME") เฉยๆ
    def publish(self, event_type: str, payload: Dict[str, Any] = None, priority: int = 10) -> None:
        if payload is None:
            payload = {}
            
        event = SystemEvent(priority=priority, event_type=event_type, payload=payload)
        with self._lock:
            heapq.heappush(self._event_queue, event)

    def process_events(self) -> int:
        processed_count = 0
        while True:
            # ดึง Event ออกมาอย่างปลอดภัย
            with self._lock:
                if not self._event_queue:
                    break
                event = heapq.heappop(self._event_queue)
            
            subscribers = self._subscribers.get(event.event_type, [])
            for callback in subscribers:
                try:
                    callback(event)
                except Exception as e:
                    # [Telemetry] ระบุชื่อคลาส/ฟังก์ชันที่พังทันที
                    self._report_failure(event.event_type, callback, e)
            
            processed_count += 1
        return processed_count

    def _report_failure(self, event_type: str, callback: Callable, error: Exception) -> None:
        """ระบุตัวตนของ Subscriber ที่ทำงานผิดพลาด"""
        func_name = getattr(callback, '__name__', 'unknown_func')
        # ถ้าเป็น method ของ class ให้ดึงชื่อ class มาด้วย
        class_name = getattr(callback, '__self__', None)
        ctx = class_name.__class__.__name__ if class_name else "Global"
        
        self.logger.error(
            f"❌ [EventBus] CRITICAL ERROR | Event: {event_type} | "
            f"Target: {ctx}.{func_name}() | Error: {str(error)}"
        )