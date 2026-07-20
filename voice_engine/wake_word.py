# ONE OS Voice Module: voice/wake_word.py
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import io

class WakeWordEngine:
    """ระบบตรวจจับคลื่นความถี่เสียงคำปลุกระบบ (Wake Word Engine) แบบ Realtime Seamless"""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000
        self.wake_words = ["วัน", "one", "friday", "จาร์วิส", "ว่าน", "วาน"]
        self.last_detected_text = ""

    def listen_continuously(self) -> bool:
        """เปิดไมค์รับเสียงแบบสตรีม 3 วินาที เพื่อแกะรวบทั้งคำปลุกและคำสั่งพร้อมกันในประโยคเดียว"""
        duration = 3.0
        try:
            # ดึงเสียงสดลงแรมความเร็วสูงทันที
            audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
            sd.wait()

            wav_io = io.BytesIO()
            wav.write(wav_io, self.sample_rate, audio_data)
            wav_io.seek(0)
            
            with sr.AudioFile(wav_io) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language="th-TH").lower().strip()
                
                if text:
                    self.last_detected_text = text
                    # เช็กคำทักทายคำปลุก
                    for word in self.wake_words:
                        if word in text:
                            return True
        except:
            pass
        return False

global_wake_engine = WakeWordEngine()