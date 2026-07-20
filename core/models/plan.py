# core/models/plan.py
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class CandidatePlan:
    plan_id: str
    actions: List[Dict[str, Any]]
    constraints: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)