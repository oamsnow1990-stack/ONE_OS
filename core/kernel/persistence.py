import os
import json
from typing import Any, Dict
from pathlib import Path
from core.kernel.base_service import BaseService

class PersistenceService(BaseService):
    def __init__(self, data_dir: str = "data"):
        super().__init__("persistence_service")
        
        self.base_path = Path.cwd() / data_dir
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.logger = None

    def on_initialize(self, container: Any) -> None:
        self.logger = container.get("system_logger")
        if self.logger:
            self.logger.info(f"💾 [Persistence] ระบบความจำถาวรพร้อมทำงาน (Path: {self.base_path})")

    # 🟢 เพิ่มฟังก์ชันที่ BaseService บังคับให้มี
    def on_start(self):
        if self.logger:
            self.logger.info("💾 [Persistence] Service started.")

    # 🟢 เพิ่มฟังก์ชันที่ BaseService บังคับให้มี
    def on_stop(self):
        if self.logger:
            self.logger.info("💾 [Persistence] Service stopped.")

    def save(self, collection: str, data: Dict[str, Any]) -> bool:
        file_path = self.base_path / f"{collection}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            if self.logger:
                self.logger.debug(f"💾 [Persistence] บันทึก {collection}.json สำเร็จ")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ [Persistence] บันทึก {collection}.json ล้มเหลว: {str(e)}")
            return False

    def load(self, collection: str) -> Dict[str, Any]:
        file_path = self.base_path / f"{collection}.json"
        
        if not file_path.exists():
            return {}
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if self.logger:
                    self.logger.debug(f"📂 [Persistence] โหลด {collection}.json สำเร็จ")
                return data
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ [Persistence] โหลด {collection}.json ล้มเหลว: {str(e)}")
            return {}