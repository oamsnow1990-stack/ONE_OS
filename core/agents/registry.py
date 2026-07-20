from typing import Dict, List
from core.kernel.base_service import BaseService
from .base import BaseAgent

class AgentRegistry(BaseService):
    """ศูนย์รวม Agent (Plug-and-play)"""
    def __init__(self):
        super().__init__("agent_registry")
        self._agents: Dict[str, BaseAgent] = {}
        self.logger = None

    def on_initialize(self, container):
        self.logger = container.get("logger")

    def on_start(self):
        self.logger.info("Agent Registry Service is Online.")

    def on_stop(self):
        for agent in self._agents.values():
            # ตรวจสอบเผื่อ Agent มี shutdown() ในอนาคต
            if hasattr(agent, 'shutdown'):
                agent.shutdown()
        self.logger.info("Agent Registry Service Offline.")

    def register(self, agent: BaseAgent) -> None:
        """ลงทะเบียน Agent พร้อมตรวจสอบความพร้อมใช้งาน"""
        # 🟢 ใช้ hasattr เพื่อป้องกัน Error หาก Agent ไม่ได้นิยาม initialize ไว้
        if hasattr(agent, 'initialize'):
            agent.initialize()
            
        self._agents[agent.name] = agent
        
        if self.logger:
            self.logger.debug(f"Registered Agent: {agent.name}")

    def get_agent(self, name: str) -> BaseAgent:
        if name not in self._agents:
            raise KeyError(f"Agent '{name}' not found in registry.")
        return self._agents[name]