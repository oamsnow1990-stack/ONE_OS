from core.models.world_state import WorldState
from core.kernel.simulation_engine import SimulationEngine
from datetime import datetime

def test_world_cycle():
    # 1. ตั้งค่าโลกเริ่มต้น
    world = WorldState(
        version="2.0",
        timestamp=datetime.now(),
        environment={"location": "ZONE_A"},
        resources={"amount": 10}, # เริ่มต้นที่ 10 หน่วย
        weather={"condition": "sunny"},
        devices={},
        threats={},
        time_context={}
    )
    
    sim = SimulationEngine()
    
    print(f"🌍 [Start] ทรัพยากรเริ่มต้น: {world.resources['amount']} | สภาพอากาศ: {world.weather['condition']}")
    
    # 2. จำลองโลกหมุนไป 5 Ticks
    for i in range(1, 6):
        world = sim.evolve(world)
        print(f"⏳ [Tick {i}] ทรัพยากรเหลือ: {world.resources['amount']} | สภาพอากาศ: {world.weather['condition']}")

if __name__ == "__main__":
    test_world_cycle()