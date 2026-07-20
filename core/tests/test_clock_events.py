from core.kernel.event_bus import EventBus
from core.kernel.world_clock import WorldClock
from core.models.events import SystemEvent

class MockContainer:
    """Container จำลองสำหรับใช้งานใน Unit Test แบบไม่ต้องรันทั้งระบบ"""
    def __init__(self):
        self._services = {}
    
    def register(self, cls_type, instance):
        self._services[cls_type] = instance
        
    def get(self, cls_type):
        return self._services.get(cls_type)

def test_clock_and_events():
    print("🚀 [Test] เริ่มต้นการทดสอบ WorldClock & EventBus...")
    
    # 1. สร้าง Services และ Mock Container
    container = MockContainer()
    event_bus = EventBus()
    clock = WorldClock()
    
    # ลงทะเบียน EventBus เข้า Container เพื่อให้ Clock เรียกใช้ได้
    container.register(EventBus, event_bus)
    
    # 2. Initialize & Start Services
    event_bus.on_initialize(container)
    clock.on_initialize(container)
    
    event_bus.on_start()
    clock.on_start()
    
    # 3. สร้าง Listener (ผู้ฟัง)
    def on_time_tick(event: SystemEvent):
        tick_val = event.payload.get("tick")
        print(f"🔔 [Listener] ได้ยินเสียงนาฬิกา! ตอนนี้ Tick ที่: {tick_val}")
        
    def on_emergency_event(event: SystemEvent):
        msg = event.payload.get("msg")
        print(f"🚨 [Listener] รับแจ้งเหตุฉุกเฉินขัดจังหวะ! ข้อมูล: {msg}")

    # ลงทะเบียนรับฟัง Event
    event_bus.subscribe("TIME_TICK", on_time_tick)
    event_bus.subscribe("EMERGENCY", on_emergency_event)
    
    # 4. จำลองสถานการณ์ (Simulate)
    print("\n⏳ [Simulate] ให้นาฬิกาเดินไป 3 Ticks...")
    clock.tick()
    clock.tick()
    clock.tick()
    
    print("🔥 [Simulate] เกิดเหตุแทรกแซง! มีผู้บุกรุก (Priority 0)...")
    event_bus.publish(
        event_type="EMERGENCY", 
        payload={"msg": "ตรวจพบการงัดประตูหลัง!"}, 
        priority=0  # ความสำคัญสูงสุด ต้องถูกดึงมาทำก่อน
    )
    
    # 5. สั่งให้ EventBus ประมวลผลคิวทั้งหมด
    print("\n⚙️ [Process] กำลังประมวลผล Event ใน Queue...")
    processed = event_bus.process_events()
    print(f"\n✅ [Test] ประมวลผลสำเร็จรวม {processed} เหตุการณ์!")

if __name__ == "__main__":
    test_clock_and_events()