import ast
import operator
from .base import BaseTool

class CalculatorTool(BaseTool):
    @property
    def name(self) -> str: return "calculator"
    
    @property
    def description(self) -> str: return "คำนวณเลขพื้นฐาน (ปลอดภัยจากการรันโค้ดแปลกปลอม)"

    _operators = {
        ast.Add: operator.add, 
        ast.Sub: operator.sub, 
        ast.Mult: operator.mul,
        ast.Div: operator.truediv, 
        ast.Pow: operator.pow, 
        ast.USub: operator.neg
    }

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):  
            return node.value
        elif isinstance(node, ast.UnaryOp): 
            return self._operators[type(node.op)](self._eval_node(node.operand))
        elif isinstance(node, ast.BinOp):   
            return self._operators[type(node.op)](self._eval_node(node.left), self._eval_node(node.right))
        else:
            raise TypeError(f"ห้ามใช้ฟังก์ชันนี้: {type(node).__name__}")

    def execute(self, expression: str) -> str:
        try:
            node = ast.parse(expression, mode='eval').body
            result = self._eval_node(node)
            return str(result)
        except Exception as e:
            return f"Error: คำนวณไม่ได้ ({str(e)})"