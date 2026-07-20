# ONE OS Module: owner/owner.py
import json
from pathlib import Path

class OwnerProfileManager:
    """คลาสจัดการโหลดและอ่านข้อมูลเอกลักษณ์ส่วนบุคคลของเจ้านายเดย์"""
    def __init__(self):
        # ชี้พาธไปหาไฟล์ profile.json ในโฟลเดอร์เดียวกัน
        self.profile_path = Path(__file__).resolve().parent / "profile.json"
        self.profile_data = self.load_profile()

    def load_profile(self) -> dict:
        try:
            with open(self.profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # ค่าสำรองปลอดภัยกรณีไฟล์ json มีปัญหา
            return {"owner": {"name": "สุชาติ แซ่เฮ้ง", "nickname": "เดย์"}}

    def get_name(self) -> str:
        return self.profile_data.get("owner", {}).get("name", "เจ้านาย")

    def get_nickname(self) -> str:
        return self.profile_data.get("owner", {}).get("nickname", "เดย์")

# สร้างตัวแปรหลักเพื่อให้ main.py เรียกใช้งานได้ถูกต้อง
global_owner_manager = OwnerProfileManager()