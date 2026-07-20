from typing import Dict, Any

class ContextEngine:
    def __init__(self, memory_service, world_model_service, goal_manager_service):
        self.memory = memory_service
        self.world_model = world_model_service
        self.goal_manager = goal_manager_service # เพิ่มบรรทัดนี้

    def get_planner_context(self, workflow_id: str, query: str) -> Dict[str, Any]:
        """
        รวบรวมข้อมูลจากทุก Service รวมถึง Goal เพื่อสร้าง Context ให้ Planner
        """
        # 1. ดึงสถานะงานปัจจุบันจาก Memory
        current_state = self.memory.get(workflow_id, "state", "idle")
        
        # 2. ดึงความทรงจำ
        relevant_memories = self.memory.recall(query, top_k=2)
        
        # 3. ดึงสถานะของโลก
        world_context = self.world_model.get_context_for_planner(query)
        
        # 4. ดึงสถานะเป้าหมาย (จาก Goal Manager)
        goal_context = self.goal_manager.get_goal_context() # เพิ่มบรรทัดนี้
        
        return {
            "workflow_id": workflow_id,
            "state": current_state,
            "recent_experience": [mem[0] for mem in relevant_memories],
            "world_context": world_context,
            "goal_status": goal_context, # เพิ่ม Goal ลงใน Context
            "timestamp": "2026-07-17"
        }