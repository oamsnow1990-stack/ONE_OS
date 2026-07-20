import asyncio
from core.agents.base import BaseAgent
from core.agents.models import ExecutionContext, AgentResult

class PlannerAgent(BaseAgent):
    def __init__(self, container):
        self.container = container
        self.max_retries = 2

    @property
    def name(self) -> str: return "PlannerAgent"

    def execute(self, context: ExecutionContext) -> AgentResult:
        # 1. ดึง Services มาจาก Container
        llm = self.container.get("llm_service")
        runtime = self.container.get("workflow_runtime")
        ctx_engine = self.container.get("context_engine")
        skill_reg = self.container.get("skill_registry") # 🟢 เพิ่ม Skill Registry

        goal = context.input_data.get("goal", "ไม่มีเป้าหมาย")

        # 2. ⚡ [Skill-First Strategy] ลองหาในคลังก่อนเสมอ
        skill = skill_reg.find_skill(goal)
        if skill:
            context.logger.info(f"⚡ [PlannerAgent] พบ Skill ในคลัง: '{skill.name}' - นำมาใช้ซ้ำทันที!")
            # 🟢 แก้ไขบรรทัดนี้: เปลี่ยนจาก skill.workflow_template เป็น skill.template
            plan = {"workflow_id": skill.name, "steps": skill.template}
        else:
            # 3. 🧠 [LLM Fallback] ถ้าไม่เจอค่อยใช้ LLM + ContextEngine
            context.logger.info(f"🔍 [PlannerAgent] ไม่พบ Skill -> เริ่มวางแผนใหม่ด้วย LLM...")
            current_context = ctx_engine.get_planner_context(context.workflow_id, goal)
            
            retries = 0
            last_error = None
            plan = None

            while retries <= self.max_retries:
                try:
                    if retries == 0:
                        plan = llm.generate_plan(goal, context=current_context)
                    else:
                        context.logger.warning(f"🔄 [PlannerAgent] พยายามแก้ไขครั้งที่ {retries}")
                        plan = llm.regenerate_plan(goal, last_error, context=current_context)
                    break # ถ้าสำเร็จให้ออก loop
                except Exception as e:
                    last_error = str(e)
                    retries += 1
                    context.logger.error(f"❌ [PlannerAgent] แผนล้มเหลว: {last_error}")
            
            if not plan:
                return AgentResult(status="failed", error="เกินขีดจำกัดการแก้ไขแผน")

        # 4. รัน Workflow
        context.logger.info(f"📋 [PlannerAgent] ดำเนินการแผนงานรหัส: {plan.get('workflow_id')}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(runtime.execute(plan))
        loop.close()

        return AgentResult(status="success", output={"plan_executed": plan.get("workflow_id")})

    def undo(self, context: ExecutionContext) -> AgentResult:
        context.logger.info("⏪ [PlannerAgent] Undo: ยกเลิกการวางแผน")
        return AgentResult(status="success", output={})