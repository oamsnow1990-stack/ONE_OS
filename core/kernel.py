# ONE OS Core Module: core/kernel.py
import asyncio
import time
from core.event_bus import global_event_bus

class ONEAIKernel:
    """แกนควบคุมหลักของระบบปฏิบัติการ AI OS (Kernel Loader)"""
    def __init__(self):
        self.is_running = False
        self.boot_time = None

    async def boot_kernel(self):
        """จุดชนวนเครื่องยนต์หลักพร้อมบรอดแคสต์สถานะเริ่มต้นระบบ"""
        self.is_running = True
        self.boot_time = time.time()
        print("\n🧠 [AI Kernel]: ระบบกำลังจุดระเบิดโครงข่ายประสาท Event Bus ส่วนกลาง...")
        await global_event_bus.publish("SYSTEM_BOOT", {"timestamp": self.boot_time})
        print("🧠 [AI Kernel]: แกนสมอง AI Kernel สแตนด์บายพร้อมรันภารกิจ 100%")

    async def shutdown_kernel(self):
        """ปิดระบบปฏิบัติการและคืนทรัพยากรอย่างปลอดภัย"""
        self.is_running = False
        print("\n🛑 [AI Kernel]: กำลังดับเครื่องยนต์ระบบปฏิบัติการ ONE OS อย่างปลอดภัย...")
        await global_event_bus.publish("SYSTEM_SHUTDOWN")

global_ai_kernel = ONEAIKernel()