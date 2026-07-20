from typing import Dict, Any

class FilterRegistry:
    def __init__(self):
        # สร้าง Dictionary ไว้เก็บฟิลเตอร์ต่างๆ
        self._filters: Dict[str, Any] = {}

    def register(self, name: str, filter_instance: Any):
        """ใช้สำหรับลงทะเบียนฟิลเตอร์"""
        self._filters[name] = filter_instance

    def get(self, name: str) -> Any:
        """ใช้สำหรับดึงฟิลเตอร์ออกมาใช้งาน"""
        return self._filters.get(name)