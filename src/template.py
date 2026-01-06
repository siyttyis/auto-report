from dataclasses import dataclass, field

@dataclass
class FunctionTemplate:
    name_template: str = "{} `{}{}{}`" # heading level, async, class name, function name

    arg_title_template: str = "{} Args:"  # heading level
    default_template: str = "- `{}`: `{}` = `{}`" # Argument name, type hint, default value
    vkarg_template: str = "- `{}`"  # Argument name only for *args and **kwargs

    return_title_template: str = "{} Returns:" # heading level
    return_type_template: str = "- `{}`"  # Return type

    docstring_title_template: str = "{} Description:"  # heading level
    docstring_content_template: str = "{}"  # Docstring content
    
@dataclass
class ClassTemplate:
    name_template: str = "{} `class {}`" # heading level, class name
    
    bases_title_template: str = "{} Bases:"  # heading level
    bases_template: str = "- Bases: {}"  # base classes
    
    decorators_title_template: str = "{} Decorators:"  # heading level
    decorator_template: str = "- {}"  # decorator name

    methods_title_template: str = "{} Methods:"  # heading level
    method_template: FunctionTemplate = field(default_factory=FunctionTemplate)

    docstring_title_template: str = "{} Description:"  # heading level
    docstring_content_template: str = "{}"  # Docstring content

@dataclass
class ModuleTemplate:
    name_template: str = "{} Module: *{}*"  # heading level, module name

    classes_title_template: str = "{} Classes:"  # heading level
    class_template: ClassTemplate = field(default_factory=ClassTemplate)

    functions_title_template: str = "{} Functions:"  # heading level
    function_template: FunctionTemplate = field(default_factory=FunctionTemplate)

    docstring_title_template: str = "{} Description:"  # heading level
    docstring_content_template: str = "{}"  # Docstring content