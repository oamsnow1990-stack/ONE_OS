from core.kernel.di_container import DIContainer
from core.kernel.confidence_engine import ConfidenceEngine

def test_confidence_learning():
    # 1. Setup DIContainer
    container = DIContainer()
    container.register("confidence_engine", ConfidenceEngine())
    
    # 2. Initialize
    conf_engine = container.get("confidence_engine")
    conf_engine.on_start()
    
    print("🚀 [Test] เริ่มรันภารกิจชุดทดสอบความมั่นใจ (Learning Curve)...")
    print("สถานะ: ระบบจะเรียนรู้ว่าตัวเองเก่งขึ้นเรื่อยๆ ตามภารกิจที่ผ่านไป\n")

    # 3. จำลองการรันภารกิจ 3 รอบ
    # สมมติว่าในแต่ละรอบ ระบบทำผลงานได้ดีขึ้นเรื่อยๆ
    accuracies = [0.85, 0.90, 0.95]
    
    for i, acc in enumerate(accuracies):
        # Update metrics จำลองจาก ReflectionEngine
        conf_engine.update_metrics("EMERGENCY", accuracy=acc, success=True)
        
        # ดึง Score ล่าสุด
        score = conf_engine.get_confidence_score("EMERGENCY")
        print(f"   - รอบที่ {i+1}: ทำผลงานได้แม่นยำ {acc*100:.0f}% | Confidence Score ปัจจุบัน = {score:.2f}")

    print("\n✅ [System] การเรียนรู้เสร็จสิ้น")
    if conf_engine.get_confidence_score("EMERGENCY") > 0.8:
        print("💡 ผลการวิเคราะห์: ระบบมีความมั่นใจสูง! (พร้อมสลับไปใช้แผน Aggressive)")

if __name__ == "__main__":
    test_confidence_learning()