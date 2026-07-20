from .base import BaseTool

class WebSearchTool(BaseTool):
    @property
    def name(self) -> str: return "web_search"
    
    @property
    def description(self) -> str: return "ค้นหาข้อมูลจากอินเทอร์เน็ต"
    
    def execute(self, query: str) -> str:
        # เจ้านายสามารถเชื่อมต่อ Google API จริงๆ ตรงนี้ได้เลย
        return f"ผลลัพธ์การค้นหาสำหรับ '{query}': เจอข้อมูล 3 รายการเกี่ยวกับ {query}"