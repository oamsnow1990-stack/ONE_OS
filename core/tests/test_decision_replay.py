from core.kernel.di_container import DIContainer
from core.kernel.telemetry_service import TelemetryService
from core.kernel.simulation_engine import SimulationEngine
from core.kernel.replay_engine import ReplayEngine
from core.models.decision_models import DecisionRecord

def test_decision_replay():
    container = DIContainer()
    container.register("telemetry_service", TelemetryService())
    container.register("simulation_engine", SimulationEngine())
    container.register("replay_engine", ReplayEngine())

    # Initialize ทุก service
    for s in ["telemetry_service", "simulation_engine", "replay_engine"]:
        container.get(s).on_initialize(container)

    telemetry = container.get("telemetry_service")
    replay = container.get("replay_engine")

    # 1. จำลอง "อดีต" (สร้าง DecisionRecord ที่มี Snapshot โลก)
    past_record = DecisionRecord(
        mission_id="HIST_001",
        world_version=15,
        profile_name="ROUTINE",
        selected_plan="PLAN_A",
        selected_score=0.9,
        world_snapshot={"battery": 80, "weather": "clear"}, # <--- สภาพโลกในอดีต
        simulation_metrics={"latency": 0.5}
    )
    telemetry.record(past_record.to_dict())

    # 2. รัน Replay (What-if Analysis)
    print("🚀 [Test] เริ่มทำ What-if Analysis...")
    result = replay.replay_mission("HIST_001", "PLAN_B")
    
    print(f"\n✅ ผลลัพธ์ Replay: หากเลือก PLAN_B ในตอนนั้น")
    print(f"   - Latency คาดการณ์: {result.latency}s")
    print(f"   - ความมั่นใจ: {result.confidence}")

if __name__ == "__main__":
    test_decision_replay()