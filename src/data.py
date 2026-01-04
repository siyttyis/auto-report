from dataclasses import dataclass, field
from typing import Sequence, Optional

@dataclass
class ArgumentInfo:
    name: str
    type_hint: Optional[str] = "Any"
    default_value: Optional[str] = None

@dataclass
class FunctionInfo:
    name: str
    args: Sequence[str]
    return_type: Optional[str]
    docstring: Optional[str]
    decorators: Sequence[str]
    is_async: bool = False
    is_method: bool = False # 是否为类的方法

@dataclass
class ClassInfo:
    name: str
    bases: Sequence[str] = field(default_factory=list) 
    methods: Sequence[FunctionInfo] = field(default_factory=list)
    docstring: Optional[str] = None

@dataclass
class ModuleInfo:
    name: str
    classes: Sequence[ClassInfo] = field(default_factory=list)
    functions: Sequence[FunctionInfo] = field(default_factory=list)
    docstring: Optional[str] = None