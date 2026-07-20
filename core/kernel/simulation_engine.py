import random
from typing import Any, Optional, Dict
from core.models.decision_models import EvaluationResult
from core.models.world_state import WorldState
from core.kernel.base_service import BaseService
from core.utils.logger import get_logger
from core.kernel.event_bus import EventBus
from core.kernel.world_state_registry import WorldStateRegistry
from core.models.events import SystemEvent

class SimulationEngine(BaseService):
    """
    SimulationEngine ระดับ Production:
    รองรับการทำ Defensive Programming เพื่อจัดการ Payload ที่ไม่คาดคิด
    """
    def __init__(self):
        super().__init__("simulation_engine")
        self.logger = get_logger(__name__)
        self.latency_bias = 1.0
        self.difficulty_factor = 1.0 
        self.event_bus: Optional[EventBus] = None
        self.registry: Optional[WorldStateRegistry] = None

    def on_initialize(self, container: Any) -> None:
        self.event_bus = container.get(EventBus)
        self.registry = container.get(WorldStateRegistry)
        if self.event_bus:
            # ใช้ lambda เพื่อ wrap ฟังก์ชัน ป้องกันปัญหา context
            self.event_bus.subscribe("TIME_TICK", self._on_time_tick)

    def on_start(self) -> None:
        self.logger.info(f"🛠️ [SimulationEngine] ระบบพร้อมทำงาน (Difficulty: {self.difficulty_factor:.1f})")

    def set_difficulty(self, factor: float):
        self.difficulty_factor = max(1.0, factor)
        self.logger.info(f"📈 [SimulationEngine] ปรับระดับความยาก: {self.difficulty_factor:.1f}")

    def on_stop(self) -> None:
        pass

    def _on_time_tick(self, event: SystemEvent) -> None:
        """
        [Defensive Implementation] ป้องกัน Crash หาก payload ไม่ใช่ Dict
        """
        if not self.registry: return
        
        # 🟢 ป้องกัน Error: string indices must be integers
        payload = event.payload
        if isinstance(payload, str):
            # หาก payload เป็นแค่ String (เช่น "TIME_TICK") ให้ตั้งค่า default แทน
            tick_val = 0
            self.logger.debug("TIME_TICK Received non-dict payload, using default tick 0")
        else:
            tick_val = payload.get("tick", 0) if isinstance(payload, dict) else 0

        current_world = self.registry.get_current_state()
        if not current_world: return
        
        evolved_world = self.evolve(current_world)
        new_version_id = self.registry.register_state(evolved_world)
        
        if self.event_bus:
            self.event_bus.publish(
                event_type="WORLD_STATE_UPDATED",
                payload={"version_id": new_version_id, "tick": tick_val},
                priority=20
            )

    def evolve(self, world: WorldState) -> WorldState:
        """
        คำนวณการเปลี่ยนแปลงของโลก (Physics & Weather)
        """
        # 1. 🟢 ปรับสภาพอากาศ (Data Access ที่ปลอดภัย)
        # ตรวจสอบก่อนว่า world.weather เป็น dict หรือไม่
        weather_data = world.weather if isinstance(world.weather, dict) else {"condition": "sunny"}
        current_weather = weather_data.get("condition", "sunny")

        storm_weight = 0.2 * self.difficulty_factor
        sunny_weight = 0.4 / self.difficulty_factor
        cloudy_weight = 0.3
        
        new_weather = random.choices(
            ["sunny", "cloudy", "storm"], 
            weights=[sunny_weight, cloudy_weight, storm_weight], 
            k=1
        )[0]
        
        if current_weather != new_weather:
            weather_data["condition"] = new_weather
            # ถ้า world.weather เป็น object ให้ใช้ setattr หรือ dict update
            if isinstance(world.weather, dict):
                world.weather.update(weather_data)
            
            self.logger.info(f"🌍 [SimEngine] สภาพอากาศ: {new_weather} (Diff: {self.difficulty_factor:.1f})")

        # 2. 🟢 ฟิสิกส์พลังงาน (Solar & Drain System)
        # ใช้ .get เพื่อความปลอดภัย
        res = world.resources if isinstance(world.resources, dict) else {"amount": 100}
        current_energy = res.get("amount", 100)
        energy_change = -2 
        
        if new_weather == "sunny": energy_change += 8
        elif new_weather == "cloudy": energy_change += 2
        elif new_weather == "storm": energy_change -= 5

        res["amount"] = max(0, min(100, current_energy + energy_change))
        
        # เพิ่ม Tick (ต้องมั่นใจว่า world object มี attribute นี้)
        if hasattr(world, 'tick'):
            world.tick += 1
            
        return world

    def predict(self, scenario: Any, world: WorldState) -> EvaluationResult:
        # ใช้ .get เพื่อป้องกัน KeyError
        weather_cond = world.weather.get("condition", "sunny") if isinstance(world.weather, dict) else "sunny"
        res_level = world.resources.get("amount", 100) if isinstance(world.resources, dict) else 100
        
        risk_modifier = 0.3 if weather_cond == "storm" else 0.0
        cost_modifier = (100 - res_level) * 0.005 

        risk = round(min(0.9, random.uniform(0.1, 0.5) + risk_modifier), 2)
        cost = round(min(0.9, random.uniform(0.1, 0.5) + cost_modifier), 2)
        score = round(random.uniform(0.5, 1.0) - (risk + cost) / 2, 2)
        
        # ป้องกันกรณี world.devices ไม่มี (ใช้ getattr)
        devices_count = len(getattr(world, 'devices', []))
        raw_latency = 0.1 + (devices_count * 0.01)
        
        return EvaluationResult(
            scenario_id=getattr(scenario, 'id', 'unknown'),
            risk=risk, confidence=0.8, cost=cost,
            latency=round(raw_latency * self.latency_bias, 4),
            score=score
        )