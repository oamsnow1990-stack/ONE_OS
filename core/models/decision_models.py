import time
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from .enums import RejectedReason

@dataclass
class MissionProfile:
    name: str
    risk_tolerance: float    # ความกล้าเสี่ยง
    resource_priority: float # ความสำคัญของทรัพยากร
    time_sensitivity: float  # ความสำคัญของเวลา (แทนที่ latency_weight)
    cost_efficiency: float   # ความสำคัญของความคุ้มค่า (แทนที่ cost_weight)

@dataclass
class EvaluationResult:
    scenario_id: str
    risk: float
    confidence: float
    cost: float
    latency: float
    score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DecisionRecord:
    mission_id: str
    world_version_id: str 
    profile_name: str
    selected_plan: str
    selected_score: float
    reasoning: Dict[str, Any] = field(default_factory=dict)
    world_snapshot: Dict[str, Any] = field(default_factory=dict)
    candidates: List[Dict[str, Any]] = field(default_factory=list)
    simulation_metrics: Dict[str, Any] = field(default_factory=dict)
    execution_result: Optional[Dict[str, Any]] = None 
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)