from abc import ABC, abstractmethod
from typing import Any
from enum import Enum
from core.utils.logger import get_logger

class ServiceState(Enum):
    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    DESTROYED = "DESTROYED"

class BaseService(ABC):
    def __init__(self, name: str):
        self.name = name
        self.state = ServiceState.CREATED
        self.logger = get_logger(self.name) # ใช้ logger ของตัวเอง
        self.dependencies = []

    def initialize(self, container: Any) -> None:
        if self.state != ServiceState.CREATED:
            self.logger.warning(f"[{self.name}] พยายาม Init ซ้ำ!")
            return
            
        self.state = ServiceState.INITIALIZING
        self.on_initialize(container)
        
        self.state = ServiceState.STARTING
        self.on_start()
        
        self.state = ServiceState.RUNNING
        self.logger.info(f"[{self.name}] Service รันสมบูรณ์")

    def stop(self) -> None:
        if self.state != ServiceState.RUNNING:
            return
            
        self.state = ServiceState.STOPPING
        self.on_stop()
        self.state = ServiceState.STOPPED

    @abstractmethod
    def on_initialize(self, container: Any) -> None: pass

    @abstractmethod
    def on_start(self) -> None: pass

    @abstractmethod
    def on_stop(self) -> None: pass