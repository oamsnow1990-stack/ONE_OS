from abc import ABC, abstractmethod
from typing import Any
from .models import ExecutionContext, AgentResult
import time

class BaseAgent(ABC):
    """รากฐานของ Agent ทุกตัวในระบบ ONE_OS"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def initialize(self) -> None:
        """เตรียมความพร้อมก่อนทำงาน เช่น โหลดโมเดล หรือต่อ DB"""
        pass

    def validate(self, context: ExecutionContext) -> bool:
        """ตรวจสอบว่า Input หรือ Context ครบถ้วนพร้อมทำงานหรือไม่"""
        return True

    def can_execute(self, context: ExecutionContext) -> bool:
        """ตรวจสอบเงื่อนไขว่า Agent ตัวนี้เหมาะสมกับงานนี้หรือไม่"""
        return True

    @abstractmethod
    def execute(self, context: ExecutionContext) -> AgentResult:
        """หัวใจหลักของการทำงาน (Logic จริงๆ จะอยู่ที่นี่)"""
        pass

    def shutdown(self) -> None:
        """ทำความสะอาดหน่วยความจำ คืน Resource หลังใช้งานเสร็จ"""
        pass