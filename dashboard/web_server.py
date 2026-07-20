from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # นำเข้าไลบรารี Static
import uvicorn
import psutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🚀 ตรงนี้คือหัวใจสำคัญครับ: เชื่อมโฟลเดอร์ static เข้ากับระบบ
app.mount("/static", StaticFiles(directory="dashboard/static_ui"), name="static")

@app.get("/api/system/stats")
async def get_system_stats():
    return {
        "cpu_usage": psutil.cpu_percent(interval=None),
        "ram_usage": psutil.virtual_memory().percent
    }

@app.get("/api/system/speech")
async def get_latest_speech():
    from voice_engine.text_to_speech import global_tts_engine
    if global_tts_engine.has_new_speech:
        text = global_tts_engine.latest_speech_text
        global_tts_engine.has_new_speech = False
        return {"should_speak": True, "text": text}
    return {"should_speak": False, "text": ""}

def start_dashboard_api_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)