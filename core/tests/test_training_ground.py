import asyncio
import logging
from datetime import datetime
from core.kernel.event_bus import EventBus
from core.kernel.world_clock import WorldClock
from core.kernel.world_simulator import WorldSimulator
from core.kernel.world_state_registry import WorldStateRegistry
from core.kernel.simulation_engine import SimulationEngine
from core.kernel.experience_store import ExperienceStore 
from core.kernel.cognitive_decision_engine import CognitiveDecisionEngine
from core.kernel.confidence_engine import ConfidenceEngine
from core.kernel.telemetry_service import TelemetryService
from core.kernel.scenario_generator import ScenarioGenerator
from core.kernel.learning_engine import LearningEngine
from core.models.world_state import WorldState

# ตั้งค่า Logging สำหรับ Production Debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class MockContainer:
    def __init__(self):
        self._services = {}
    def register(self, cls_type, instance):
        self._services[cls_type] = instance
    def get(self, cls_type):
        return self._services.get(cls_type)

async def run_training_ground():
    print("🚀 [Training Ground] กำลังบูทระบบด้วย Production Lifecycle...")
    container = MockContainer()
    
    # 1. สร้าง Service Instances
    services = [
        EventBus(), WorldClock(), WorldSimulator(), WorldStateRegistry(), 
        SimulationEngine(), ExperienceStore(), ConfidenceEngine(), 
        TelemetryService(), CognitiveDecisionEngine(), ScenarioGenerator(),
        LearningEngine()
    ]
    
    # 2. Register & Initialize
    for svc in services:
        container.register(type(svc), svc)
        
    try:
        # ใช้ initialize() แทนการเรียก on_initialize/on_start แยกกัน
        for svc in services:
            svc.initialize(container)

        # 3. ตั้งค่าโลกเริ่มต้น (ผ่าน Dataclass ของ WorldState)
        registry = container.get(WorldStateRegistry)
        # แก้ไขให้ตรงกับโครงสร้าง Immutable Dataclass
        initial_world = WorldState(weather="sunny", energy=20)
        registry.register_state(initial_world)

        # 4. รัน Training Cycle
        print("\n⚡ [Hyperbolic Time Chamber] เริ่ม Training...")
        simulator = container.get(WorldSimulator)
        learning_engine = container.get(LearningEngine)
        
        for batch in range(10):
            await simulator.run_loop(tick_interval=0.0, max_ticks=100)
            learning_engine.run_calibration()
        
        print("\n✅ [System] จบการจำลอง Training Ground!")

        # 5. สรุปผลจาก SQLite (Analytics)
        store = container.get(ExperienceStore)
        cursor = store.conn.cursor()
        
        cursor.execute("SELECT COUNT(*), AVG(success) FROM experiences")
        row = cursor.fetchone()
        
        if row and row[0] > 0:
            print(f"\n📦 ความจำที่เรียนรู้: {row[0]} Records | Avg Success: {row[1]:.4f}")
            print("🔍 วิเคราะห์ตามสภาพอากาศ:")
            cursor.execute("SELECT weather, COUNT(*), AVG(success) FROM experiences GROUP BY weather")
            for w in cursor.fetchall():
                print(f"   - อากาศ [{w[0].upper()}]: เจอ {w[1]} ครั้ง -> Success: {w[2]:.2f}")
        else:
            print("⚠️ ไม่มีข้อมูลใน Database")

    except Exception as e:
        logging.error(f"CRITICAL [TrainingGround] ระบบล้มเหลว: {e}", exc_info=True)
    
    finally:
        # Shutdown Services อย่างปลอดภัย
        print("\n🛑 [System] กำลังปิดระบบ...")
        for svc in reversed(services):
            svc.stop()

if __name__ == "__main__":
    asyncio.run(run_training_ground())