from typing import Any
from .tokenizer import Tokenizer
from .parser import Parser
from .evaluator import Evaluator
from .resolver import RuntimeResolver

# ใช้ Absolute Import ตรงนี้ที่เดียวจบครับ
from .registry.function_registry import FunctionRegistry
from .registry.filter_registry import FilterRegistry
from .registry.variable_registry import VariableRegistry # เพิ่มบรรทัดนี้ครับ

class OELEngine:
    def __init__(self):
        # สร้างคลังฟังก์ชัน, ฟิลเตอร์ และตัวแปร
        self.functions = FunctionRegistry()
        self.filters = FilterRegistry()
        self.variables = VariableRegistry() # เพิ่มบรรทัดนี้ครับ
        
    def compile(self, expression: str):
        """แปลง string เป็น AST ที่พร้อม execute"""
        tokens = Tokenizer(expression).tokenize()
        ast = Parser(tokens).parse()
        return ast

    def execute(self, ast: Any, context: ExecutionContext) -> Any:
        """รัน AST ด้วย Context ที่กำหนด"""
        resolver = RuntimeResolver(context)
        evaluator = Evaluator(resolver, self.functions)
        return evaluator.evaluate(ast)

    def run(self, expression: str, context: ExecutionContext) -> Any:
        """ทางลัด: Compile + Execute ในบรรทัดเดียว"""
        ast = self.compile(expression)
        return self.execute(ast, context)