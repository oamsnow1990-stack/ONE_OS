import asyncio
from datetime import datetime
from core.kernel.event_bus import EventBus
from core.kernel.world_clock import WorldClock
from core.kernel.world_simulator import WorldSimulator
from core.kernel.world_state_registry import WorldStateRegistry
from core.kernel.simulation_engine import SimulationEngine
from core.kernel.experience_store import ExperienceStore  # 🟢 เพิ่ม Import สมองส่วนความจำ
from core.kernel.cognitive_decision_engine import CognitiveDecisionEngine
from core.kernel.confidence_engine import ConfidenceEngine
from core.kernel.telemetry_service import TelemetryService
from core.models.world_state import WorldState
from core.kernel.scenario_generator import ScenarioGenerator

class MockContainer:
    def __init__(self):
        self._services = {}
    def register(self, cls_type, instance):
        self._services[cls_type] = instance
    def get(self, cls_type):
        return self._services.get(cls_type)

async def test_reactive_brain():
    print("🚀 [System] กำลังบูทระบบ Autonomous Core + Cognitive Brain...")
    container = MockContainer()
    
    # 1. สร้าง Services ทั้งหมด! (Full Stack)
    services = [
        EventBus(), 
        WorldClock(), 
        WorldSimulator(), 
        WorldStateRegistry(), 
        SimulationEngine(),
        ExperienceStore(),         # 🟢 เสียบสมองส่วนความจำเข้าสู่ระบบ
        ConfidenceEngine(), 
        TelemetryService(), 
        CognitiveDecisionEngine(), 
        ScenarioGenerator()
    ]
    
    for svc in services:
        container.register(type(svc), svc)
        
    # 2. Initialize & Start
    for svc in services:
        svc.on_initialize(container)
        svc.on_start()

    # 3. สร้าง Initial WorldState (ทรัพยากร 20, อากาศสุ่มเปลี่ยน)
    registry = container.get(WorldStateRegistry)
    initial_world = WorldState(
        version="1.0", timestamp=datetime.now(),
        resources={"amount": 20}, weather={"condition": "sunny"}
    )
    registry.register_state(initial_world)

    # 4. รันวงล้อแห่งเวลา!
    print("\n⚙️ [Simulator] ปล่อยโลกหมุน 5 Ticks ให้สมองได้ทำงาน...")
    simulator = container.get(WorldSimulator)
    
    # ตั้งค่าให้เปลี่ยน Tick ทุกๆ 1 วินาที เพื่อให้ท่านเห็นกระบวนการคิด
    await simulator.run_loop(tick_interval=1.0, max_ticks=10) 
    
    print("\n✅ [System] จบการจำลอง!")

if __name__ == "__main__":
    asyncio.run(test_reactive_brain())