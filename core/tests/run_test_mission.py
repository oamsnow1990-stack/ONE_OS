from core.kernel.di_container import DIContainer
from core.kernel.simulation_engine import SimulationEngine
from core.kernel.decision_engine import DecisionEngine
from core.kernel.telemetry_service import TelemetryService
from core.kernel.executive_brain import ExecutiveBrain
from core.models.decision_models import MissionProfile
from core.models.world_state import WorldState
import json

# Mock Scenario Class
class MockScenario:
    def __init__(self, id): self.id = id

# 1. Setup Environment
container = DIContainer()
container.register("simulation_engine", SimulationEngine())
container.register("decision_engine", DecisionEngine())
container.register("telemetry_service", TelemetryService())

brain = ExecutiveBrain()
brain.on_initialize(container)
brain.on_start()

# 2. Prepare Context (Simulation of WorldState)
world = WorldState(version=15, data={"status": "active_mission"})
scenarios = [MockScenario("Plan_A"), MockScenario("Plan_B"), MockScenario("Plan_C")]
profile = MissionProfile("EMERGENCY", 0.55, 0.25, 0.05, 0.15)

# 3. Run Mission
print("🚀 Running Mission Alpha (v2.6 Alpha)...")
record = brain.run_mission("mission_alpha", profile, scenarios, world)

# 4. Verify Output (ตรวจสอบว่า Telemetry เก็บครบไหม)
print("\n✅ Mission Finished!")
print("--- DecisionRecord Details ---")
print(f"Winner: {record.selected_plan}")
print(f"World Version: {record.world_version}")
print(f"Candidates Count: {len(record.candidates)}")
print(f"Metrics (Risk): {record.simulation_metrics.get('risk')}")

# เพื่อให้ท่านเห็นโครงสร้างชัดเจน ผม Print สรุปข้อมูลทั้งหมด
print("\n--- JSON Snapshot ---")
print(json.dumps({
    "mission_id": record.mission_id,
    "selected": record.selected_plan,
    "simulation": record.simulation_metrics,
    "candidates_summary": record.candidates
}, indent=2))