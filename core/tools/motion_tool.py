import cv2
from .base import BaseTool

class MotionDetectionTool(BaseTool):
    @property
    def name(self) -> str: return "motion_detector"
    
    @property
    def description(self) -> str: return "ตรวจจับการเคลื่อนไหวผ่านกล้องเว็บแคม"

    def execute(self, camera_index=0) -> str:
        try:
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                return "ERROR: ไม่สามารถเปิดกล้องได้"

            ret, frame1 = cap.read()
            ret, frame2 = cap.read()
            
            if not ret:
                cap.release()
                return "ERROR: ไม่สามารถอ่านภาพจากกล้องได้"

            # เปรียบเทียบ 2 เฟรมเพื่อดูความต่าง
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            
            # นับพื้นที่ที่มีการเคลื่อนไหว
            count = cv2.countNonZero(thresh)
            cap.release()
            
            if count > 5000: # ถ้าพื้นที่การเคลื่อนไหวเกินกำหนด
                return "MOTION_DETECTED"
            return "NO_MOTION"
            
        except Exception as e:
            return f"ERROR: {str(e)}"