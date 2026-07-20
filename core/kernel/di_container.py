import re
from typing import Any, Dict, Set, List
from core.kernel.base_service import ServiceState # ปรับ Path ให้ตรงกับโครงสร้างจริง

class DIContainer:
    def __init__(self):
        self._services: Dict[str, Any] = {}

    def _camel_to_snake(self, name: str) -> str:
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _generate_aliases(self, name: str) -> Set[str]:
        aliases = {
            name,
            name.lower(),
            self._camel_to_snake(name),
            name.lower().replace("_", "")
        }
        return aliases

    def register(self, key: Any, instance: Any) -> None:
        name = key.__name__ if isinstance(key, type) else str(key)
        aliases = self._generate_aliases(name)
        for alias in aliases:
            self._services[alias] = instance

    def get(self, key: Any) -> Any:
        name = key.__name__ if isinstance(key, type) else str(key)
        possible_keys = self._generate_aliases(name)
        
        for k in possible_keys:
            if k in self._services:
                return self._services[k]
                
        raise KeyError(f"Service '{key}' ไม่พบใน DI Container!")

    def _get_unique_services(self) -> List[Any]:
        return list(set(self._services.values()))

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