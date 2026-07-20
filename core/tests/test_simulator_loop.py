import asyncio
from core.kernel.event_bus import EventBus
from core.kernel.world_clock import WorldClock
from core.kernel.world_simulator import WorldSimulator
from core.models.events import SystemEvent

class MockContainer:
    """Container จำลองสำหรับการทดสอบ"""
    def __init__(self):
        self._services = {}
    
    def register(self, cls_type, instance):
        self._services[cls_type] = instance
        
    def get(self, cls_type):
        return self._services.get(cls_type)

async def test_simulator():
    print("🚀 [Test] เริ่มบูทระบบ WorldSimulator Loop...")
    
    # 1. สร้าง Services
    container = MockContainer()
    event_bus = EventBus()
    clock = WorldClock()
    simulator = WorldSimulator()
    
    # 2. ลงทะเบียน Services
    container.register(EventBus, event_bus)
    container.register(WorldClock, clock)
    
    # 3. Initialize
    event_bus.on_initialize(container)
    clock.on_initialize(container)
    simulator.on_initialize(container)
    
    # 4. Start Services
    event_bus.on_start()
    clock.on_start()
    simulator.on_start()
    
    # 5. สร้าง Listener เพื่อฟังเสียงนาฬิกา
    def on_time_tick(event: SystemEvent):
        tick_val = event.payload.get("tick")
        print(f"🌍 [World Observer] รับทราบการเปลี่ยนแปลง! ตอนนี้โลกอยู่ที่ Tick: {tick_val}")

    event_bus.subscribe("TIME_TICK", on_time_tick)
    
    # 6. รัน Simulator Loop อัตโนมัติ (5 Ticks, หน่วงเวลา 1 วินาที/Tick)
    print("\n⚙️ [Simulator] ปล่อยให้โลกหมุนอัตโนมัติ 5 Ticks (ความเร็ว: 1 วินาที/Tick)...")
    await simulator.run_loop(tick_interval=1.0, max_ticks=5)
    
    print("\n✅ [Test] จบการจำลองโลกอย่างสมบูรณ์!")

if __name__ == "__main__":
    # ใช้ asyncio.run เพื่อรัน Asynchronous function
    asyncio.run(test_simulator())