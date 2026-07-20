# ONE OS Agent Module: agents/research_agent.py
import asyncio
import webbrowser

class ONEResearchAgent:
    """เอเจนต์นักวิจัยอัจฉริยะ (Research Agent) รับหน้าที่เจาะลึก ค้นหาข้อมูล และวิเคราะห์ดัชนีสดบนโลกออนไลน์"""
    def __init__(self):
        self.agent_name = "ONE_Research_Subsystem"
        print(f"🕵️ [Agent Registry]: สถาปนาเอเจนต์สายสืบข้อมูล -> '{self.agent_name}' พร้อมประจำการ")

    async def execute_web_search(self, search_query: str) -> str:
        """ทำการเปิดเบราว์เซอร์เพื่อสืบค้นข้อมูลจริงตามคีย์เวิร์ดที่เจ้านายสั่ง"""
        print(f"🔍 [Research Agent]: กำลังวิเคราะห์หัวข้อวิจัย -> '{search_query}'")
        # จำลองท่อประมวลผลการค้นหาข้อมูลเชิงลึก
        await asyncio.sleep(1.0)
        
        # ยิง URL ค้นหาตรงเข้า Google Chrome บนเครื่อง Windows จริง
        search_url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(search_url)
        
        return f"🕵️ ข้อมูลการวิจัยเรื่อง '{search_query}' ถูกเปิดขึ้นบนบอร์ดเบราว์เซอร์หลักเรียบร้อยแล้วครับเจ้านายเดย์"

global_research_agent = ONEResearchAgent()