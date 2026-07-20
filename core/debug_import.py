import sys
import traceback

try:
    print("กำลังพยายามโหลด WorldSimulator...")
    from core.kernel.world_simulator import WorldSimulator
    print("✅ โหลดสำเร็จ! คลาส WorldSimulator ถูกพบแล้ว")
except Exception as e:
    print("❌ โหลดไม่สำเร็จ! นี่คือสาเหตุที่แท้จริง:")
    traceback.print_exc()