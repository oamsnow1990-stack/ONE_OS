from core.kernel.di_container import DIContainer
from core.kernel.simulation_engine import SimulationEngine
from core.kernel.decision_engine import DecisionEngine
from core.kernel.telemetry_service import TelemetryService
from core.kernel.executive_brain import ExecutiveBrain
from core.kernel.executor_service import ExecutorService
from core.kernel.reflection_engine import ReflectionEngine
from core.models.decision_models import MissionProfile
from core.models.world_state import WorldState

# Mock Scenario Class
class MockScenario:
    def __init__(self, id): self.id = id

def run_full_cycle():
    # 1. Setup DI Container
    container = DIContainer()
    container.register("simulation_engine", SimulationEngine())
    container.register("decision_engine", DecisionEngine())
    container.register("telemetry_service", TelemetryService())
    container.register("executor_service", ExecutorService())
    container.register("reflection_engine", ReflectionEngine())

    # 2. Initialize Services
    brain = ExecutiveBrain()
    brain.on_initialize(container)
    
    executor = container.get("executor_service")
    executor.on_initialize(container)
    
    reflector = container.get("reflection_engine")
    reflector.on_initialize(container)

    # 3. เตรียมข้อมูล
    world = WorldState(version=15, data={"status": "active"})
    scenarios = [MockScenario("Plan_A"), MockScenario("Plan_B")]
    profile = MissionProfile("EMERGENCY", 0.5, 0.2, 0.1, 0.2)
    mission_id = "mission_alpha_cycle"

    print("🚀 [System] เริ่มต้นวงจร Full Cycle...")

    # A. BRAIN: ตัดสินใจและบันทึกข้อมูล
    brain.run_mission(mission_id, profile, scenarios, world)

    # B. EXECUTOR: รันจริงและอัปเดตผลลัพธ์ลง Telemetry
    executor.execute_mission(mission_id, "Plan_A") # จำลองว่าเลือก Plan_A

    # C. REFLECTION: วิเคราะห์ผลลัพธ์
    report = reflector.reflect_on_mission(mission_id)
    
    print(f"\n✅ [System] วงจรสมบูรณ์: {report}")

if __name__ == "__main__":
    run_full_cycle()