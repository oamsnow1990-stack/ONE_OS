from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class Scenario:
    scenario_id: str
    description: str
    actions: List[Dict[str, Any]]
    expected_outcome: Dict[str, Any]
    estimated_cost: float
    confidence: float
    risk_level: str  # 'low', 'medium', 'high'
    rollback_possibility: bool # สำคัญมากตามที่ท่าน CTO ต้องการ