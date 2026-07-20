import sys
import os
# เพิ่ม path ไปที่ ONE_OS (ขึ้นไป 2 ชั้นจาก core/tests/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# กลับมาใช้ import จาก core เหมือนเดิมครับ
from core.expression_engine.engine import OELEngine
from core.expression_engine.context import ExecutionContext
from core.expression_engine.registry.interfaces import OELFunction
# 1. สร้าง Mock Function สำหรับทดสอบ
class LenFunction(OELFunction):
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        if not args:
            return 0 # ถ้าไม่มี arguments ให้คืนค่า 0
        return len(args[0])

# 2. Setup ระบบ
engine = OELEngine()
engine.functions.register("len", LenFunction())

# 3. เตรียม Context จำลอง
context = ExecutionContext(
    runtime={
        "search": {
            "output": {
                "video_ids": ["id_1", "id_2", "id_3"]
            }
        }
    }
)

# 4. ทดสอบรันคำสั่ง
expression = "{{ len(search.output.video_ids) }}"

try:
    print(f"กำลังทดสอบ Expression: {expression}")
    result = engine.run(expression, context)
    print(f"ผลลัพธ์ที่ได้: {result}")
    
    # ตรวจสอบ Type ให้แน่ใจว่าได้เป็น int ไม่ใช่ string
    print(f"Type ของผลลัพธ์: {type(result)}")
    
except Exception as e:
    print(f"❌ ทดสอบล้มเหลว: {e}")