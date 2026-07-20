# ONE OS Voice Module: voice_engine/text_to_speech.py
import time

class ONETextToSpeech:
    """ระบบกล่องเสียงแบบฝากข้อความ (Web Dashboard Dispatcher)"""
    def __init__(self):
        self.latest_speech_text = ""
        self.has_new_speech = False

    def speak(self, text_to_say: str):
        """ฝากข้อความไว้ในระบบ เพื่อให้หน้าเว็บ 3D ดึงไปพูดออกลำโพง Chrome"""
        if not text_to_say:
            return
        
        print(f"📡 [Web TTS Dispatcher]: ส่งข้อความไปที่ Dashboard -> '{text_to_say}'")
        self.latest_speech_text = text_to_say
        self.has_new_speech = True
        
        # หน่วงเวลาสั้น ๆ ให้ระบบหน้าเว็บจัดการดึงข้อมูล
        time.sleep(0.5)

global_tts_engine = ONETextToSpeech()