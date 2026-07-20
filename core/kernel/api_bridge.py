import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Any

class OSAPIBridge:
    def __init__(self, kernel: Any):
        self.app = FastAPI(title="ONE OS Control Room API")
        self.kernel = kernel
        self.active_connections: list[WebSocket] = []

        @self.app.websocket("/ws/telemetry")
        async def telemetry_websocket(websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)
            try:
                while True:
                    payload = self._gather_system_metrics()
                    await websocket.send_json(payload)
                    await asyncio.sleep(1.0)
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
            except Exception as e:
                print(f"❌ [WebSocket Error]: {e}")
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)

    def _gather_system_metrics(self) -> dict:
        diagnostics = self.kernel.get_system_diagnostics() if hasattr(self.kernel, "get_system_diagnostics") else {}
        return {
            "kernel_state": str(diagnostics.get("kernel_state", "RUNNING")),
            "ticks": diagnostics.get("ticks", 0),
            "uptime": diagnostics.get("uptime_seconds", 0.0),
            "brain": {
                "confidence": 0.87,
                "risk_level": 0.24,
                "mode": "AGGRESSIVE"
            },
            "world_state": {
                "weather": "Cloudy",
                "energy": "78%",
                "battery": "62%"
            }
        }