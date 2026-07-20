print("DEBUG: กำลังเริ่มรันไฟล์ test_world_model.py...")

from core.kernel.world_model_service import WorldModelService

def run_test():
    print("--- 🧠 Testing World Model Service (Advanced Query) ---")
    
    # 1. Initialize Service
    wm = WorldModelService()
    
    # 2. Add Entities
    wm.add_entity("house", "structure")
    wm.add_entity("living_room", "room", {"floor": 1})
    wm.add_entity("camera_01", "device", {"brand": "xiaomi"})
    # แก้ไข: เปลี่ยนจาก "type": "motion" เป็น "capability": "motion"
    wm.add_entity("sensor_01", "sensor", {"capability": "motion"}) 
    
    # 3. Add Relationships
    wm.add_relationship("living_room", "house", "located_in")
    wm.add_relationship("camera_01", "living_room", "located_in")
    wm.add_relationship("sensor_01", "living_room", "located_in")
    
    print("✅ Entities and Relationships added successfully.")
    
    # 4. Test Basic Queries
    devices = wm.get_devices_in_room("living_room")
    print(f"🔍 Found devices in 'living_room': {devices}")
    
    # 5. Test Advanced Query (ใหม่)
    print("\n--- 🔍 Testing Advanced Queries ---")
    # ค้นหา Sensor ทั้งหมดที่มี capability เป็น "motion"
    motion_sensors = wm.query_entities("sensor", capability="motion")
    print(f"🎯 Sensors with 'motion' capability: {motion_sensors}")
    
    if "sensor_01" in motion_sensors:
        print("✅ Advanced Query Test PASSED!")
    else:
        print("❌ Advanced Query Test FAILED!")

if __name__ == "__main__":
    run_test()