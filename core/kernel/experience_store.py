from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, List, Optional, Dict
import sqlite3
import os
import uuid
import threading
from datetime import datetime
from core.kernel.base_service import BaseService

class ExperienceType(Enum):
    MEMORY = "MEMORY"
    LEARNING = "LEARNING"
    KNOWLEDGE = "KNOWLEDGE"
    ACTION = "ACTION"
    SYSTEM = "SYSTEM"

@dataclass
class Experience:
    mission: str
    weather: str
    confidence: float
    resources: float
    plan_id: str
    exp_type: ExperienceType = ExperienceType.MEMORY

# --- แก้ไข: ดึง class นี้ออกมาข้างนอกครับ ---
class ExperienceStore(BaseService):
    def __init__(self, db_path: str = "memory/experiences.db"):
        super().__init__("experience_store")
        self._db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        self._lock = threading.Lock()

    def on_initialize(self, container: Any) -> None:
        try:
            os.makedirs(os.path.dirname(self._db_path) or ".", exist_ok=True)
            self.conn = sqlite3.connect(self._db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self._init_schema()
            self.logger.info(f"💾 [ExperienceStore] Database พร้อมใช้งานที่: {self._db_path}")
        except Exception as e:
            self.logger.error(f"❌ [ExperienceStore] Init failed: {e}")

    def on_start(self) -> None:
        self.logger.info("ExperienceStore started.")

    def on_stop(self) -> None:
        with self._lock:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.logger.info("ExperienceStore stopped.")

    def _init_schema(self) -> None:
        with self._lock:
            self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id TEXT PRIMARY KEY,
                    mission TEXT,
                    weather TEXT,
                    confidence REAL,
                    resources REAL,
                    plan_id TEXT,
                    exp_type TEXT,
                    created_at TIMESTAMP
                );
            """)
            self.conn.commit()

    def save(self, data: Dict[str, Any]) -> None:
        """บันทึกประสบการณ์โดยรับเป็น Dictionary หรือ Object"""
        with self._lock:
            try:
                exp_id = str(uuid.uuid4())
                self.conn.execute(
                    """INSERT INTO experiences (id, mission, weather, confidence, resources, plan_id, exp_type, created_at) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        exp_id, 
                        data.get('mission', 'unknown'),
                        data.get('weather', 'unknown'),
                        data.get('confidence', 0.0),
                        data.get('resources', 0.0),
                        data.get('plan_id', 'UNKNOWN'),
                        str(data.get('exp_type', 'MEMORY')),
                        datetime.now().isoformat()
                    )
                )
                self.conn.commit()
            except sqlite3.Error as e:
                self.logger.error(f"❌ [DB Error]: {e}")

    def get_best_plan_for_context(self, context: str) -> Optional[str]:
        """ค้นหา plan_id ที่ดีที่สุด (Confidence สูงสุด) สำหรับภารกิจนั้นๆ"""
        with self._lock:
            cursor = self.conn.execute(
                "SELECT plan_id FROM experiences WHERE mission = ? ORDER BY confidence DESC LIMIT 1",
                (context,)
            )
            row = cursor.fetchone()
            return row['plan_id'] if row else None

    def get_contextual_stats(self) -> Dict[str, Any]:
        """สรุปสถิติประสบการณ์ทั้งหมด"""
        with self._lock:
            cursor = self.conn.execute("SELECT COUNT(*) as total, AVG(confidence) as avg_conf FROM experiences")
            row = cursor.fetchone()
            return {"total_records": row['total'], "average_confidence": round(row['avg_conf'] or 0, 2)}

    def get_recent_success_rates(self, limit: int = 10) -> float:
        """คำนวณอัตราความสำเร็จจากประสบการณ์ล่าสุด"""
        with self._lock:
            cursor = self.conn.execute(
                "SELECT AVG(confidence) as success_rate FROM (SELECT confidence FROM experiences ORDER BY created_at DESC LIMIT ?)",
                (limit,)
            )
            row = cursor.fetchone()
            return round(row['success_rate'] or 0.0, 2)