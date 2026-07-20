from typing import Any, Dict
from core.kernel.base_service import BaseService
from core.utils.logger import get_logger

class TelemetryService(BaseService):
    name = "telemetry_service"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)

    def on_initialize(self, container: Any) -> None:
        pass

    def on_start(self) -> None:
        self.logger.info("📡 [TelemetryService] NASA Control Room พร้อมแสดงผล")

    def on_stop(self) -> None:
        pass

    def render_control_room(self, tick: int, snapshot: Dict[str, Any]):
        """สร้าง UI Control Room บน Console (Reasoning Trace)"""
        print(f"\n" + "═"*65)
        print(f" 🚀 ONE OS v3 - NASA CONTROL ROOM  [ TICK: {tick} ] ")
        print("═"*65)
        
        # 1. World State
        world = snapshot.get("world", {})
        weather_icon = "🌩️" if world.get("weather") == "storm" else ("☁️" if world.get("weather") == "cloudy" else "☀️")
        print(f" 🌍 [WORLD STATE]   Weather: {world.get('weather').upper()} {weather_icon} | Energy: {world.get('resources')}%")
        
        # 2. Memory Recall
        mem = snapshot.get("memory_recall", {})
        print(f" 💾 [MEMORY RECALL] Context ({mem.get('context').upper()}): Ratios {mem.get('avg_success')*100:.1f}% Success (จาก {mem.get('count')} Records)")
        
        # 3. Cognitive State
        cog = snapshot.get("cognitive", {})
        print(f" 🧠 [COGNITIVE]     Mode: {cog.get('mode')} | Reason: {cog.get('reason')}")
        
        # 4. Calibration & Breakdown
        brk = snapshot.get("confidence_breakdown", {})
        cal = snapshot.get("calibration", {})
        print(f" ⚖️ [CALIBRATION]   Error Bias: {cal.get('last_error'):.4f}")
        print(f" 📊 [WEIGHTS]       Hist: {brk.get('history',0):.2f} | Ctx: {brk.get('context',0):.2f} | Err: {brk.get('prediction_error',0):.2f}")
        
        # 5. Execution Decision
        dec = snapshot.get("decision", {})
        print(f" 🎯 [EXECUTION]     Plan: {dec.get('plan')} | Final Confidence: {dec.get('confidence'):.2f}")
        print("═"*65 + "\n")