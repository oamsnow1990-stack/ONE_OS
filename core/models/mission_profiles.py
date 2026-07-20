from dataclasses import dataclass

@dataclass
class MissionProfile:
    name: str
    risk_tolerance: float  # 0.0 (กลัวเสี่ยง) ถึง 1.0 (กล้าเสี่ยงสุดๆ)
    resource_priority: float # 0.0 (ประหยัดสุด) ถึง 1.0 (เน้นเอาทรัพยากร)