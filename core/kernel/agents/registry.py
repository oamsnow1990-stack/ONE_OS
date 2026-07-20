from typing import Dict, List
from core.kernel.base_service import BaseService
from .base import BaseAgent

class AgentRegistry(BaseService):
    """ศูนย์รวม Agent ทั้งหมดในระบบ (Plug-and-play architecture)"""
    def __init__(self):
        super().__init__("agent_registry")
        self._agents: Dict[str, BaseAgent] = {}

    def on_initialize(self, container):
        self.logger = container.get("logger")

    def on_start(self):
        self.logger.info("Agent Registry Service is Online.")

    def on_stop(self):
        self.shutdown_all()
        self.logger.info("Agent Registry Service Offline.")

    def register(self, agent: BaseAgent) -> None:
        """ลงทะเบียน Agent เข้าสู่ระบบ"""
        if agent.name in self._agents:
            self.logger.warning(f"Agent '{agent.name}' is being overwritten.")
        
        agent.initialize()
        self._agents[agent.name] = agent
        if self.logger:
            self.logger.debug(f"Registered Agent: {agent.name}")

    def unregister(self, name: str) -> None:
        """ถอดถอน Agent ออกจากระบบ"""
        if name in self._agents:
            self._agents[name].shutdown()
            del self._agents[name]
            if self.logger:
                self.logger.debug(f"Unregistered Agent: {name}")

    def get_agent(self, name: str) -> BaseAgent:
        """ดึง Agent ไปใช้งาน"""
        if name not in self._agents:
            raise KeyError(f"Agent '{name}' not found in registry.")
        return self._agents[name]

    def exists(self, name: str) -> bool:
        return name in self._agents

    def list_agents(self) -> List[str]:
        return list(self._agents.keys())

    def reload(self) -> None:
        """Reload Agent ทั้งหมด (เตรียมไว้สำหรับ Plugin SDK)"""
        if self.logger:
            self.logger.info("Reloading all agents...")
        # (อนาคต: สแกนโฟลเดอร์ plugins/ และเรียก register ใหม่)
        pass

    def shutdown_all(self):
        for agent in self._agents.values():
            agent.shutdown()