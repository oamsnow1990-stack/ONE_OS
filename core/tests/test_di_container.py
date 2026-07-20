from core.kernel.di_container import DIContainer
# 1. นำเข้า ServiceState ตัวจริงจาก Kernel ครับ
from core.kernel.base_service import ServiceState 

class MockService:
    def __init__(self):
        # 2. ใช้ค่าจาก ServiceState ตัวจริง
        self.state = ServiceState.CREATED 
        self.initialized = False
        self.stopped = False
        self.destroyed = False

    def initialize(self, container):
        self.initialized = True
        self.state = ServiceState.RUNNING # เปลี่ยนสถานะให้เป็น Running จริงๆ

    def stop(self):
        self.stopped = True

    def destroy(self):
        self.destroyed = True

def test_di_container():
    container = DIContainer()
    service = MockService()
    
    print("Testing Registration & Aliasing...")
    container.register("MySuperService", service)
    
    # ทดสอบดึง Service
    s1 = container.get("MySuperService")
    assert s1 == service
    print("✅ Aliasing works perfectly.")

    print("Testing Lifecycle...")
    container.resolve_and_start_all()
    
    # ตรวจสอบว่า initialize ถูกเรียกจริง
    assert service.initialized is True
    print("✅ Lifecycle management works perfectly.")

    container.stop_all()
    assert service.stopped is True
    
    container.destroy_all()
    assert service.destroyed is True
    print("✅ Full lifecycle test passed.")

if __name__ == "__main__":
    test_di_container()