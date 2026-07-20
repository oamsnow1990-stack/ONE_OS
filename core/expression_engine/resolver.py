from typing import Any
from .context import ExecutionContext
from .errors import ResolveError

class RuntimeResolver:
    def __init__(self, context: ExecutionContext):
        self.context = context

    def resolve(self, path: tuple) -> Any:
        root_key = path[0]
        
        # 1. ลองหาจาก Attribute ของ ExecutionContext (เช่น variables)
        current_data = getattr(self.context, root_key, None)
        
        # 2. ถ้าไม่เจอ ให้ลองหาใน runtime dictionary
        if current_data is None and hasattr(self.context, 'runtime'):
            current_data = self.context.runtime.get(root_key)
            
        # 3. ถ้ายังไม่เจอ ให้ลองหาใน variables registry
        if current_data is None:
            current_data = self.context.variables.get(root_key)
            
        if current_data is None:
            raise ResolveError(f"Variable '{root_key}' not found in context")

        # ไล่ตาม path ที่เหลือ
        for part in path[1:]:
            if isinstance(current_data, dict):
                current_data = current_data.get(part)
            else:
                current_data = getattr(current_data, part, None)
            
            if current_data is None:
                raise ResolveError(f"Cannot resolve path part: {part}")
                
        return current_data