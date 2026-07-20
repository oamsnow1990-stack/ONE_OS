from dataclasses import replace
from typing import Dict, Any, List, Optional
from core.kernel.world_state import WorldState
import time

class WorldStateManager:
    def __init__(self):
        self._current_state = WorldState(version=1)
        self._history: Dict[int, WorldState] = {1: self._current_state}
        self._event_log: List[Dict[str, Any]] = []
        self._is_locked = False

    def get_state(self) -> WorldState:
        return self._current_state

    def commit(self, event_name: str, payload: Dict[str, Any]) -> WorldState:
        if self._is_locked:
            raise RuntimeError("WorldState is currently locked.")

        self._is_locked = True
        try:
            old_state = self._current_state
            
            event_entry = {
                "version": old_state.version + 1,
                "event": event_name,
                "payload": payload,
                "timestamp": time.time()
            }
            self._event_log.append(event_entry)

            new_data = self._apply_logic(old_state, event_name, payload)
            
            new_state = replace(
                old_state,
                version=old_state.version + 1,
                timestamp=time.time(),
                **new_data
            )

            self._current_state = new_state
            self._history[new_state.version] = new_state
            return new_state
        finally:
            self._is_locked = False

    def _apply_logic(self, state: WorldState, event: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        new_data = {
            "environment": dict(state.environment),
            "user": dict(state.user),
            "devices": dict(state.devices),
            "agents": dict(state.agents),
            "goals": list(state.goals),
            "threats": list(state.threats),
            "resources": dict(state.resources),
            "history": list(state.history),
            "predictions": list(state.predictions),
        }

        if event == "UPDATE_DEVICE":
            new_data["devices"].update(payload)
        elif event == "DETECT_THREAT":
            new_data["threats"].append(payload)
        return new_data