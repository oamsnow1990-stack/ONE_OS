from typing import Dict
from .interfaces import OELFunction
from ..errors import RuntimeError

class FunctionRegistry:
    def __init__(self):
        # เก็บฟังก์ชันภายใต้ชื่อ key ที่เป็น string
        self._functions: Dict[str, OELFunction] = {}

    def register(self, name: str, func: OELFunction) -> None:
        """ลงทะเบียนฟังก์ชันใหม่เข้าสู่ระบบ"""
        if not isinstance(func, OELFunction):
            raise RuntimeError(f"Object {type(func)} does not implement OELFunction interface")
        self._functions[name] = func

    def get(self, name: str) -> OELFunction:
        """ดึงฟังก์ชันออกมาใช้งาน"""
        if name not in self._functions:
            raise RuntimeError(f"Function '{name}' not found in registry")
        return self._functions[name]

    def list_functions(self) -> list:
        """ดูรายการฟังก์ชันทั้งหมดที่มีในระบบ"""
        return list(self._functions.keys())