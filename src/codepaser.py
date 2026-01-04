import ast
import sys
from pathlib import Path
from typing import List, Optional, Sequence


from src.data import ModuleInfo, FunctionInfo, ClassInfo, ArgumentInfo

class FunctionParser(ast.NodeVisitor):
    def __init__(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        super().__init__()
        self.node = node

    def parse(self) -> FunctionInfo:
        return FunctionInfo(
            name=self.node.name,
            args=self._parse_arguments(),
            return_type=self._get_return_type(),
            docstring=ast.get_docstring(self.node),
            decorators=self._parse_decorators(),
            is_async=isinstance(self.node, ast.AsyncFunctionDef),
        )

    def _parse_arguments(self) -> List[ArgumentInfo]:
        args_info: list[ast.arg] = []
        args = self.node.args
        # args.defaults
        default_args = [*args.posonlyargs, *args.args] # 合并位置参数，对应默认值 args.defaults
        default_vals = args.defaults
        offset = len(default_args) - len(default_vals)
        for i, arg in enumerate(default_args):
            default_value = None
            if i >= offset: # 有默认值
                default_value=ast.unparse(default_vals[i - offset]) if default_vals[i - offset] else None

            args_info.append(ArgumentInfo(
                name=arg.arg,
                type_hint=ast.unparse(arg.annotation) if arg.annotation else "Any",
                default_value=default_value
            ))

        # args.vararg 对应 *args
        if args.vararg:
            args_info.append(ArgumentInfo(
                name=f"*{args.vararg.arg}",
                type_hint=ast.unparse(args.vararg.annotation) if args.vararg.annotation else "Any",
                default_value=None
            ))

        # args.kwonlyargs 对应默认值 args.kw_defaults
        for arg, default_val in zip(args.kwonlyargs, args.kw_defaults):
            args_info.append(ArgumentInfo(
                name=arg.arg,
                type_hint=ast.unparse(arg.annotation) if arg.annotation else "Any",
                default_value=ast.unparse(default_val) if default_val else None
            ))
        
        # args.kwarg 对应 **kwargs
        if args.kwarg:
            args_info.append(ArgumentInfo(
                name=f"**{args.kwarg.arg}",
                type_hint=ast.unparse(args.kwarg.annotation) if args.kwarg.annotation else "Any",
                default_value=None
            ))
        return args_info

    def _get_return_type(self) -> Optional[str]:
        if self.node.returns:
            return ast.unparse(self.node.returns)
        return None

    def _parse_decorators(self) -> List[str]:
        decorators = []
        for decorator in self.node.decorator_list:
            decorators.append(f"@{ast.unparse(decorator)}")
        return decorators
    
    def __str__(self):
        return f"FunctionParser(name={self.node.name}, is_async={isinstance(self.node, ast.AsyncFunctionDef)}, return_type={self._get_return_type()})"

class ClassParser(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.class_info: Optional[ClassInfo] = None
        self.methods: Sequence[FunctionInfo] = []
