import asyncio
from typing import Any
from core.kernel.base_service import BaseService
from core.kernel.world_clock import WorldClock
from core.kernel.event_bus import EventBus
from core.utils.logger import get_logger

class WorldSimulator(BaseService):
    name = "world_simulator"

    def __init__(self):
        super().__init__(self.name)
        self.logger = get_logger(__name__)
        self.clock = None
        self.event_bus = None
        self.is_running = False

    def on_initialize(self, container: Any) -> None:
        self.clock = container.get(WorldClock)
        self.event_bus = container.get(EventBus)

    def on_start(self) -> None:
        self.logger.info("🌌 [WorldSimulator] เครื่องกำเนิดจักรวาลพร้อมทำงาน...")

    def on_stop(self) -> None:
        self.is_running = False
        self.logger.info("🛑 [WorldSimulator] หยุดการจำลองโลก...")

    async def run_loop(self, tick_interval: float = 1.0, max_ticks: int = 10):
        """
        วงล้อแห่งเวลา (Main Loop) พร้อมการป้องกันการรันซ้ำและการจัดการสถานะ
        """
        if self.is_running:
            self.logger.warning("⚠️ [WorldSimulator] Simulator กำลังทำงานอยู่แล้ว ไม่สามารถเริ่มใหม่ได้")
            return

        self.is_running = True
        self.logger.info(f"⚙️ [WorldSimulator] เริ่มหมุนวงล้อแห่งเวลา (ความเร็ว: {tick_interval}s/Tick)...")

        try:
            while self.is_running:
                # ตรวจสอบขีดจำกัด
                if max_ticks and self.clock and self.clock.current_tick >= max_ticks:
                    self.logger.info(f"🏁 [WorldSimulator] ถึงขีดจำกัดที่ {max_ticks} Ticks แล้ว. สั่งหยุดเวลา.")
                    break

                # 1. เข็มนาฬิกาขยับ
                if self.clock:
                    self.clock.tick()

                # 2. ประมวลผลเหตุการณ์
                if self.event_bus:
                    self.event_bus.process_events()

                # 3. หน่วงเวลา
                await asyncio.sleep(tick_interval)

        except asyncio.CancelledError:
            self.logger.info("⚠️ [WorldSimulator] Task ถูกยกเลิกโดยระบบ...")
            raise
        except Exception as e:
            self.logger.error(f"❌ [WorldSimulator] เกิดข้อผิดพลาดร้ายแรง: {e}")
            raise e
        finally:
            self.is_running = False
            self.logger.info("🛑 [WorldSimulator] หยุดการจำลองโลกโดยสมบูรณ์.")