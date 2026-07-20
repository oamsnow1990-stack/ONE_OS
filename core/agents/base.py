from abc import ABC, abstractmethod
from core.agents.models import ExecutionContext, AgentResult

class BaseAgent(ABC):
    @property
    @abstractmethod
    def name(self) -> str: pass
        
    @abstractmethod
    def execute(self, context: ExecutionContext) -> AgentResult: pass

    # 🟢 เพิ่มฟังก์ชันเหล่านี้เพื่อให้ทุก Agent มีค่า Default (ถือว่าผ่านเสมอ)
    def validate(self, context: ExecutionContext) -> bool:
        return True

    def can_execute(self, context: ExecutionContext) -> bool:
        return True

    def undo(self, context: ExecutionContext) -> AgentResult:
        return AgentResult(status="success", output={"message": "No undo logic defined."})

    def initialize(self):
        pass