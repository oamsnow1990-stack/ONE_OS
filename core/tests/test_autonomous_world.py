import asyncio
from datetime import datetime
from core.kernel.event_bus import EventBus
from core.kernel.world_clock import WorldClock
from core.kernel.world_simulator import WorldSimulator
from core.kernel.world_state_registry import WorldStateRegistry
from core.kernel.simulation_engine import SimulationEngine
from core.models.world_state import WorldState
from core.models.events import SystemEvent

class MockContainer:
    def __init__(self):
        self._services = {}
    def register(self, cls_type, instance):
        self._services[cls_type] = instance
    def get(self, cls_type):
        return self._services.get(cls_type)

async def test_autonomous_world():
    print("🚀 [Test] เริ่มบูทระบบ Autonomous World...")
    container = MockContainer()
    
    # 1. สร้าง Services ครบทุกตัว
    services = [
        EventBus(), WorldClock(), WorldSimulator(), 
        WorldStateRegistry(), SimulationEngine()
    ]
    
    # ลงทะเบียนเข้า Container
    for svc in services:
        container.register(type(svc), svc)
        
    # 2. Initialize & Start
    for svc in services:
        svc.on_initialize(container)
        svc.on_start()

    # 3. สร้าง Initial WorldState ยัดเข้า Registry ไว้เป็นจุดเริ่มต้น
    registry = container.get(WorldStateRegistry)
    initial_world = WorldState(
        version="1.0", timestamp=datetime.now(),
        resources={"amount": 20}, # เริ่มที่ทรัพยากร 20
        weather={"condition": "sunny"}
    )
    registry.register_state(initial_world)

    # 4. สร้าง Listener รอฟังเวลา State เปลี่ยน
    def on_world_updated(event: SystemEvent):
        current = registry.get_current_state()
        print(f"🌀 [World Observer] Tick {current.tick}: ทรัพยากรเหลือ {current.resources['amount']} | อากาศ: {current.weather['condition']}")
        
    container.get(EventBus).subscribe("WORLD_STATE_UPDATED", on_world_updated)

    # 5. ปล่อยให้ระบบเดินเอง!
    print("\n⚙️ [Simulator] ปล่อยให้โลกหมุนอัตโนมัติ 5 Ticks...")
    simulator = container.get(WorldSimulator)
    await simulator.run_loop(tick_interval=0.5, max_ticks=5) # ลดความเร็วเทสเหลือ 0.5s จะได้ไวๆ
    
    print("\n✅ [Test] จบการจำลองโลกอย่างสมบูรณ์!")

if __name__ == "__main__":
    asyncio.run(test_autonomous_world())