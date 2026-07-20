from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
from .base_service import BaseService, ServiceState
from core.kernel.event_bus import EventBus

@dataclass
class HealthStatus:
    status: str = "HEALTHY"  # HEALTHY, DEGRADED, CRITICAL
    latency_ms: float = 0.0
    cpu_usage: float = 0.0
    memory_mb: float = 0.0
    last_heartbeat: datetime = field(default_factory=datetime.now)

class HealthMonitor(BaseService):
    """
    ระบบเฝ้าระวังสุขภาพของทุก Service ใน ONE_OS
    (ทำหน้าที่รวบรวม Metrics และตรวจสอบว่า Service ไหนตายหรือยัง)
    """
    def __init__(self):
        super().__init__("health_monitor")
        self.registry: Dict[str, HealthStatus] = {}
        self.event_bus = None # ประกาศไว้ล่วงหน้าเพื่อป้องกัน Attribute Error

    def on_initialize(self, container: Any) -> None:
        # 🟢 [แก้ไขแล้ว] เปลี่ยนมาใช้ Type-Based DI ตามมาตรฐานใหม่!
        self.event_bus = container.get(EventBus)

    def on_start(self) -> None:
        # เริ่มต้น Monitor
        pass

    def on_stop(self) -> None:
        pass

    def update_metrics(self, service_name: str, cpu: float, mem: float, latency: float) -> None:
        """รับข้อมูลจาก Service ต่างๆ"""
        status = "HEALTHY"
        if latency > 500 or cpu > 90: # ตัวอย่าง Threshold
            status = "DEGRADED"
        
        self.registry[service_name] = HealthStatus(
            status=status,
            latency_ms=latency,
            cpu_usage=cpu,
            memory_mb=mem,
            last_heartbeat=datetime.now()
        )
        
        if status == "DEGRADED":
            # ตรวจสอบก่อนเผื่อ EventBus ยังไม่พร้อม
            if self.event_bus: 
                self.event_bus.publish("SYSTEM_WARNING", {"service": service_name, "issue": "High Latency/Load"})

    def get_report(self) -> Dict[str, HealthStatus]:
        return self.registry
    
    def is_healthy(self) -> bool:
        # ตรวจสอบว่ามี Service ไหนอยู่ในสถานะ CRITICAL หรือไม่
        for service_name, data in self.registry.items():
            if data.status == "CRITICAL":
                return False
        return True