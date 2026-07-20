import time
from core.kernel.kernel import ONEKernel

def main():
    print("--- 🌟 Initiating ONE_OS Boot Sequence 🌟 ---\n")
    
    # 1. สร้างอินสแตนซ์ของ Kernel
    kernel = ONEKernel()
    
    # 2. ทดสอบ Event Bus: จำลอง Dashboard ที่มารอดักฟัง Event จากระบบ
    def on_system_ready(payload):
        print(f"\n🎉 [Dashboard Listener] ได้รับแจ้งเตือนจาก Event Bus: KERNEL_READY! (ข้อมูล: {payload})")
        
    def on_system_error(payload):
        print(f"\n🚨 [Dashboard Listener] ระบบแจ้งเตือนข้อผิดพลาด: {payload}")

    # ลงทะเบียนดักฟัง
    kernel.event_bus.subscribe("KERNEL_READY", on_system_ready)
    kernel.event_bus.subscribe("KERNEL_ERROR", on_system_error)
    
    # 3. เตรียม Config จำลองก่อนบูต
    initial_config = {
        "database.url": "postgres://localhost:5432/one_os",
        "system.environment": "development"
    }
    
    # 4. 🚀 สั่งบูตระบบ!
    try:
        kernel.start(initial_config)
    except Exception as e:
        print(f"Boot Failed: {e}")
        return

    print("\n--- 🛠️ System Check: ทดสอบการทำงานของ Module ต่างๆ ---")
    
    # ทดสอบดึงค่าจาก Global Context
    sys_version = kernel.global_context.get("system_version")
    kernel.logger.info(f"ดึงข้อมูลจาก Context -> System Version: {sys_version}")
    
    # ทดสอบดึงค่าจาก Config
    db_url = kernel.config.get_nested("database.url")
    kernel.logger.debug(f"ดึงข้อมูลจาก Config -> Database URL: {db_url}")
    
    # ทดสอบเช็กสิทธิ์ผ่าน Permission Manager
    planner_can_propose = kernel.permissions.has_permission("AGENT_PLANNER", "propose_plan")
    kernel.logger.warning(f"เช็กสิทธิ์ -> AGENT_PLANNER เสนอแผนได้ไหม? : {planner_can_propose}")
    
    boss_can_execute = kernel.permissions.has_permission("BOSS", "format_c_drive")
    kernel.logger.critical(f"เช็กสิทธิ์ -> BOSS สั่งรันคำสั่งอันตรายได้ไหม? : {boss_can_execute}")
    
    time.sleep(1.5) # หน่วงเวลาให้เห็นว่าระบบกำลังรันอยู่
    
    print("\n--- 🛑 Initiating Shutdown Sequence ---\n")
    # 5. 💤 สั่งปิดระบบ
    kernel.stop()
    
    print("\n--- 🏁 ONE_OS Test Complete 🏁 ---")

if __name__ == "__main__":
    main()