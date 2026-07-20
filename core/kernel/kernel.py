from __future__ import annotations

import signal
import sys
import time
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional, Dict

# นำเข้า Services ต่างๆ
from .service_registry import DIContainer
from .scenario_generator import ScenarioGenerator
from .event_bus import EventBus
from .context import ContextManager
from .configuration import ConfigurationManager
from .logger import SystemLogger, LogLevel
from .permission_manager import PermissionManager
from .health_monitor import HealthMonitor
from .events import EventType, SystemEvent
from .simulation_engine import SimulationEngine
from .cognitive_decision_engine import CognitiveDecisionEngine
from .world_state_registry import WorldStateRegistry
from .confidence_engine import ConfidenceEngine
from .telemetry_service import TelemetryService
from .reasoning_engine import ReasoningEngine
from .planning_engine import PlanningEngine
from .knowledge_layer import KnowledgeLayer
from .experience_store import ExperienceStore
from .learning_engine import LearningEngine

class KernelState(Enum):
    OFFLINE      = "OFFLINE"
    BOOTING      = "BOOTING"
    INITIALIZING = "INITIALIZING"
    READY        = "READY"
    RUNNING      = "RUNNING"
    BUSY         = "BUSY"
    ERROR        = "ERROR"
    RECOVERY     = "RECOVERY"
    SHUTDOWN     = "SHUTDOWN"

