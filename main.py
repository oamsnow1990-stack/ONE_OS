# main.py — ONE OS Main Entry Point (GUI + Voice + Orchestrator)

from __future__ import annotations

import asyncio
import logging
import os
import sys
import threading
import time
import tkinter as tk
import webbrowser

import config
from agents.brain import global_ai_brain
from core.kernel.kernel import ONEKernel
from core.kernel.experience_store import Experience, ExperienceType
from core.permissions import global_permission_manager
from dashboard.web_server import start_dashboard_api_server
from voice_engine.text_to_speech import global_tts_engine
from voice_engine.wake_word import global_wake_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# ─────────────────────────────────────────────────────────────
# Global State
# ─────────────────────────────────────────────────────────────

gui_root:         tk.Tk     | None = None
gui_status_label: tk.Label  | None = None
gui_canvas:       tk.Canvas | None = None
gui_orb:          int       | None = None

kernel = ONEKernel()   # สร้างครั้งเดียวระดับ module

# ─────────────────────────────────────────────────────────────
# GUI Helpers
# ─────────────────────────────────────────────────────────────

def shift_visual_orb_state(status_text: str, hex_color: str) -> None:
    """เปลี่ยนข้อความและสีลูกแก้ว AI — thread-safe"""
    global gui_status_label, gui_canvas, gui_orb
    if gui_status_label and gui_canvas and gui_orb is not None:
        gui_status_label.config(text=status_text, fg=hex_color)
        gui_canvas.itemconfig(gui_orb, fill=hex_color, outline=hex_color)


def animate_visual_feedback(mode: str) -> None:
    """สร้าง Animation ให้ลูกแก้วตาม mode การทำงาน"""
    _MODE_MAP = {
        "LEARNING":        ("🎓 LEARNING IN PROGRESS...", "#FFD700"),
        "CALIBRATING":     ("⚙️ SYSTEM CALIBRATION...",   "#00BFFF"),
        "DECISION_MAKING": ("🧠 ANALYZING DATA...",        "#8A2BE2"),
    }
    text, color = _MODE_MAP.get(mode, ("🟢 STANDBY", "#00FF00"))
    shift_visual_orb_state(text, color)


# ─────────────────────────────────────────────────────────────
# Windows Action Dispatcher
# ─────────────────────────────────────────────────────────────

_APP_URLS = {
    "netflix": "https://www.netflix.com",
    "google":  "https://www.google.com",
    "youtube": "https://www.youtube.com",
}

def trigger_windows_action(target_app: str) -> None:
    """เปิดแอปหรือ URL ผ่าน Chrome — fallback default browser"""
    if target_app == "calculator":
        os.system("calc")
        return

    url = _APP_URLS.get(target_app)
    if not url:
        return

    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    try:
        webbrowser.get(chrome_path).open(url)
    except Exception:
        webbrowser.open(url)


# ─────────────────────────────────────────────────────────────
# NLP Pipeline
# ─────────────────────────────────────────────────────────────

async def asynchronous_nlp_dispatcher(detected_command: str) -> None:
    """วิเคราะห์คำสั่งเสียงและตรวจสอบสิทธิ์ก่อน execute"""
    shift_visual_orb_state("🤔 ONE กำลังคิดคำนวณ...", "#FF00FF")

    result = global_ai_brain.process_thinking(detected_command)
    print(f'\n🤖 ONE: "{result["reply"]}"')
    global_tts_engine.speak(result["reply"])

    shift_visual_orb_state("🟢 ประมวลผลภารกิจสำเร็จ!", "#00FF00")
    await asyncio.sleep(1.5)

    if result.get("type") != "action":
        return

    security_key = (
        "SYSTEM_MUTATION"
        if any(kw in detected_command for kw in ["ลบ", "ปิด"])
        else "NORMAL_ACTION"
    )
    gate = global_permission_manager.check_action_permission(security_key)

    if gate in {"LEVEL_4_CRITICAL_LOCK", "LEVEL_3_OWNER_VERIFICATION"}:
        if global_permission_manager.execute_owner_verification_flow(detected_command):
            trigger_windows_action(result.get("target", ""))
    else:
        trigger_windows_action(result.get("target", ""))


# ─────────────────────────────────────────────────────────────
# Voice Background Thread
# ─────────────────────────────────────────────────────────────

