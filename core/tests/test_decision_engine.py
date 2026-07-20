from core.kernel.decision_engine import DecisionEngine
from core.models.decision_models import MissionProfile, EvaluationResult

def test_decision_engine():
    engine = DecisionEngine()
    
    # 1. นิยาม Profiles
    emergency_profile = MissionProfile("EMERGENCY", 0.55, 0.25, 0.05, 0.15)
    business_profile  = MissionProfile("BUSINESS", 0.20, 0.30, 0.40, 0.10)
    
    # 2. เตรียม Scenarios
    # Plan A: Risk ต่ำมาก (เหมาะกับ Emergency)
    # Plan B: Cost ต่ำมาก (เหมาะกับ Business)
    scenarios = [
        EvaluationResult("Plan_A", risk=0.1, confidence=0.8, cost=0.5, latency=0.5),
        EvaluationResult("Plan_B", risk=0.6, confidence=0.7, cost=0.1, latency=0.5),
        EvaluationResult("Plan_C", risk=0.4, confidence=0.5, cost=0.4, latency=0.5),
    ]
    
    print("--- Testing EMERGENCY Profile ---")
    record_em = engine.decide("mission_001", scenarios, emergency_profile)
    print(f"Winner: {record_em.winner.scenario_id} (Score: {record_em.winner.score})")
    assert record_em.winner.scenario_id == "Plan_A", "Emergency should pick Low Risk Plan A"
    
    print("\n--- Testing BUSINESS Profile ---")
    record_biz = engine.decide("mission_002", scenarios, business_profile)
    print(f"Winner: {record_biz.winner.scenario_id} (Score: {record_biz.winner.score})")
    assert record_biz.winner.scenario_id == "Plan_B", "Business should pick Low Cost Plan B"
    
    print("\n✅ Decision Engine Logic Passed!")

if __name__ == "__main__":
    test_decision_engine()