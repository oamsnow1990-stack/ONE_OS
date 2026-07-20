import os
import glob
import shutil
from core.kernel.di_container import DIContainer
from core.kernel.telemetry_service import TelemetryService
from core.kernel.telemetry_models import TelemetryRecord, DecisionRecord

# 1. Mock คลาสเพื่อจำลอง ExecutiveBrain
class MockExecutiveBrain:
    def __init__(self, container):
        self.telemetry = container.get("telemetry_service")
    
    def run_mission_mock(self):
        # จำลองการบันทึก telemetry หลังจากรันภารกิจ
        record = TelemetryRecord(
            mission_id="test_mission_001",
            profile="Emergency",
            world_version=1,
            simulation={"risk": 0.1},
            execution={"status": "SUCCESS"},
            decision_journal=DecisionRecord(
                mission_id="test_mission_001",
                decision="Scenario_B",
                reason="Testing Integration",
                rejected=[],
                what_if={}
            ),
            result="SUCCESS"
        )
        self.telemetry.record(record)

def test_telemetry_file_creation():
    # Setup
    log_dir = "data/telemetry"
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir) # ล้างไฟล์เก่าก่อนเริ่ม
        
    container = DIContainer()
    container.register("telemetry_service", TelemetryService(log_dir=log_dir))
    
    # Run
    brain = MockExecutiveBrain(container)
    brain.run_mission_mock()
    
    # Verify
    files = glob.glob(os.path.join(log_dir, "*.jsonl"))
    
    print(f"DEBUG: Found files: {files}")
    
    if len(files) > 0:
        print("✅ SUCCESS: Telemetry file created!")
        # ตรวจสอบเนื้อหาภายใน
        with open(files[0], "r", encoding="utf-8") as f:
            content = f.read()
            if "test_mission_001" in content:
                print("✅ SUCCESS: Content verified!")
            else:
                print("❌ FAILED: File content mismatch.")
    else:
        print("❌ FAILED: No telemetry file found.")

if __name__ == "__main__":
    test_telemetry_file_creation()