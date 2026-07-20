import os
import shutil
from core.kernel.telemetry_service import TelemetryService
from core.models.decision_models import DecisionRecord, EvaluationResult

def run_telemetry_test():
    print("🧪 Starting Telemetry Service Test...")
    
    # 1. Setup (ใช้โฟลเดอร์แยกเพื่อไม่ให้ปนกับข้อมูลจริง)
    test_dir = "data/telemetry_test"
    service = TelemetryService(log_dir=test_dir)
    
    # 2. เตรียม Mock Data
    record = DecisionRecord(
        mission_id="MISSION_TEST_999",
        world_version=99,
        profile_name="TEST_PROFILE",
        selected_plan="Plan_X",
        selected_score=0.95,
        candidates=[{"plan": "Plan_X", "score": 0.95}, {"plan": "Plan_Y", "score": 0.5}],
        simulation_metrics={"risk": 0.05, "confidence": 0.95, "cost": 0.1, "latency": 0.1}
    )
    
    # 3. Test Writing
    print("📝 Writing test record...")
    service.record(record)
    
    # 4. Test Reading
    print("🔍 Reading test record...")
    found_record = service.get_record("MISSION_TEST_999")
    
    if found_record and found_record.get("mission_id") == "MISSION_TEST_999":
        print("✅ Success: Telemetry Read/Write verified.")
        print(f"   Data Verification: Selected Plan = {found_record.get('selected_plan')}")
    else:
        print("❌ Failed: Record not found or corrupted.")
        
    # 5. Cleanup (ลบไฟล์ทดสอบทิ้ง)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
        print("🧹 Cleanup: Test directory removed.")

if __name__ == "__main__":
    run_telemetry_test()