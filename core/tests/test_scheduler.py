from core.kernel.scheduler import Scheduler, Task
from core.kernel.service_registry import DIContainer
from core.kernel.event_bus import EventBus
from core.kernel.logger import SystemLogger, LogLevel

def test_scheduler():
    # 1. Setup ระบบ DI Container จำลองเพื่อให้ Scheduler มี Logger ใช้
    container = DIContainer()
    event_bus = EventBus()
    logger = SystemLogger(event_bus, LogLevel.DEBUG)
    container.register(logger)

    # 2. Initialize Scheduler
    scheduler = Scheduler()
    scheduler.on_initialize(container)
    scheduler.on_start()

    # 3. Schedule 5 งานที่มี Priority ต่างกัน
    # ใส่แบบสลับลำดับ เพื่อดูว่า Scheduler จะจัดระเบียบให้เราไหม
    tasks_data = [
        ("Task-1-Low", 1),
        ("Task-2-Urgent", 8),
        ("Task-3-Normal", 3),
        ("Task-4-Max", 10),
        ("Task-5-Mid", 5),
    ]

    print("\n--- 📥 Scheduling 5 Tasks ---")
    for name, prio in tasks_data:
        task = Task(id=name, priority=prio, action="execute_something")
        scheduler.schedule(task)
        print(f"Scheduled: {name} (Priority: {prio})")

    # 4. ทดสอบรันงาน (ควรจะได้ 10 -> 8 -> 5 -> 3 -> 1)
    print("\n--- 🚀 Processing Tasks (Expect Priority Descending) ---")
    
    while scheduler.get_queue_size() > 0:
        task = scheduler.run_next()
        if task:
            print(f"✅ Executed: {task.id} [Priority: {task.priority}]")

    scheduler.on_stop()
    print("\n--- 🏁 Test Complete ---")

if __name__ == "__main__":
    test_scheduler()