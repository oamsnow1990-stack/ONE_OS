from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from core.kernel.base_service import BaseService

@dataclass
class Skill:
    name: str
    workflow_id: str
    template: Any  # workflow template ที่เรียนมา
    description: str = "" # 🟢 เผื่อไว้ใช้ตอน Planner หาความสอดคล้อง
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    success_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize สำหรับบันทึกลง disk"""
        return {
            "name": self.name,
            "workflow_id": self.workflow_id,
            "description": self.description,
            "template": self.template if isinstance(self.template, (dict, list, str)) else str(self.template),
            "created_at": self.created_at,
            "success_count": self.success_count,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Deserialize จาก disk"""
        return cls(
            name=data["name"],
            workflow_id=data.get("workflow_id", data["name"]),
            description=data.get("description", ""),
            template=data.get("template", {}),
            created_at=data.get("created_at", datetime.now().isoformat()),
            success_count=data.get("success_count", 0),
            metadata=data.get("metadata", {}),
        )

class SkillRegistryService(BaseService):
    def __init__(self):
        super().__init__("skill_registry")
        self.skills: Dict[str, Skill] = {}
        self.logger = None
        self.persistence = None

    def on_initialize(self, container: Any) -> None:
        self.logger = container.get("system_logger")
        self.persistence = container.get("persistence_service") 
        
        if self.logger:
            self.logger.info("📚 [SkillRegistry] ระบบจัดการทักษะพร้อมทำงาน")
            
        self._load_from_disk()

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def _load_from_disk(self) -> None:
        """โหลด skills ที่เรียนไว้แล้วกลับมา โดยผ่าน PersistenceService"""
        if not self.persistence: return
        
        data = self.persistence.load("skills")
        if data:
            for name, skill_data in data.items():
                self.skills[name] = Skill.from_dict(skill_data)
            if self.logger:
                self.logger.info(f"🧠 [SkillRegistry] ดึงความจำเก่ากลับมาได้ {len(self.skills)} ทักษะ")

    def _save_to_disk(self) -> None:
        """บันทึกข้อมูลโดยใช้ PersistenceService"""
        if not self.persistence: return
        
        # 🟢 ใช้ .to_dict() ที่เจ้านายเขียนไว้ได้เลย!
        data_to_save = {name: skill.to_dict() for name, skill in self.skills.items()}
        self.persistence.save("skills", data_to_save)

    def register_skill(self, skill: Any) -> None:
        """รองรับการเรียกจาก Learning Engine โดยตรง"""
        if isinstance(skill, dict):
            name = skill.get("name", "unknown")
            workflow_id = skill.get("workflow_id", name)
            desc = skill.get("description", "")
            template = skill.get("workflow_template", skill.get("template", []))
            new_skill = Skill(name=name, workflow_id=workflow_id, description=desc, template=template)
            self.skills[name] = new_skill
        else:
            # แปลง Object ที่ส่งมาให้กลายเป็น Skill Dataclass ที่สมบูรณ์
            name = getattr(skill, "name", "unknown")
            workflow_id = getattr(skill, "workflow_id", name)
            desc = getattr(skill, "description", "")
            template = getattr(skill, "workflow_template", getattr(skill, "template", []))
            
            self.skills[name] = Skill(name=name, workflow_id=workflow_id, description=desc, template=template)
            
        if self.logger:
            self.logger.info(f"📚 [SkillRegistry] เรียนรู้และลงทะเบียนทักษะใหม่: {name}")
            
        self._save_to_disk()

    def learn_skill(self, name: str, description: str, workflow_template: Any) -> None:
        new_skill = Skill(name=name, workflow_id=name, description=description, template=workflow_template)
        self.skills[name] = new_skill
        
        if self.logger:
            self.logger.info(f"📚 [SkillRegistry] เรียนรู้ทักษะใหม่: {name}")
            
        self._save_to_disk()

    def find_skill(self, goal: str) -> Optional[Skill]:
        for skill_name, skill in self.skills.items():
            if goal.lower() in skill_name.lower():
                return skill
        return None