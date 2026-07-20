# core/kernel/llm_interface.py
from abc import ABC, abstractmethod

class ILLMProvider(ABC):
    @abstractmethod
    def generate_plan(self, goal: str) -> dict:
        pass

    @abstractmethod
    def regenerate_plan(self, goal: str, error_log: str) -> dict:
        pass