# ONE OS Brain Module: agents/brain.py
import requests
import json

class ONEAIBrain:
    """แกนสมองอัจฉริยะระดับสูง เชื่อมต่อขุมพลังคิดวิเคราะห์ผ่าน API ระดับโลก"""
    def __init__(self):
        # 🔑 กุญแจรหัสสมองเจ้านายสามารถสมัครรับฟรีได้จาก Google AI Studio
        # (ระหว่างนี้ผมใส่ stub ระบบจำลองคำพูดฉลาดยืดหยุ่นไว้ให้เทสก่อนครับ)
        self.api_key = "YOUR_GEMINI_API_KEY_HERE"
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"

    def process_thinking(self, detected_command: str) -> dict:
        """รับประโยคเสียงแปลตัวหนังสือแล้วยิงเข้าชั้นโครงข่ายประสาทเพื่อวิเคราะห์คำตอบ"""
        if not detected_command:
            return {"type": "chat", "reply": "ผมพร้อมรับฟังแล้วครับเจ้านายเดย์"}

        # บล็อกเช็กคำสั่งเปิดระบบพื้นฐานด่วน (Action Interceptor) เพื่อความเร็ว
        cmd_lower = detected_command.lower()
        if "เปิด" in cmd_lower or "open" in cmd_lower:
            if "youtube" in cmd_lower or "ยูทูป" in cmd_lower:
                return {"type": "action", "target": "youtube", "reply": "เปิด YouTube ลอยขึ้นจอ สแตนด์บายความสุขและเสียงเพลงให้เรียบร้อยครับ"}
            elif "google" in cmd_lower or "กูเกิล" in cmd_lower:
                return {"type": "action", "target": "google", "reply": "เปิดหน้าค้นหา Google เตรียมพร้อมหาข้อมูลให้เจ้านายแล้วครับ"}
            elif "netflix" in cmd_lower or "เน็ตฟลิก" in cmd_lower:
                return {"type": "action", "target": "netflix", "reply": "เปิดระบบความบันเทิง Netflix ให้เจ้านายเดย์พักผ่อนครับ"}
            elif "เครื่องคิดเลข" in cmd_lower or "calculator" in cmd_lower:
                return {"type": "action", "target": "calculator", "reply": "เปิดแอปพลิเคชันเครื่องคิดเลขขึ้นสู่หน้าจอหลักเรียบร้อยครับ"}

        # 🛸 กรณีเป็นคำถามทั่วไป คุยเล่น หรือข้อคิดวิเคราะห์ ให้ส่งขึ้นโมเดล AI ระดับโลกคิดคำตอบมาให้
        if self.api_key == "YOUR_GEMINI_API_KEY_HERE":
            # ตัวจำลองคำตอบฉลาดชดเชย กรณีเจ้านายยังไม่ได้ใส่ API Key
            return {
                "type": "chat", 
                "reply": f"ผมได้รับข้อความคำถาม '{detected_command}' แล้วครับเจ้านายเดย์ ตัวระบบกำลังรอเจ้านายนำ API Key จากกูเกิลมาหยอดเพื่อเปิดสวิตช์พลังสมองเต็มร้อยครับ!"
            }

        try:
            # ยิงขึ้นขุมพลังคลาวด์วิเคราะห์ภาษา
            payload = {
                "contents": [{
                    "parts": [{"text": f"คุณคือ ONE OS ระบบปฏิบัติการ AI อัจฉริยะประจำตัวของคุณเดย์ (เดย์ สุชาติ แซ่เฮ้ง) จงตอบคำถามต่อไปนี้สั้นๆ กระชับ สุภาพ สไตล์ AI สุดล้ำ ไซไฟ: {detected_command}"}]
                }]
            }
            response = requests.post(self.endpoint, json=payload, timeout=7)
            if response.status_code == 200:
                result_json = response.json()
                ai_reply = result_json['candidates'][0]['content']['parts'][0]['text']
                return {"type": "chat", "reply": ai_reply.strip()}
            else:
                return {"type": "chat", "reply": f"การเชื่อมโยงสมองส่วนกลางติดขัดชั่วคราว รหัสเอเรอร์ {response.status_code} ครับเจ้านาย"}
        except Exception as e:
            return {"type": "chat", "reply": "โครงข่ายประสาทเชื่อมคลาวด์หมดเวลาการรอคอยข้อมูลครับเจ้านาย"}

# สถาปนาโครงสร้างก้อนสมองจำลองระดับโลกประจำพิกัด
global_ai_brain = ONEAIBrain()