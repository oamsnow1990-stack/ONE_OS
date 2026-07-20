from typing import List, Dict, Any

class DAGBuilder:
    """
    สร้าง Graph ของ Task และจัดลำดับการรันแบบ Layered
    เพื่อรองรับ Parallel Execution
    """
    
    @staticmethod
    def build(tasks: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        # 1. เตรียมข้อมูล
        task_map = {t['id']: t for t in tasks}
        graph = {t['id']: [] for t in tasks}
        in_degree = {t['id']: 0 for t in tasks}

        # 2. สร้าง Graph และนับจำนวน Dependency (In-degree)
        for task in tasks:
            task_id = task['id']
            deps = task.get("depends_on", [])
            
            for dep in deps:
                if dep not in task_map:
                    raise ValueError(f"Dependency Error: Task '{task_id}' depends on non-existent task '{dep}'")
                
                # ถ้า dep -> task_id แสดงว่า task_id ต้องรอ dep
                graph[dep].append(task_id)
                in_degree[task_id] += 1

        # 3. จัดกลุ่มเป็น Layer (Queue-based layering)
        # ชั้นที่ 0 คือ task ที่ไม่มี dependency (รันได้เลย)
        layers = []
        queue = [tid for tid in in_degree if in_degree[tid] == 0]

        if not queue and tasks:
            raise ValueError("Cycle detected: Workflow has no entry point (Circular dependency).")

        while queue:
            # เพิ่มชั้นปัจจุบันเข้าไป
            current_layer = [task_map[tid] for tid in queue]
            layers.append(current_layer)
            
            # เตรียม Layer ถัดไป
            next_queue = []
            for tid in queue:
                for neighbor in graph[tid]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        next_queue.append(neighbor)
            queue = next_queue

        # 4. ตรวจสอบ Cycle (ถ้า tasks ใน layers ไม่ครบตามจำนวน task เดิม แสดงว่าติด Loop)
        total_tasks_sorted = sum(len(layer) for layer in layers)
        if total_tasks_sorted != len(tasks):
            raise ValueError("Cycle detected: Workflow contains circular dependencies.")

        return layers