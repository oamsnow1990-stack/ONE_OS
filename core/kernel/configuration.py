from typing import Any, Dict

class ConfigurationManager:
    """ระบบโหลดและจัดเก็บการตั้งค่าระดับโครงสร้าง (System Config) ของ ONE_OS"""
    
    def __init__(self):
        self._config: Dict[str, Any] = {}

    def load_from_dict(self, config_data: Dict[str, Any]) -> None:
        """โหลดการตั้งค่าจาก Dictionary (ในอนาคตจะเปลี่ยนเป็นโหลดจาก .env หรือ JSON/YAML)"""
        self._config.update(config_data)

    def set(self, key: str, value: Any) -> None:
        """ตั้งค่าหรือแก้ไข Config แบบ Manual (Runtime)"""
        self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """ดึงการตั้งค่าออกมาใช้งาน ถ้าไม่มีให้คืนค่า Default"""
        return self._config.get(key, default)
    
    def get_nested(self, path: str, default: Any = None) -> Any:
        """ดึงการตั้งค่าแบบซ้อนทับ เช่น 'database.port'"""
        keys = path.split('.')
        current = self._config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def show_all(self) -> Dict[str, Any]:
        return self._config.copy()