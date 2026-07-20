from dataclasses import dataclass
from typing import List, Tuple, Any

@dataclass(frozen=True)
class Node: pass

@dataclass(frozen=True)
class LiteralNode(Node): value: Any

@dataclass(frozen=True)
class VariableNode(Node): path: Tuple[str, ...]

@dataclass(frozen=True)
class FunctionCallNode(Node): name: str; arguments: List[Node]

@dataclass(frozen=True)
class FilterNode(Node): target: Node; name: str; arguments: List[Node]

@dataclass(frozen=True)
class BinaryOpNode(Node):
    left: Node
    op: str
    right: Node

@dataclass(frozen=True)
class PipelineNode(Node):
    target: Node
    filters: List[Node]

# --- เพิ่มส่วนนี้สำหรับ Sprint 4 ---

@dataclass(frozen=True)
class ListNode(Node):
    elements: List[Node]

@dataclass(frozen=True)
class DictNode(Node):
    # เก็บเป็น List ของ Tuple เพื่อรักษาลำดับ และให้ key เป็น str (กรณีทั่วไป) 
    # หรือเปลี่ยนเป็น List[Tuple[Node, Node]] หากต้องการให้ key เป็น Expression ได้
    items: List[Tuple[str, Node]]

@dataclass(frozen=True)
class DictNode(Node):
    items: List[Tuple[str, Node]]

# --- เพิ่มสำหรับ Sprint 5 ---
@dataclass(frozen=True)
class TernaryNode(Node):
    condition: Node
    true_expr: Node
    false_expr: Node