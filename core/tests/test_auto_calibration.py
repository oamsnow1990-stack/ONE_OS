from core.kernel.di_container import DIContainer
from core.kernel.simulation_engine import SimulationEngine
from core.kernel.telemetry_service import TelemetryService
from core.kernel.calibration_engine import CalibrationEngine
from core.kernel.reflection_engine import ReflectionEngine
from core.models.world_state import WorldState
from core.models.decision_models import DecisionRecord # ต้องนำเข้าตัวนี้ครับ

def test_calibration():
    # 1. Setup DI Container
    container = DIContainer()
    container.register("simulation_engine", SimulationEngine())
    container.register("telemetry_service", TelemetryService())
    container.register("calibration_engine", CalibrationEngine())
    container.register("reflection_engine", ReflectionEngine())

    # --- สำคัญมาก: ต้อง Initialize ทุก Service ---
    for service_name in ["simulation_engine", "telemetry_service", "calibration_engine", "reflection_engine"]:
        container.get(service_name).on_initialize(container)

    sim = container.get("simulation_engine")
    reflector = container.get("reflection_engine")
    telemetry = container.get("telemetry_service")

    # 2. จำลองภารกิจแรก
    print("🚀 [Test] รันภารกิจที่ 1 (Initial State)...")
    world = WorldState(version=1, data={})
    pred_1 = sim.predict(None, world)
    
    # ใช้ Dataclass แทน Dictionary เพื่อแก้ Error asdict()
    record = DecisionRecord(
        mission_id="TEST_001",
        world_version=1,
        profile_name="TEST",
        selected_plan="PLAN_A",
        selected_score=0.9,
        candidates=[],
        simulation_metrics={"latency": pred_1.latency}
    )
    
    telemetry.record(record)
    
    # 3. จำลองความจริง
    telemetry.update_record("TEST_001", {"actual_latency": 1.0})
    print(f"   - Simulator ทำนาย: {pred_1.latency}s | Reality: 1.0s")

    # 4. ทดสอบ Reflection
    reflector.reflect_on_mission("TEST_001")

    # 5. รันภารกิจที่ 2
    print("\n🚀 [Test] รันภารกิจที่ 2 (Post-Calibration)...")
    pred_2 = sim.predict(None, world)
    print(f"   - Simulator ทำนายใหม่: {pred_2.latency}s (ควรสูงขึ้น)")

if __name__ == "__main__":
    test_calibration()