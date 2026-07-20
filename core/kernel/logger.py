from __future__ import annotations
import logging
import sys
from datetime import datetime
from enum import Enum
from typing import Any, Optional, TYPE_CHECKING
from core.kernel.base_service import BaseService

if TYPE_CHECKING:
    from .event_bus import EventBus

class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

class SystemLogger(BaseService):
    """Logger อัจฉริยะที่เชื่อมต่อกับ EventBus เพื่อทำ Real-time Telemetry"""

    def __init__(self, min_level: LogLevel = LogLevel.DEBUG):
        super().__init__("system_logger")
        self.event_bus: Optional[Any] = None
        self.min_level = min_level

    def on_initialize(self, container: Any) -> None:
        # ใช้ try-except แทนการเรียก container.has() เพื่อความยืดหยุ่น (Duck Typing)
        try:
            self.event_bus = container.get(EventBus)
        except Exception:
            self.warning("SystemLogger: ไม่พบ EventBus ใน Container, จะทำงานเฉพาะ Console Mode")

    def on_start(self) -> None:
        self.info("SystemLogger Service started.")

    def on_stop(self) -> None:
        self.info("SystemLogger Service stopped.")

    def _log(self, level: LogLevel, message: str, context: dict = None):
        if level.value < self.min_level.value:
            return

        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "level": level.name,
            "message": message,
            "context": context or {},
        }

        # 1. Console Output (เช็ค TTY เพื่อป้องกันขยะสีใน Log File)
        if sys.stdout.isatty():
            print(f"{self._get_color(level)}[{timestamp}] [{level.name}] {message}\033[0m")
        else:
            print(f"[{timestamp}] [{level.name}] {message}")

        # 2. EventBus Output
        if self.event_bus:
            try:
                self.event_bus.publish("SYSTEM_LOG", log_entry)
            except Exception as e:
                # กัน Logger ล่มเอง
                pass

    def debug(self, msg: str, ctx: dict = None): self._log(LogLevel.DEBUG, msg, ctx)
    def info(self, msg: str, ctx: dict = None): self._log(LogLevel.INFO, msg, ctx)
    def warning(self, msg: str, ctx: dict = None): self._log(LogLevel.WARNING, msg, ctx)
    def error(self, msg: str, ctx: dict = None): self._log(LogLevel.ERROR, msg, ctx)
    def critical(self, msg: str, ctx: dict = None): self._log(LogLevel.CRITICAL, msg, ctx)

    def _get_color(self, level: LogLevel) -> str:
        return {
            LogLevel.DEBUG:    "\033[94m",
            LogLevel.INFO:     "\033[92m",
            LogLevel.WARNING:  "\033[93m",
            LogLevel.ERROR:    "\033[91m",
            LogLevel.CRITICAL: "\033[95m",
        }.get(level, "\033[0m")


class _SimpleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        return f"[{ts}] [{record.levelname}] {record.getMessage()}"

def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Factory สำหรับสร้าง Logger มาตรฐาน"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_SimpleFormatter())
        logger.addHandler(handler)
        logger.propagate = False
    return logger