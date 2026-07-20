import asyncio
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="ONE OS KERNEL API")

# อนุญาตให้ Frontend เชื่อมต่อเข้ามาได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/telemetry")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🟢 [SYSTEM] Control Room Connected!")
    
    states = ['LISTENING', 'THINKING', 'SPEAKING', 'ALERT']
    
    try:
        while True:
            # สุ่มเปลี่ยนสถานะ AI ทุกๆ 3 วินาที (ของจริงเราจะดึงค่าจากสมอง AI จริงๆ)
            current_state = random.choice(states)
            
            # ส่งข้อมูลไปให้หน้าเว็บ
            await websocket.send_json({
                "kernel_state": current_state
            })
            
            await asyncio.sleep(3) 
            
    except Exception as e:
        print("🔴 [SYSTEM] Control Room Disconnected.")

if __name__ == "__main__":
    print("🚀 Starting ONE OS API Server on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)