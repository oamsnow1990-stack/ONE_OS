import numpy as np
from core.kernel.memory_service import MemoryService

# Mock LLMService สำหรับใช้ในการ Test โดยเฉพาะ
class MockLLMService:
    def get_embedding(self, text: str) -> list[float]:
        # จำลอง Vector ด้วยการสุ่มเลข (สมมติว่าเป็น Embedding)
        # ใช้ความยาว 768 เท่ากับมาตรฐานทั่วไป
        return np.random.rand(768).tolist()

def run_test():
    print("--- 🧠 Testing Memory Service (State & Semantic) ---")
    
    # 1. Initialize
    llm = MockLLMService()
    mem = MemoryService(llm)
    
    # 2. Test State Memory (Key-Value)
    print("\n[1/2] Testing State Memory...")
    mem.set("workflow_001", "status", "running")
    mem.set("workflow_001", "task", "data_cleaning")
    
    status = mem.get("workflow_001", "status")
    print(f"✅ State Retrieved: {status}")
    
    if status == "running":
        print("🎉 State Memory Test PASSED!")
    else:
        print("❌ State Memory Test FAILED!")

    # 3. Test Semantic Memory (Vector)
    print("\n[2/2] Testing Semantic Memory...")
    mem.remember("The weather in Bangkok is very hot.")
    mem.remember("The camera sensor detects motion in the living room.")
    
    # ลอง recall สิ่งที่เกี่ยวข้องกับ 'hot weather'
    results = mem.recall("Is it hot outside?")
    print(f"🔍 Semantic Recall Result: {results}")
    
    if len(results) > 0:
        print("🎉 Semantic Memory Test PASSED!")
    else:
        print("❌ Semantic Memory Test FAILED!")

if __name__ == "__main__":
    run_test()