import unittest
from core.kernel.kernel import ONEKernel, KernelState

class TestKernelIntegration(unittest.TestCase):
    def setUp(self):
        # สร้าง Kernel ขึ้นมาใหม่ก่อนเริ่มเทสแต่ละข้อ
        self.kernel = ONEKernel()

    def test_kernel_initialization(self):
        """เทสว่าตอนสร้าง Kernel สถานะและอุปกรณ์ต่างๆ ถูกสร้างครบไหม"""
        self.assertEqual(self.kernel.state, KernelState.OFFLINE)
        self.assertIsNotNone(self.kernel.event_bus, "EventBus should be initialized")
        self.assertIsNotNone(self.kernel.registry, "DIContainer should be initialized")

    def test_kernel_boot_sequence(self):
        """เทสว่าถ้าสั่ง start() แล้ว Kernel สามารถเปิดตัวเองไปจนถึงสถานะ READY ได้หรือไม่"""
        # ทดลองส่ง config ว่างๆ เข้าไป
        self.kernel.start(initial_config={})
        
        # หลังจาก start เสร็จ สถานะควรจะเป็น READY
        self.assertEqual(self.kernel.state, KernelState.READY)

if __name__ == "__main__":
    print("🧪 [Test] Starting Kernel Integration Tests...")
    unittest.main()