def background_voice_worker_thread() -> None:
    """เธรดเปิดไมค์รอรับคำสั่งเบื้องหลังตลอดเวลา"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        shift_visual_orb_state(
            f"🎤 ONE กำลังฟังคุณ{config.OWNER_NICKNAME}...", "#00FFFF"
        )

        if global_wake_engine.listen_continuously():
            shift_visual_orb_state("⚡ ระบบตื่นตัว! กำลังถอดสลักคำสั่ง...", "#FFAA00")

            raw_text = global_wake_engine.last_detected_text
            print(f'\n👂 [Detected]: "{raw_text}"')

            clean_cmd = raw_text
            for word in global_wake_engine.wake_words:
                if word in raw_text:
                    clean_cmd = raw_text.replace(word, "").strip()
                    break

            if len(clean_cmd) >= 2:
                loop.run_until_complete(asynchronous_nlp_dispatcher(clean_cmd))
            else:
                reply = "ครับเจ้านายเดย์ ONE สแตนด์บายรอฟังอยู่ครับ"
                print(f'\n⚡ [Wake Only]\n🤖 ONE: "{reply}"')
                global_tts_engine.speak(reply)
                time.sleep(1.5)

        time.sleep(0.3)


# ─────────────────────────────────────────────────────────────
# System Orchestrator
# ─────────────────────────────────────────────────────────────

class SystemOrchestrator:
    """
    จัดการความสัมพันธ์ระหว่าง:
    - Legacy Systems (Voice Engine, AI Brain)
    - New Infrastructure (ONEKernel, Cognitive Engine)
    - GUI Lifecycle (Orb State Management)
    """

    def __init__(self, kernel: ONEKernel, root: tk.Tk) -> None:
        self.kernel    = kernel
        self.root      = root
        self.logger    = logging.getLogger("Orchestrator")
        self.is_active = True
        self._lock     = threading.Lock()
        self.logger.info("🛠️ [Orchestrator] เริ่มต้นการเชื่อมต่อระบบ...")

    def run_full_lifecycle(self) -> None:
        """Boot sequence + เริ่ม kernel loop + heartbeat"""
        self.logger.info("🔄 [Orchestrator] รวมระบบ Legacy เข้ากับ Kernel...")

        try:
            self.kernel.start()
        except Exception as e:
            self.logger.critical(f"❌ [Orchestrator] Kernel Boot Failure: {e}")
            shift_visual_orb_state("🚨 KERNEL PANIC!", "#FF0000")
            return

        threading.Thread(
            target=self._managed_kernel_loop, daemon=True, name="kernel-loop"
        ).start()
        threading.Thread(
            target=self._system_heartbeat, daemon=True, name="heartbeat"
        ).start()

    def _managed_kernel_loop(self) -> None:
        """ดูแล kernel.run() และ auto-recovery เมื่อแครช"""
        while self.is_active:
            try:
                self.kernel.run()
            except Exception as e:
                self.logger.error(f"⚠️ [Orchestrator] Kernel หลุด RUNNING: {e}")
                if self.is_active:
                    self.logger.info("♻️ [Orchestrator] กำลังกู้คืนระบบ...")
                    self.kernel.trigger_recovery()
                    time.sleep(2)

    def _system_heartbeat(self) -> None:
        """ตรวจสอบสถานะทุก 5 วินาทีและอัปเดต GUI"""
        while self.is_active:
            try:
                diag = self.kernel.get_system_diagnostics()
                if diag.get("registry_health") != "OK":
                    self.logger.warning("🩺 [Heartbeat] Registry พบปัญหา!")

                status = (
                    f"ONE OS: {self.kernel.state.value} "
                    f"| Ticks: {diag.get('ticks', 0)}"
                )
                # อัปเดต GUI ผ่าน main thread
                if self.root and gui_status_label:
                    self.root.after(
                        0, lambda s=status: gui_status_label.config(text=s)
                    )
            except Exception as e:
                self.logger.debug(f"🩺 [Heartbeat] error: {e}")

            time.sleep(5)

    def bridge_command_to_cognitive(self, command: str):
        """สะพานเชื่อม Voice → Planning Engine"""
        with self._lock:
            self.logger.info(f"🧠 [Bridge] คำสั่ง: {command}")

            planning  = self.kernel.registry.get_by_name("planning_engine")
            exp_store = self.kernel.registry.get_by_name("experience_store")

            # บันทึก experience ด้วย object ที่ถูกต้อง
            if exp_store:
                from datetime import datetime
                import uuid
                exp = Experience(
                    id=          f"voice_{uuid.uuid4().hex[:8]}",
                    goal=        "voice_command",
                    workflow_id= command,
                    outcome=     ExperienceType.SUCCESS,
                    lesson=      f"Executed: {command}",
                )
                exp_store.save(exp)

            if planning:
                result = planning.execute_plan("NORMAL_MODE", "ACTIVE_CONTEXT", 0)
                self.logger.info(f"✅ [Bridge] Planning Engine: {result}")
                return result
            return None

    def graceful_shutdown(self) -> None:
        """ปิดระบบทุกอย่างอย่างปลอดภัย"""
        self.is_active = False
        self.logger.info("🛑 [Orchestrator] กำลังปิดระบบ...")
        self.kernel.shutdown()
        if self.root:
            self.root.destroy()
        sys.exit(0)


# ─────────────────────────────────────────────────────────────
# Diagnostics Tool
# ─────────────────────────────────────────────────────────────

class SystemDiagnosticsTool:
    """เครื่องมือตรวจสอบระบบเชิงลึก"""

    @staticmethod
    def dump_all_service_status(k: ONEKernel) -> None:
        print("\n--- [DI Container Dump] ---")
        for name, svc in k.registry._services.items():
            print(f"  {name:<30} | {type(svc).__name__}")
        print("----------------------------\n")

    @staticmethod
    def run_stress_test(k: ONEKernel, cycles: int = 10) -> None:
        for i in range(cycles):
            k.logger.info(f"🧪 [Stress] Cycle {i + 1}/{cycles}")
            time.sleep(0.5)
        k.logger.info("🧪 [Stress] Complete.")


# ─────────────────────────────────────────────────────────────
# Orchestrated Start
# ─────────────────────────────────────────────────────────────

def start_one_os_orchestrated() -> None:
    """
    เริ่มต้นระบบผ่าน Orchestrator
    เรียกหลังจาก gui_root ถูกสร้างแล้วเท่านั้น
    """
    orchestrator = SystemOrchestrator(kernel, gui_root)

    # Kernel lifecycle (boot + heartbeat)
    threading.Thread(
        target=orchestrator.run_full_lifecycle,
        daemon=True, name="orchestrator",
    ).start()

    # Voice thread (แยกต่างหาก)
    threading.Thread(
        target=background_voice_worker_thread,
        daemon=True, name="voice",
    ).start()

    # Dashboard API
    threading.Thread(
        target=start_dashboard_api_server,
        daemon=True, name="dashboard",
    ).start()

    # ผูก close window
    gui_root.protocol("WM_DELETE_WINDOW", orchestrator.graceful_shutdown)


# ─────────────────────────────────────────────────────────────
# GUI Builder
# ─────────────────────────────────────────────────────────────

def spawn_innovative_orb_gui() -> None:
    """สร้างหน้าต่าง GUI ลูกแก้ว AI แล้วเริ่ม orchestrator"""
    global gui_root, gui_status_label, gui_canvas, gui_orb

    gui_root = tk.Tk()
    gui_root.title(f"ONE OS — Visual Body v{config.SYSTEM_VERSION}")
    gui_root.geometry("400x360")
    gui_root.configure(bg="#0B0B0F")
    gui_root.resizable(False, False)
    gui_root.attributes("-topmost", True)

    gui_canvas = tk.Canvas(
        gui_root, width=200, height=200,
        bg="#0B0B0F", highlightthickness=0,
    )
    gui_canvas.pack(pady=40)

    gui_orb = gui_canvas.create_oval(
        15, 15, 185, 185, fill="#00FFFF", outline="#00FFFF"
    )

    gui_status_label = tk.Label(
        gui_root,
        text="🤖 กำลังสตาร์ทคอร์ระบบ...",
        font=("Consolas", 12, "bold"),
        bg="#0B0B0F",
        fg="#00FFFF",
    )
    gui_status_label.pack()

    # เริ่ม orchestrator หลังจาก gui_root พร้อมแล้ว ← สำคัญ
    start_one_os_orchestrated()

    gui_root.mainloop()


# ─────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 85)
    print(f"  🤖 ONE OS [AI Operating System] v{config.SYSTEM_VERSION}")
    print(f"  👤 OWNER: คุณ{config.OWNER_NAME} ({config.OWNER_NICKNAME})")
    print("=" * 85)
    spawn_innovative_orb_gui()   # blocking — จนกว่าจะปิดหน้าต่าง