import unittest
from core.kernel.reasoning_engine import ReasoningEngine

class MockReasoningEngine(ReasoningEngine):
    def __init__(self):
        # 1. เรียก super() แบบว่างๆ เพื่อหลีกเลี่ยง Argument Error
        super().__init__()
        
        # 2. กำหนดค่า name ให้กับ Instance โดยตรง (ถ้าคลาสแม่ต้องการ)
        # ถ้ายังติด Error เรื่อง name อีก ให้ลองเอาบรรทัดนี้ออกครับ
        self.name = "TestReasoningEngine"
        
    def on_initialize(self): pass
    def on_start(self): pass
    def on_stop(self): pass

class TestReasoningEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MockReasoningEngine()
        self.thresholds = {"SAFE": 0.60, "AGGRESSIVE": 0.85}

    def test_emergency_crisis(self):
        strategy, reason = self.engine.select_strategy(100, "sunny", 0.9, self.thresholds, is_crisis=True)
        self.assertEqual(strategy, "EMERGENCY_MODE")

    def test_energy_depletion(self):
        strategy, reason = self.engine.select_strategy(0, "sunny", 0.9, self.thresholds, is_crisis=False)
        self.assertEqual(strategy, "SYSTEM_SLEEP")

    def test_low_battery_eco_mode(self):
        strategy, reason = self.engine.select_strategy(15, "sunny", 0.9, self.thresholds, is_crisis=False)
        self.assertEqual(strategy, "ECO-MODE")

    def test_storm_weather_safety(self):
        strategy, reason = self.engine.select_strategy(50, "storm", 0.9, self.thresholds, is_crisis=False)
        self.assertEqual(strategy, "SAFE_MODE")

    def test_aggressive_performance(self):
        # Confidence 0.9 > 0.85
        strategy, reason = self.engine.select_strategy(50, "sunny", 0.9, self.thresholds, is_crisis=False)
        self.assertEqual(strategy, "AGGRESSIVE_MODE")

    def test_safe_mode_low_confidence(self):
        # Confidence 0.4 < 0.60
        strategy, reason = self.engine.select_strategy(50, "sunny", 0.4, self.thresholds, is_crisis=False)
        self.assertEqual(strategy, "SAFE_MODE")

    def test_normal_stable_operation(self):
        # Confidence 0.7 (กลางๆ)
        strategy, reason = self.engine.select_strategy(50, "sunny", 0.7, self.thresholds, is_crisis=False)
        self.assertEqual(strategy, "NORMAL_MODE")

if __name__ == "__main__":
    print("🧪 [Test] Starting ReasoningEngine Unit Tests...")
    unittest.main()