import re
from typing import Any, Dict

class VariableResolver:
    """ถอดรหัสตัวแปรในรูปแบบ {{ key.path }}"""
    
    @staticmethod
    def resolve(data: Any, context: Dict[str, Any]) -> Any:
        # ถ้าเป็น dict ให้วนลูปเข้าไปแก้ทุกค่า
        if isinstance(data, dict):
            return {k: VariableResolver.resolve(v, context) for k, v in data.items()}
        # ถ้าเป็น list ให้วนลูปเข้าไปแก้ทุกตัว
        elif isinstance(data, list):
            return [VariableResolver.resolve(v, context) for v in data]
        # ถ้าเป็น string ให้เช็กว่ามี {{ ... }} หรือไม่
        elif isinstance(data, str):
            pattern = r"\{\{\s*(.*?)\s*\}\}"
            matches = re.findall(pattern, data)
            for match in matches:
                # ดึงค่าจาก context (เช่น "search_step.output.videos")
                val = VariableResolver._get_value_by_path(match, context)
                data = data.replace(f"{{{{ {match} }}}}", str(val))
            return data
        return data

    @staticmethod
    def _get_value_by_path(path: str, context: Dict[str, Any]) -> Any:
        """แปลง path เช่น 'search_step.output' เป็นค่าใน context"""
        keys = path.split('.')
        current = context
        try:
            for key in keys:
                current = current[key]
            return current
        except KeyError:
            return f"{{ERROR: {path} not found}}"