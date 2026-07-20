import networkx as nx
from core.kernel.base_service import BaseService, ServiceState

class WorldModelService(BaseService):
    def __init__(self):
        super().__init__("world_model")
        self.graph = nx.MultiDiGraph() # ใช้ MultiDiGraph เพื่อรองรับหลายความสัมพันธ์

    # --- Lifecycle Methods ---
    def on_initialize(self, container):
        pass

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def add_entity(self, entity_id: str, type: str, metadata: dict = None) -> None:
        """เพิ่ม Node โดยแยก type ออกจาก metadata เพื่อป้องกัน Argument ซ้ำซ้อน"""
        attributes = metadata.copy() if metadata else {}
        attributes['type'] = type
        self.graph.add_node(entity_id, **attributes)

    def add_relationship(self, source: str, target: str, relation: str) -> None:
        self.graph.add_edge(source, target, relation=relation)

    def get_devices_in_room(self, room_id: str) -> list:
        # เช็คก่อนว่ามีห้องนี้ในกราฟไหม
        if room_id not in self.graph:
            return []
            
        # แก้ไขการ Unpack: รับ (u, v, data) ให้ครบ 3 ตัว
        return [u for u, v, data in self.graph.in_edges(room_id, data=True) 
                if data.get('relation') == 'located_in']

    def get_context_for_planner(self, entity_id: str) -> list:
        # เช็คก่อนว่ามี entity นี้ในกราฟไหม
        if entity_id not in self.graph:
            return []
            
        # คืนค่าเพื่อนบ้านทั้งหมดเพื่อให้ Planner เห็นภาพรวม
        return list(self.graph.neighbors(entity_id))

    def query_entities(self, type_filter: str = None, **attributes) -> list:
        """
        [Advanced Query] ค้นหา Entity ตามเงื่อนไข:
        เช่น query_entities(type_filter="sensor", capability="motion")
        """
        results = []
        for n, data in self.graph.nodes(data=True):
            # 1. กรองด้วย type (ถ้ามีการระบุ)
            if type_filter and data.get('type') != type_filter:
                continue
            
            # 2. กรองด้วย Attributes อื่นๆ (เช่น capability, brand)
            match = True
            for key, value in attributes.items():
                if data.get(key) != value:
                    match = False
                    break
            
            if match:
                results.append(n)
        return results