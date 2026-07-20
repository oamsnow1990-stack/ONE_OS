# ONE OS Core Module: core/event_bus.py
import asyncio
from typing import Dict, List, Callable, Any

class ONEEventBus:
    """ระบบท่อส่งสัญญาณประสาทส่วนกลาง (Event Bus) รองรับการประมวลผลคู่ขนาน Asynchronous"""
    def __init__(self):
        self._listeners: Dict[str, List[Callable[[Any], Any]]] = {}

    def subscribe(self, event_type: str, listener: Callable[[Any], Any]):
        """ให้โมดูลต่าง ๆ ในระบบมาลงชื่อต่อท่อเกาะดักฟังเหตุการณ์สัญญาณ"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        if listener not in self._listeners[event_type]:
            self._listeners[event_type].append(listener)
            print(f"🔗 [Event Bus]: โมดูลลงทะเบียนเกาะดักฟังรหัส '{event_type}' เรียบร้อย")

    async def publish(self, event_type: str, data: Any = None):
        """ยิงกระจายสัญญาณ Event ออกไปหาทุกโมดูลที่รอดักฟังอยู่ให้ทำงานทันทีข้ามเธรด"""
        if event_type in self._listeners:
            tasks = []
            for listener in self._listeners[event_type]:
                if asyncio.iscoroutinefunction(listener):
                    tasks.append(listener(data))
                else:
                    # แปลงฟังก์ชันแบบปกติให้รันคู่ขนานไม่ให้ความเร็วลูปร่วง
                    tasks.append(asyncio.to_thread(listener, data))
            if tasks:
                await asyncio.gather(*tasks)

global_event_bus = ONEEventBus()