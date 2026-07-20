# ONE OS Module: voice/speech_to_text.py
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import io

class SpeechToTextEngine:
    """ระบบแปลงเสียงคำสั่งของเจ้านายให้กลายเป็นข้อความ (Command Dictation)"""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 16000

    def listen_to_command(self) -> str:
        """เปิดไมค์อัดเสียงคำสั่งหลังจากระบบตื่นแล้ว"""
        print("🎙️ [Listening Command]: ONE กำลังฟังคำสั่ง... (มีเวลาพูด 6 วินาที)")
        try:
            # ขยายเวลาให้เจ้านายพูดได้ยาวและสบายขึ้นเป็น 6 วินาที
            duration = 6.0
            audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
            sd.wait()
            
            wav_io = io.BytesIO()
            wav.write(wav_io, self.sample_rate, audio_data)
            wav_io.seek(0)
            
            with sr.AudioFile(wav_io) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language="th-TH").strip()
                return text
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"⚠ [Speech Error]: {e}")
            return ""

global_stt_engine = SpeechToTextEngine()