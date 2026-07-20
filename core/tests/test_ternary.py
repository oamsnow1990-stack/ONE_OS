from core.expression_engine.tokenizer import Tokenizer
from core.expression_engine.parser import Parser
from core.expression_engine.evaluator import Evaluator
from core.expression_engine.resolver import RuntimeResolver
from core.expression_engine.registry.function_registry import FunctionRegistry

# 1. Setup สภาพแวดล้อม
resolver = RuntimeResolver({}) # สำหรับตัวแปร
func_registry = FunctionRegistry() # สำหรับฟังก์ชัน
evaluator = Evaluator(resolver, func_registry)

def test_expression(expr: str):
    print(f"\n--- ทดสอบ Expression: {expr} ---")
    try:
        tokens = Tokenizer(expr).tokenize()
        node = Parser(tokens).parse()
        result = evaluator.evaluate(node)
        print(f"ผลลัพธ์ที่ได้: {result}")
        print(f"Type ของผลลัพธ์: {type(result)}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    # ทดสอบเงื่อนไขที่เป็นจริง (True)
    test_expression('10 > 5 ? "Yes" : "No"')
    
    # ทดสอบเงื่อนไขที่เป็นเท็จ (False)
    test_expression('1 == 2 ? "Pass" : "Fail"')
    
    # ทดสอบแบบ Advance: เอา Collections ซ้อนเข้าไปใน Ternary ด้วย!
    test_expression('5 * 2 == 10 ? [1, 2, 3] : {"status": "error"}')