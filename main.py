import ast
import sys
from pathlib import Path
current_dir = Path(__file__).parent
sys.path.append(current_dir)
from src.data import ModuleInfo, FunctionInfo, ClassInfo, ArgumentInfo
from src.codeparser import FunctionParser, ClassParser, FileParser

def test_function_parser():
    source_code = '''
def example_function(param1: int, param2: str = "default", *args, kwonly1: float, kwonly2: bool = True, **kwargs) -> None:
    """This is an example function."""
    pass
'''
    node = ast.parse(source_code).body[0]  # 获取第一个节点，即函数定义
    parser = FunctionParser(node)
    print(parser)

def test_class_parser():
    source_code = '''
class ExampleClass(BaseClass):
    """This is an example class."""

    @classmethod
    def class_method(cls, param: int) -> str:
        """This is a class method."""
        return str(param)
'''
    node = ast.parse(source_code).body[0]  # 获取第一个节点，即类定义
    # 这里假设你有一个 ClassParser 类，类似于 FunctionParser
    parser = ClassParser(node)
    print(parser.parse())

def test_file_parser():
    from pprint import pprint
    file_parser = FileParser("src/codeparser.py")
    module_info = file_parser.parse()
    pprint(module_info)
    

if __name__ == "__main__":
    # import time
    # start = time.time()
    # test_function_parser()
    # func_end = time.time()
    # test_class_parser()
    # class_end = time.time()
    # print(f"Function parsing time: {func_end - start}s")
    # print(f"Class parsing time: {class_end - func_end}s")
    test_file_parser()
    print("test")