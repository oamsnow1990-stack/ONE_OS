from typing import Any
# --- เพิ่ม TernaryNode เข้าไปในบรรทัด Import ---
from .ast import Node, LiteralNode, VariableNode, FunctionCallNode, BinaryOpNode, PipelineNode, ListNode, DictNode, TernaryNode
from .resolver import RuntimeResolver
from .registry.function_registry import FunctionRegistry
from .errors import RuntimeError

class Evaluator:
    def __init__(self, resolver: RuntimeResolver, func_registry: FunctionRegistry):
        self.resolver = resolver
        self.func_registry = func_registry

    def evaluate(self, node: Node) -> Any:
        if isinstance(node, LiteralNode):
            return node.value
        
        if isinstance(node, VariableNode):
            return self.resolver.resolve(node.path)
            
        if isinstance(node, FunctionCallNode):
            args = [self.evaluate(arg) for arg in node.arguments]
            func = self.func_registry.get(node.name)
            return func.execute(*args)

        if isinstance(node, BinaryOpNode):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            
            if node.op == '+': return left_val + right_val
            if node.op == '-': return left_val - right_val
            if node.op == '*': return left_val * right_val
            if node.op == '/': return left_val / right_val
            if node.op == '<': return left_val < right_val
            if node.op == '>': return left_val > right_val
            if node.op == '==': return left_val == right_val
            
            raise RuntimeError(f"Unknown operator: {node.op}")

        # --- เพิ่มส่วนจัดการ Collections (Sprint 4) ---
        if isinstance(node, ListNode):
            # Evaluate สมาชิกทุกตัวใน List แล้วเก็บเป็น Python List
            return [self.evaluate(el) for el in node.elements]

        if isinstance(node, DictNode):
            # Evaluate ค่า (Value) ทุกตัวใน Dict แล้วเก็บเป็น Python Dict
            # Key เป็น string ที่เราดึงมาตั้งแต่ตอน Parse อยู่แล้ว
            return {key: self.evaluate(val_node) for key, val_node in node.items}

        # --- ส่วนจัดการ Pipeline (Sprint 3) ---
        if isinstance(node, PipelineNode):
            value = self.evaluate(node.target)
            for f_node in node.filters:
                func = self.func_registry.get(f_node.name)
                args = [self.evaluate(arg) for arg in f_node.arguments]
                value = func.execute(value, *args)
            return value

        # --- เพิ่มส่วนจัดการ Ternary Operator (Sprint 5) ---
        if isinstance(node, TernaryNode):
            condition_val = self.evaluate(node.condition)
            if condition_val:
                return self.evaluate(node.true_expr)
            else:
                return self.evaluate(node.false_expr)
            
        raise RuntimeError(f"Unknown node type: {type(node)}")