from dataclasses import dataclass, field
from typing import Dict, Any, List
import time

@dataclass
class DecisionRecord:
    mission_id: str
    decision: str
    reason: str
    rejected: List[Dict[str, Any]]
    what_if: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

@dataclass
class TelemetryRecord:
    mission_id: str
    profile: str
    world_version: int
    simulation: Dict[str, Any]
    execution: Dict[str, Any]
    decision_journal: DecisionRecord
    result: str # SUCCESS / FAIL