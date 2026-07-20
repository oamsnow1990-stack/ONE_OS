from core.expression_engine.tokenizer import Tokenizer
from core.expression_engine.parser import Parser
from core.expression_engine.evaluator import Evaluator
from core.expression_engine.resolver import RuntimeResolver
from core.expression_engine.registry.function_registry import FunctionRegistry

# 1. Setup Environment (จำลองตัวแปรและฟังก์ชัน)
resolver = RuntimeResolver({}) # สำหรับตัวแปร
func_registry = FunctionRegistry() # สำหรับฟังก์ชัน
evaluator = Evaluator(resolver, func_registry)

def test_expression(expr: str):
    print(f"\n--- ทดสอบ Expression: {expr} ---")
    try:
        # Tokenize -> Parse -> Evaluate
        tokens = Tokenizer(expr).tokenize()
        node = Parser(tokens).parse()
        result = evaluator.evaluate(node)
        print(f"ผลลัพธ์ที่ได้: {result}")
        print(f"Type ของผลลัพธ์: {type(result)}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

# 2. รายการทดสอบ
if __name__ == "__main__":
    # Test List with Math
    test_expression("[1 + 2, 4 / 2, 10 * 5]")
    
    # Test Dict with Math
    test_expression("{ \"a\": 1 + 1, \"b\": 10 * 10 }")
    
    # Test Nested Collection
    test_expression("{ \"data\": [1, 2, 3], \"nested\": { \"x\": 10 } }")