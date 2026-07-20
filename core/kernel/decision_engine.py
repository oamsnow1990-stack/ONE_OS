import time
from typing import List, Any
from core.models.decision_models import MissionProfile, EvaluationResult, DecisionRecord
from core.models.enums import RejectedReason

class DecisionEngine:
    def __init__(self):
        self.RISK_THRESHOLD = 0.5
        self.CONFIDENCE_THRESHOLD = 0.4
        self.COST_THRESHOLD = 0.8

    def decide(self, mission_id: str, candidates: List[EvaluationResult], profile: MissionProfile, world_version: int) -> DecisionRecord:
        """ประมวลผลการตัดสินใจและสร้าง Record ตาม Schema ใหม่"""
        
        # 1. คำนวณคะแนนและ Ranking
        scored_candidates = []
        for cand in candidates:
            score = (
                (1.0 - cand.risk) * profile.risk_weight +
                (cand.confidence) * profile.confidence_weight +
                (1.0 - cand.cost) * profile.cost_weight +
                (1.0 - cand.latency) * profile.latency_weight
            )
            cand.score = round(score, 4)
            scored_candidates.append(cand)

        scored_candidates.sort(key=lambda x: x.score, reverse=True)
        winner = scored_candidates[0]
        
        # 2. จัดเตรียม Candidates List สำหรับ Record (Explainable AI)
        candidates_list = [
            {"plan": c.scenario_id, "score": c.score} 
            for c in scored_candidates
        ]

        # 3. สร้าง DecisionRecord ตาม Schema ใหม่
        record = DecisionRecord(
            mission_id=mission_id,
            world_version=world_version,
            profile_name=profile.name,
            selected_plan=winner.scenario_id,
            selected_score=winner.score,
            candidates=candidates_list,
            simulation_metrics={
                "risk": winner.risk,
                "confidence": winner.confidence,
                "cost": winner.cost,
                "latency": winner.latency
            }
        )
        
        return record