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
    args: Sequence[ArgumentInfo]
    return_type: Optional[str]
    docstring: Optional[str]
    decorators: Sequence[str]
    is_async: bool = False
    class_name: Optional[str] = None

@dataclass
class ClassInfo:
    name: str
    bases: Sequence[str]
    methods: Sequence[FunctionInfo]
    docstring: Optional[str]
    decorators: Sequence[str]

@dataclass
class ModuleInfo:
    name: str
    classes: Sequence[ClassInfo]
    functions: Sequence[FunctionInfo]
    docstring: Optional[str] = None