class ONEKernel:
    def __init__(self):
        self.state = KernelState.OFFLINE
        self._tick_count = 0
        self._start_time = 0.0

        # Core infrastructure & Engines
        self.registry            = DIContainer()
        self.event_bus           = EventBus()
        self.config              = ConfigurationManager()
        self.logger              = SystemLogger()
        self.scenario_generator  = ScenarioGenerator()
        self.global_context      = ContextManager()
        self.permissions         = PermissionManager()
        self.health_monitor      = HealthMonitor()

        self.sim_engine          = SimulationEngine()
        self.world_registry      = WorldStateRegistry()
        self.confidence_engine   = ConfidenceEngine()
        self.telemetry           = TelemetryService()
        self.decision_engine     = CognitiveDecisionEngine()
        self.reasoning_engine    = ReasoningEngine()
        self.planning_engine     = PlanningEngine()
        self.knowledge_layer     = KnowledgeLayer()
        self.experience_store    = ExperienceStore()
        self.learning_engine     = LearningEngine()

        # Registry
        self.registry.register(SystemLogger, self.logger)
        self.registry.register(EventBus, self.event_bus)
        self.registry.register(HealthMonitor, self.health_monitor)
        self.registry.register(SimulationEngine, self.sim_engine)
        self.registry.register(WorldStateRegistry, self.world_registry)
        self.registry.register(ConfidenceEngine, self.confidence_engine)
        self.registry.register(TelemetryService, self.telemetry)
        self.registry.register(CognitiveDecisionEngine, self.decision_engine)
        self.registry.register(ReasoningEngine, self.reasoning_engine)
        self.registry.register(PlanningEngine, self.planning_engine)
        self.registry.register(KnowledgeLayer, self.knowledge_layer)
        self.registry.register(ScenarioGenerator, self.scenario_generator)
        self.registry.register(ExperienceStore, self.experience_store)
        self.registry.register(LearningEngine, self.learning_engine)

    def transition_to(self, new_state: KernelState) -> bool:
        if self.state == new_state:
            return True

        valid_transitions = {
            KernelState.OFFLINE:      [KernelState.BOOTING],
            KernelState.BOOTING:      [KernelState.INITIALIZING, KernelState.ERROR],
            KernelState.INITIALIZING: [KernelState.READY, KernelState.ERROR],
            KernelState.READY:        [KernelState.RUNNING, KernelState.SHUTDOWN],
            KernelState.RUNNING:      [KernelState.BUSY, KernelState.READY, KernelState.ERROR, KernelState.SHUTDOWN],
            KernelState.BUSY:         [KernelState.RUNNING, KernelState.ERROR],
            KernelState.ERROR:        [KernelState.RECOVERY, KernelState.SHUTDOWN],
            KernelState.RECOVERY:     [KernelState.READY, KernelState.SHUTDOWN],
            KernelState.SHUTDOWN:     [KernelState.OFFLINE],
        }

        if new_state not in valid_transitions.get(self.state, []):
            self.logger.error(f"Illegal transition: {self.state.value} → {new_state.value}")
            return False

        self.state = new_state
        self.logger.info(f"Kernel State: {self.state.value}")
        return True

    def start(self, initial_config: dict = None) -> None:
        if not self.transition_to(KernelState.BOOTING):
            return

        try:
            self.transition_to(KernelState.INITIALIZING)
            self.event_bus.publish("SYSTEM_BOOT")
            if initial_config:
                self.config.load_from_dict(initial_config)
            self.registry.resolve_and_start_all()
            self.transition_to(KernelState.READY)
            self.event_bus.publish(EventType.SYSTEM_READY.value)
        except Exception as e:
            self.transition_to(KernelState.ERROR)
            self.logger.critical(f"System Critical Failure: {e}")
            raise

    def run(self) -> None:
        if not self.transition_to(KernelState.RUNNING):
            self.logger.error("❌ ไม่สามารถเข้าสู่สถานะ RUNNING ได้")
            return

        self.logger.info("🚀 [Kernel Runtime] ระบบเริ่มเดินเครื่อง")
        try:
            signal.signal(signal.SIGINT, self._handle_signal)
            signal.signal(signal.SIGTERM, self._handle_signal)
        except ValueError:
            self.logger.warning("⚠️ [Kernel] ไม่สามารถลงทะเบียน Signal (ไม่ใช่ Main Thread)")

        self._start_time = time.time()
        self._tick_count = 0

        try:
            while self.state == KernelState.RUNNING:
                self._process_cycle()
                time.sleep(0.1) 
                self._tick_count += 1
                if self._tick_count % 100 == 0:
                    self._report_system_status()
        except Exception as e:
            self.logger.critical(f"🔥 [Kernel Panic] ข้อผิดพลาดใน Runtime: {e}")
            self.transition_to(KernelState.ERROR)
        finally:
            self.shutdown()

    def _process_cycle(self) -> None:
        if not self.health_monitor.is_healthy():
            self.logger.warning("⚠️ [HealthMonitor] ตรวจพบความผิดปกติ")
        if hasattr(self.learning_engine, "run_calibration"):
            self.learning_engine.run_calibration()
        self.event_bus.process_events()

    def _report_system_status(self) -> None:
        uptime = time.time() - self._start_time
        self.logger.info(f"📊 [Telemetry] uptime: {round(uptime, 2)}s, ticks: {self._tick_count}, state: {self.state.value}")

    def _handle_signal(self, signum: int, frame: Any) -> None:
        self.logger.info(f"🛑 [System] Signal {signum} — กำลังปิดระบบ")
        self.request_shutdown()

    def request_shutdown(self) -> None:
        self.logger.info("⏳ [Kernel] กำลังดำเนินการปิดระบบ...")
        self.transition_to(KernelState.SHUTDOWN)

    def shutdown(self) -> None:
        self.logger.info("🧹 [Kernel] กำลังทำความสะอาด Resources...")
        for name in list(self.registry._services.keys()):
            # ตรงนี้ปลอดภัยแล้ว เพราะเราเพิ่ม get_by_name เข้าไปใน DIContainer แล้ว
            svc = self.registry.get_by_name(name)
            if hasattr(svc, "on_stop"):
                try:
                    svc.on_stop()
                except Exception as e:
                    self.logger.error(f"❌ on_stop '{name}': {e}")
        self.state = KernelState.OFFLINE
        self.logger.info("✅ [Kernel] ปิดระบบสำเร็จ")

    # --- ฟังก์ชันนี้ถูกย้ายออกมาไว้ข้างนอกแล้ว ---
    def trigger_recovery(self) -> None:
        """กู้คืนระบบจากสถานะ ERROR"""
        self.logger.info("♻️ [Recovery] เริ่มต้นกระบวนการกู้คืน...")
        self.transition_to(KernelState.READY)