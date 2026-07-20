import re
from typing import List, NamedTuple
from .errors import LexerError

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class Tokenizer:
    TOKEN_SPEC = [
        ('LBRACE',   r'\{\{'), 
        ('RBRACE',   r'\}\}'), 
        ('LBRACKET', r'\['),    
        ('RBRACKET', r'\]'),    
        ('LCURLY',   r'\{'),    
        ('RCURLY',   r'\}'),    
        ('NUMBER',   r'\d+(\.\d*)?'),
        ('STRING',   r'"[^"]*"'),        # รองรับข้อความในเครื่องหมาย "..."
        ('FUNCTION', r'[a-zA-Z_]\w*(?=\()'),
        ('IDENT',    r'[a-zA-Z_]\w*'),
        ('PIPE',     r'\|'),
        # --- แก้ไขบรรทัดนี้: รองรับ ==, != และเครื่องหมายเดี่ยวทั้งหมด ---
        ('OP',       r'==|!=|[+\-*/.(),:?<>=]'), 
        ('SKIP',     r'\s+'),
        ('MISMATCH', r'.'),
    ]

    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        regex = '|'.join('(?P<%s>%s)' % pair for pair in self.TOKEN_SPEC)
        line_num = 1
        line_start = 0
        
        for mo in re.finditer(regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            
            if kind == 'SKIP':
                if '\n' in value:
                    line_num += value.count('\n')
                    line_start = mo.end()
                continue
            elif kind == 'MISMATCH':
                raise LexerError(f'Unexpected character {value!r} at line {line_num}, col {column}')
            
            self.tokens.append(Token(kind, value, line_num, column))
            
        return self.tokens