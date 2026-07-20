from typing import Any, Dict, Optional

class ContextManager:
    """ระบบจัดการ Context ข้อมูลและตัวแปรที่ใช้ร่วมกันใน ONE_OS"""
    
    def __init__(self, parent_context: Optional['ContextManager'] = None):
        self._data: Dict[str, Any] = {}
        # Parent Context ช่วยให้สืบทอดตัวแปรจากระดับบน (Global) สู่ระดับล่าง (Local/Workflow) ได้
        self._parent = parent_context

    def set(self, key: str, value: Any) -> None:
        """บันทึกหรือแก้ไขค่าตัวแปรใน Context ปัจจุบัน"""
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """ดึงค่าตัวแปร ถ้าไม่มีในนี้ ให้ไปหาใน Parent Context"""
        if key in self._data:
            return self._data[key]
        if self._parent is not None:
            return self._parent.get(key, default)
        return default

    def has(self, key: str) -> bool:
        """ตรวจสอบว่ามีตัวแปรนี้อยู่หรือไม่ (รวมถึงใน Parent ด้วย)"""
        return key in self._data or (self._parent is not None and self._parent.has(key))

    def delete(self, key: str) -> None:
        """ลบตัวแปรออกจาก Context ปัจจุบัน (ไม่กระทบ Parent)"""
        if key in self._data:
            del self._data[key]
        else:
            raise KeyError(f"Key '{key}' not found in current context.")

    def clear(self) -> None:
        """ล้างข้อมูลใน Context ปัจจุบันทั้งหมด"""
        self._data.clear()

    def snapshot(self) -> Dict[str, Any]:
        """ดึงข้อมูลตัวแปรทั้งหมดออกมาเป็น Dictionary เพื่อนำไปใช้กับ OEL Evaluator"""
        result = {}
        if self._parent:
            # เอาข้อมูล Parent มาใส่ก่อน
            result.update(self._parent.snapshot())
        # เอาข้อมูลตัวเองไปทับ (Local ย่อมมีสิทธิ์สูงกว่า Global)
        result.update(self._data)
        return result