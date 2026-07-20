from typing import Any, Dict, List, Type
from .base_service import ServiceState 

class DIContainer:
    def __init__(self):
        # บังคับให้ Key ต้องเป็น Class Type เท่านั้น
        self._services: Dict[Type, Any] = {}

    def register(self, service_type: Type, instance: Any) -> None:
        """ลงทะเบียน Service ด้วย Class Type เท่านั้น"""
        if not isinstance(service_type, type):
            raise TypeError(f"❌ [DIContainer] การ Register ต้องใช้ Class Type เท่านั้น แต่ได้รับ: {type(service_type)}")
        self._services[service_type] = instance

    def get(self, service_type: Type) -> Any:
        """ดึง Service ด้วย Class Type เท่านั้น"""
        if not isinstance(service_type, type):
            raise TypeError(f"❌ [DIContainer] การ Get ต้องใช้ Class Type เท่านั้น แต่ได้รับ: {type(service_type)}")
        
        if service_type not in self._services:
            raise KeyError(f"❌ [DIContainer] Service '{service_type.__name__}' ไม่พบในระบบ!")
            
        return self._services[service_type]

    # --- เพิ่มฟังก์ชันนี้ที่นี่ (อยู่นอก destroy_all) ---
    def get_by_name(self, name: str) -> Any:
        """ดึง Service ด้วยชื่อ (String)"""
        for service in self._services.values():
            # ตรวจสอบว่า Service นั้นมี attribute name หรือไม่
            if hasattr(service, 'name') and service.name == name:
                return service
        return None
    # ---------------------------------------------

    def has_service(self, service_type: Type) -> bool:
        """เช็คว่ามี Service นี้ลงทะเบียนหรือยัง"""
        return service_type in self._services

    def _get_unique_services(self) -> List[Any]:
        return list(self._services.values())

    def resolve_and_start_all(self) -> None:
        for service in self._get_unique_services():
            if hasattr(service, 'state') and hasattr(service, 'initialize'):
                if service.state == ServiceState.CREATED:
                    service.initialize(self)

    def stop_all(self) -> None:
        for service in self._get_unique_services():
            if hasattr(service, 'stop'):
                service.stop()

    def destroy_all(self) -> None:
        for service in self._get_unique_services():
            if hasattr(service, 'destroy'):
                service.destroy()
        self._services.clear()