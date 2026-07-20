from typing import List
from .ast import Node, LiteralNode, VariableNode, FunctionCallNode, BinaryOpNode, PipelineNode, FilterNode, ListNode, DictNode, TernaryNode
from .errors import ParseError
from .tokenizer import Token

# ตารางลำดับความสำคัญ
PRECEDENCE = {
    '?': 3,     # เพิ่ม ? ให้มีความสำคัญต่ำสุด (ทำทีหลังสุด)
    '==': 5, '!=': 5,
    '<': 6, '>': 6,
    '+': 10, '-': 10,
    '*': 20, '/': 20,
    '|': 5 
}

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        token = self.peek()
        self.pos += 1
        return token

    def parse(self) -> Node:
        if self.peek() and self.peek().type == 'LBRACE':
            self.consume()
        node = self.parse_expression(0)
        if self.peek() and self.peek().type == 'RBRACE':
            self.consume()
        return node

    def parse_expression(self, min_precedence: int) -> Node:
        token = self.consume()
        if not token:
            raise ParseError("Unexpected end of expression")
        
        left = self.primary(token)

        while True:
            peek_token = self.peek()
            if not peek_token or peek_token.value not in PRECEDENCE:
                break
            
            op_prec = PRECEDENCE[peek_token.value]
            if op_prec <= min_precedence:
                break
                
            op = self.consume().value
            
            # --- ตรรกะใหม่สำหรับ Ternary Operator (? :) ---
            if op == '?':
                true_expr = self.parse_expression(0)
                if not self.peek() or self.peek().value != ':':
                    raise ParseError("Expected ':' for ternary operator")
                self.consume() # กิน ':'
                false_expr = self.parse_expression(3)
                left = TernaryNode(condition=left, true_expr=true_expr, false_expr=false_expr)
                
            elif op == '|':
                filters = []
                while True:
                    filter_token = self.consume()
                    if not filter_token or filter_token.type != 'IDENT':
                        raise ParseError("Expected filter name after |")
                    
                    f_args = []
                    if self.peek() and self.peek().value == '(':
                        self.consume() 
                        if self.peek() and self.peek().value != ')':
                            f_args.append(self.parse_expression(0))
                        if self.peek() and self.peek().value == ')':
                            self.consume()
                    
                    filters.append(FilterNode(target=None, name=filter_token.value, arguments=f_args))
                    
                    if self.peek() and self.peek().value == '|':
                        self.consume()
                    else:
                        break
                left = PipelineNode(target=left, filters=filters)
            else:
                right = self.parse_expression(op_prec)
                left = BinaryOpNode(left, op, right)
            
        return left

    def parse_list(self) -> Node:
        elements = []
        if self.peek() and self.peek().type != 'RBRACKET':
            elements.append(self.parse_expression(0))
            while self.peek() and self.peek().value == ',':
                self.consume() # คอมม่า
                elements.append(self.parse_expression(0))
        if self.peek() and self.peek().type == 'RBRACKET':
            self.consume()
        return ListNode(elements=elements)

    def parse_dict(self) -> Node:
        items = []
        if self.peek() and self.peek().type != 'RCURLY':
            # พาร์ส Key:Value คู่แรก
            key_token = self.consume()
            # ยอมรับให้ Key เป็นได้ทั้งตัวแปร (IDENT) และข้อความ (STRING)
            if key_token.type not in ['IDENT', 'STRING']:
                raise ParseError("Dictionary key must be an identifier or string")
            
            key_name = key_token.value.strip('"') # ลบเครื่องหมายคำพูดออกถ้ามี
            
            if self.peek() and self.peek().value == ':':
                self.consume() # colon
            
            val = self.parse_expression(0)
            items.append((key_name, val))
            
            # พาร์สคู่ถัดไป
            while self.peek() and self.peek().value == ',':
                self.consume() # คอมม่า
                k = self.consume()
                if k.type not in ['IDENT', 'STRING']: 
                    raise ParseError("Dictionary key must be an identifier or string")
                
                k_name = k.value.strip('"')
                
                if self.peek() and self.peek().value == ':': self.consume()
                v = self.parse_expression(0)
                items.append((k_name, v))
                
        if self.peek() and self.peek().type == 'RCURLY':
            self.consume()
        return DictNode(items=items)

    def primary(self, token: Token) -> Node:
        if token.type == 'NUMBER':
            return LiteralNode(value=float(token.value))
        
        # --- เพิ่มการดักจับ STRING ---
        if token.type == 'STRING':
            return LiteralNode(value=token.value.strip('"'))
        # ------------------------------------
        
        # เพิ่มการดักจับ List และ Dict
        if token.type == 'LBRACKET':
            return self.parse_list()
        if token.type == 'LCURLY':
            return self.parse_dict()
        
        elif token.type in ['IDENT', 'FUNCTION']:
            name = token.value
            if self.peek() and self.peek().value == '(':
                self.consume()
                args = []
                if self.peek() and self.peek().value != ')':
                    args.append(self.parse_expression(0))
                if self.peek() and self.peek().value == ')':
                    self.consume()
                return FunctionCallNode(name=name, arguments=args)
            
            path = [name]
            while self.peek() and self.peek().value == '.':
                self.consume()
                part = self.consume()
                path.append(part.value)
            return VariableNode(path=tuple(path))
            
        raise ParseError(f"Unexpected token: {token.value}")