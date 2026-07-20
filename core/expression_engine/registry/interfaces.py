from abc import ABC, abstractmethod
from typing import Any

class OELFunction(ABC):
    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any: pass

class OELFilter(ABC):
    @abstractmethod
    def apply(self, value: Any, *args: Any) -> Any: pass