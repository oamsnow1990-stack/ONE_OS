from typing import Dict, Any, List, Set

class StaticAnalyzer:
    """
    ตรวจสอบความถูกต้องของ Workflow ก่อนส่งให้ Runtime
    ช่วยป้องกัน Error ประหลาดๆ ระหว่างทาง (Production-Ready Guard)
    """
    
    @staticmethod
    def analyze(workflow_data: Dict[str, Any]) -> (bool, List[str]):
        errors = []
        tasks = workflow_data.get("tasks", [])
        
        # 1. ตรวจสอบข้อมูลพื้นฐาน
        if not tasks:
            errors.append("Workflow is empty: No tasks found.")
            return False, errors

        # 2. ตรวจสอบ Duplicate IDs
        ids = [t.get("id") for t in tasks if "id" in t]
        if len(ids) != len(set(ids)):
            errors.append("Validation Error: Duplicate task IDs found.")

        # 3. ตรวจสอบความถูกต้องของ Dependency (Referential Integrity)
        task_map = {t["id"]: t for t in tasks if "id" in t}
        for task in tasks:
            deps = task.get("depends_on", [])
            for dep in deps:
                if dep not in task_map:
                    errors.append(f"Validation Error: Task '{task['id']}' depends on non-existent task '{dep}'.")

        # 4. ตรวจสอบ Cycle (Circular Dependency)
        if StaticAnalyzer._has_cycle(tasks):
            errors.append("Validation Error: Circular dependency detected in workflow.")

        return len(errors) == 0, errors

    @staticmethod
    def _has_cycle(tasks: List[Dict[str, Any]]) -> bool:
        # ใช้แนวคิด DFS ในการตรวจ Loop
        graph = {t["id"]: t.get("depends_on", []) for t in tasks}
        visited = set()
        stack = set()

        def visit(node):
            if node in stack: return True
            if node in visited: return False
            stack.add(node)
            for neighbor in graph.get(node, []):
                if visit(neighbor): return True
            stack.remove(node)
            visited.add(node)
            return False

        for node in graph:
            if visit(node): return True
        return False