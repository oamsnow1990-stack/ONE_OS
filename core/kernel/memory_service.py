import numpy as np
from typing import Any, Dict, List, Tuple
from core.kernel.base_service import BaseService

class MemoryService(BaseService):
    def __init__(self, llm_service):
        super().__init__("memory_service")
        self.llm_service = llm_service
        
        # 1. State Memory (Key-Value)
        self._kv_store: Dict[str, Dict[str, Any]] = {}
        
        # 2. Semantic Memory (Vector Store)
        self.memory_db: List[Dict[str, Any]] = [] 

    # --- Lifecycle Methods ---
    def on_initialize(self, container: Any) -> None:
        pass 

    def on_start(self) -> None:
        pass

    def on_stop(self) -> None:
        self._kv_store.clear()
        self.memory_db.clear()

    # --- Section 1: State Memory (Key-Value) ---
    def set(self, workflow_id: str, key: str, value: Any):
        if workflow_id not in self._kv_store:
            self._kv_store[workflow_id] = {}
        self._kv_store[workflow_id][key] = value

    def get(self, workflow_id: str, key: str, default: Any = None) -> Any:
        return self._kv_store.get(workflow_id, {}).get(key, default)

    def clear_state(self, workflow_id: str):
        if workflow_id in self._kv_store:
            del self._kv_store[workflow_id]

    # --- Section 2: Semantic Memory (Vector) ---
    def remember(self, text: str):
        """แปลงข้อความเป็น Vector แล้วเก็บเข้า Memory"""
        embedding = self.llm_service.get_embedding(text)
        self.memory_db.append({
            "text": text,
            "vector": np.array(embedding)
        })

    def recall(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """ค้นหาข้อความที่ใกล้เคียงที่สุดด้วย Cosine Similarity"""
        if not self.memory_db:
            return []

        query_vec = np.array(self.llm_service.get_embedding(query))
        
        results = []
        for mem in self.memory_db:
            # คำนวณ Cosine Similarity
            # Formula: (A . B) / (||A|| * ||B||)
            dot_product = np.dot(query_vec, mem["vector"])
            norm_a = np.linalg.norm(query_vec)
            norm_b = np.linalg.norm(mem["vector"])
            
            if norm_a == 0 or norm_b == 0:
                similarity = 0
            else:
                similarity = dot_product / (norm_a * norm_b)
            
            results.append((mem["text"], float(similarity)))
            
        # เรียงลำดับจากความเหมือนมากไปน้อย
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]