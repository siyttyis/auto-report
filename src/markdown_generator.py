from src.data import ModuleInfo, FunctionInfo, ClassInfo, ArgumentInfo
from src.codeparser import FileParser
from src.template import FunctionTemplate, ClassTemplate, ModuleTemplate
from typing import Optional, Literal

class MarkdownGenerator:
    def __init__(
            self,
            file_path: str,
            module_info: Optional[ModuleInfo] = None,
            class_info: Optional[ClassInfo] = None,
            function_info: Optional[FunctionInfo] = None,
            module_temlate: ModuleTemplate = ModuleTemplate(),
            class_template: ClassTemplate = ClassTemplate(),
            function_template: FunctionTemplate = FunctionTemplate(),
    ):
        self.file_path = file_path
        self.module_info = module_info
        self.class_info = class_info
        self.function_info = function_info
        self.module_template = module_temlate
        self.class_template = class_template
        self.function_template = function_template
    
    def load_file(self):
        parser = FileParser(self.file_path)
        self.module_info = parser.parse()

    def generate(self, save_path: str, file_path: Optional[str] = None) -> list[str]:
        if file_path:
            self.file_path = file_path
            self.load_file()
        self.lines = []
        if self.module_info:
            self.lines = self._generate_module_markdown()
        elif self.class_info:
            self.lines = self._generate_class_markdown()
        elif self.function_info:
            self.lines = self._generate_function_markdown()
        else:
            raise ValueError("No information provided to generate markdown.")
        self.save_markdown(self.lines, save_path)
        return self.lines
    
    def _generate_function_markdown(self, function_info: Optional[FunctionInfo] = None, heading_level: int = 1) -> list[str]:
        if function_info is None:
            if self.function_info is None:
                raise ValueError("No FunctionInfo provided for markdown generation.")
            else:
                function_info = self.function_info
        lines = []
        head_prefix = "#" * heading_level
        class_str = f"{function_info.class_name}." if function_info.class_name else ""
        async_str = "async " if function_info.is_async else ""
        # func_str = f"\_\_{function_info.name[2:]}" if function_info.name.startswith("__") and function_info.name.endswith("__") else function_info.name
        head = self.function_template.name_template.format(head_prefix, async_str, class_str, function_info.name)
        # head = f"{head_prefix} {async_str} {class_str}{function_info.name}"
        lines.append(head)
        sub_prefix = "#" * ( heading_level + 1 )
        # args
        lines.append(self.function_template.arg_title_template.format(sub_prefix))
        for arg in function_info.args:
            if arg.name.startswith("*"):
                arg_str = self.function_template.vkarg_template.format(arg.name)
            else:
                arg_str = self.function_template.default_template.format(arg.name, arg.type_hint, arg.default_value if arg.default_value is not None else "None")
            lines.append(arg_str)
        # return 
        lines.append(self.function_template.return_title_template.format(sub_prefix))
        lines.append(self.function_template.return_type_template.format(function_info.return_type if function_info.return_type else "None"))
        # docstring
        lines.append(self.function_template.docstring_title_template.format(sub_prefix))
        if not function_info.docstring:
            function_info.docstring = "No docstring provided."
        lines.append(self.function_template.docstring_content_template.format(function_info.docstring))
        
        return lines

    def _generate_class_markdown(self, class_info: Optional[ClassInfo] = None, heading_level: int = 1) -> list[str]:
        if class_info is None:
            if self.class_info is None:
                raise ValueError("No ClassInfo provided for markdown generation.")
            else:
                class_info = self.class_info
        lines = []
        head_prefix = "#" * heading_level
        head = self.class_template.name_template.format(head_prefix, class_info.name)
        lines.append(head)
        sub_prefix = "#" * ( heading_level + 1 )
        # bases
        lines.append(self.class_template.bases_title_template.format(sub_prefix))
        for base in class_info.bases:
            lines.append(self.class_template.bases_template.format(base))
        # decorators
        lines.append(self.class_template.decorators_title_template.format(sub_prefix))
        for decorator in class_info.decorators:
            lines.append(self.class_template.decorator_template.format(decorator))
        # methods
        lines.append(self.class_template.methods_title_template.format(sub_prefix))
        for method in class_info.methods:
            method_lines = self._generate_function_markdown(method, heading_level + 2)
            lines.extend(method_lines)
        # docstring
        lines.append(self.class_template.docstring_title_template.format(sub_prefix))
        if not class_info.docstring:
            class_info.docstring = "No docstring provided."
        lines.append(self.class_template.docstring_content_template.format(class_info.docstring))

        return lines

    def _generate_module_markdown(self, file_info: Optional[ModuleInfo] = None, heading_level: int = 1) -> list[str]:
        if file_info is None:
            if self.module_info is None:
                raise ValueError("No ModuleInfo provided for markdown generation.")
            else:
                file_info = self.module_info
        lines = []
        head_prefix = "#" * heading_level
        head = f"{head_prefix} Module: {file_info.name}"
        lines.append(head)
        sub_prefix = "#" * ( heading_level + 1 )
        # docstring
        lines.append(self.module_template.docstring_title_template.format(sub_prefix))
        if not file_info.docstring:
            file_info.docstring = "No docstring provided."
        lines.append(self.module_template.docstring_content_template.format(file_info.docstring))
        # classes
        lines.append(self.module_template.classes_title_template.format(sub_prefix))
        for class_info in file_info.classes:
            class_lines = self._generate_class_markdown(class_info, heading_level + 2)
            lines.extend(class_lines)
        # functions
        lines.append(self.module_template.functions_title_template.format(sub_prefix))
        for function_info in file_info.functions:
            function_lines = self._generate_function_markdown(function_info, heading_level + 2)
            lines.extend(function_lines)
        
        return lines
    
    def load_template(self, template: str, mode: str = Literal["module", "class", "function"]):
        pass

    @staticmethod
    def save_markdown(lines: list[str], save_path: str):
        with open(save_path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"Markdown saved to {save_path}")