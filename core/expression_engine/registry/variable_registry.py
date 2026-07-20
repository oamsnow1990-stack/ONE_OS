from typing import Any, Dict, Optional

class VariableRegistry:
    def __init__(self):
        # เก็บตัวแปรต่างๆ ไว้ใน Dictionary
        self._variables: Dict[str, Any] = {}

    def set(self, name: str, value: Any):
        """กำหนดค่าตัวแปร"""
        self._variables[name] = value

    def get(self, name: str) -> Optional[Any]:
        """ดึงค่าตัวแปร"""
        return self._variables.get(name)

    def has(self, name: str) -> bool:
        """ตรวจสอบว่ามีตัวแปรนี้ไหม"""
        return name in self._variables

    def update(self, data: Dict[str, Any]):
        """อัปเดตข้อมูลชุดใหญ่ (เช่น การ Load Context ทั้งหมดเข้ามา)"""
        self._variables.update(data)