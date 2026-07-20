from core.kernel.scenario_generator import ScenarioGenerator
from core.kernel.scenario import Scenario
from unittest.mock import MagicMock

def test_scenario_validation():
    # 1. Setup Mock
    generator = ScenarioGenerator()
    
    # Mock WorldState ที่มีทรัพยากรจำกัด
    mock_world = MagicMock()
    mock_world.get_state.return_value.resources = {"battery": 20} # แบตเหลือแค่ 20%
    mock_world.get_state.return_value.devices = {"camera": "offline"}
    mock_world.get_state.return_value.user = {"status": "sleeping"}
    
    generator.world_manager = mock_world
    
    # 2. สร้าง Scenarios จำลอง
    plan_a = Scenario(
        scenario_id="A", description="High Energy", actions=[], 
        expected_outcome={}, estimated_cost=50, confidence=0.9, 
        risk_level="low", rollback_possibility=True
    )
    
    plan_b = Scenario(
        scenario_id="B", description="Vision Task", actions=[{"type": "vision_scan"}], 
        expected_outcome={}, estimated_cost=5, confidence=0.9, 
        risk_level="low", rollback_possibility=True
    )

    # 3. ทดสอบ Validator
    is_valid_a, reason_a = generator._validate_scenario(plan_a)
    is_valid_b, reason_b = generator._validate_scenario(plan_b)
    
    print(f"Scenario A (High Energy): {'FAIL' if not is_valid_a else 'PASS'} - {reason_a}")
    print(f"Scenario B (Vision Task): {'FAIL' if not is_valid_b else 'PASS'} - {reason_b}")
    
    if not is_valid_a and not is_valid_b:
        print("\n✅ SUCCESS: Validator works perfectly!")
    else:
        print("\n❌ FAILED: Validation logic missed some errors.")

if __name__ == "__main__":
    test_scenario_validation()