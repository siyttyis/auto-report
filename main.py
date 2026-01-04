import ast
import sys
from pathlib import Path
current_dir = Path(__file__).parent
sys.path.append(current_dir)
from src.data import ModuleInfo, FunctionInfo, ClassInfo, ArgumentInfo
from src.codepaser import FunctionParser

def test_function_parser():
    source_code = '''
def example_function(param1: int, param2: str = "default", *args, kwonly1: float, kwonly2: bool = True, **kwargs) -> None:
    """This is an example function."""
    pass
'''
    node = ast.parse(source_code).body[0]  # 获取第一个节点，即函数定义
    parser = FunctionParser(node)
    print(parser)
if __name__ == "__main__":
    test_function_parser()