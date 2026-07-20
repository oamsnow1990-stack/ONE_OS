from core.kernel.skill_registry_service import SkillRegistryService
from core.agents.models import Skill
from typing import Dict, Any

def planner_logic(goal: str, registry: SkillRegistryService, llm_mock: Any) -> Dict[str, Any]:
    """จำลองการตัดสินใจของ Planner ที่มองหา Skill ก่อน"""
    print(f"🧠 [Planner] ได้รับคำสั่ง: '{goal}'")
    
    # 1. ค้นหาใน Skill Library ก่อน
    skill = registry.find_skill(goal)
    
    if skill:
        print(f"⚡ [Planner] พบ Skill ในคลัง: '{skill.name}' -> ใช้ซ้ำทันที!")
        return {"status": "success", "source": "skill_library", "plan": skill.workflow_template}
    
    # 2. ถ้าไม่เจอ ให้ LLM วางแผนใหม่
    print(f"🔍 [Planner] ไม่พบ Skill -> ส่งให้ LLM วางแผนใหม่")
    return {"status": "success", "source": "llm_planner", "plan": llm_mock.generate_plan(goal)}

# Mock LLM สำหรับ Fallback
class MockLLM:
    def generate_plan(self, goal): return [{"agent": "GeneralAgent", "action": "Analyze"}]

# --- การทดสอบ ---
def run_test():
    registry = SkillRegistryService()
    # Mock Logger ให้ registry
    class MockLogger:
        def info(self, msg): print(f"Log: {msg}")
    registry.on_initialize({"system_logger": MockLogger()})

    # 1. สร้างและลงทะเบียน Mock Skill
    security_skill = Skill(
        name="security_sweep",
        description="Perform a full security check of the house",
        preconditions={"state": "idle"},
        workflow_template=[{"agent": "SecurityAgent", "task": "full_sweep"}]
    )
    registry.register_skill(security_skill)

    # 2. ทดสอบกรณีที่ 1: มี Skill (ความเร็วสูง)
    print("\n--- Test Case 1: หาเจอในคลัง ---")
    plan1 = planner_logic("security sweep", registry, MockLLM())
    print(f"ผลลัพธ์: {plan1}")

    # 3. ทดสอบกรณีที่ 2: ไม่มี Skill (ต้องใช้ LLM)
    print("\n--- Test Case 2: หาไม่เจอในคลัง ---")
    plan2 = planner_logic("make coffee", registry, MockLLM())
    print(f"ผลลัพธ์: {plan2}")

if __name__ == "__main__":
    run_test()