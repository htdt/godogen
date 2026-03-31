## ScriptLanguageExtension <- ScriptLanguage

**Methods:**
- _add_global_constant(name: StringName, value: Variant)
- _add_named_global_constant(name: StringName, value: Variant)
- _auto_indent_code(code: String, from_line: int, to_line: int) -> String
- _can_inherit_from_file() -> bool
- _can_make_function() -> bool
- _complete_code(code: String, path: String, owner: Object) -> Dictionary
- _create_script() -> Object
- _debug_get_current_stack_info() -> Dictionary[]
- _debug_get_error() -> String
- _debug_get_globals(max_subitems: int, max_depth: int) -> Dictionary
- _debug_get_stack_level_count() -> int
- _debug_get_stack_level_function(level: int) -> String
- _debug_get_stack_level_instance(level: int) -> void*
- _debug_get_stack_level_line(level: int) -> int
- _debug_get_stack_level_locals(level: int, max_subitems: int, max_depth: int) -> Dictionary
- _debug_get_stack_level_members(level: int, max_subitems: int, max_depth: int) -> Dictionary
- _debug_get_stack_level_source(level: int) -> String - Returns the source associated with a given debug stack position.
- _debug_parse_stack_level_expression(level: int, expression: String, max_subitems: int, max_depth: int) -> String
- _find_function(function: String, code: String) -> int - Returns the line where the function is defined in the code, or `-1` if the function is not present.
- _finish()
- _frame()
- _get_built_in_templates(object: StringName) -> Dictionary[]
- _get_comment_delimiters() -> PackedStringArray
- _get_doc_comment_delimiters() -> PackedStringArray
- _get_extension() -> String
- _get_global_class_name(path: String) -> Dictionary
- _get_name() -> String
- _get_public_annotations() -> Dictionary[]
- _get_public_constants() -> Dictionary
- _get_public_functions() -> Dictionary[]
- _get_recognized_extensions() -> PackedStringArray
- _get_reserved_words() -> PackedStringArray
- _get_string_delimiters() -> PackedStringArray
- _get_type() -> String
- _handles_global_class_type(type: String) -> bool
- _has_named_classes() -> bool
- _init()
- _is_control_flow_keyword(keyword: String) -> bool
- _is_using_templates() -> bool
- _lookup_code(code: String, symbol: String, path: String, owner: Object) -> Dictionary
- _make_function(class_name: String, function_name: String, function_args: PackedStringArray) -> String
- _make_template(template: String, class_name: String, base_class_name: String) -> Script
- _open_in_external_editor(script: Script, line: int, column: int) -> int
- _overrides_external_editor() -> bool
- _preferred_file_name_casing() -> int
- _profiling_get_accumulated_data(info_array: ScriptLanguageExtensionProfilingInfo*, info_max: int) -> int
- _profiling_get_frame_data(info_array: ScriptLanguageExtensionProfilingInfo*, info_max: int) -> int
- _profiling_set_save_native_calls(enable: bool)
- _profiling_start()
- _profiling_stop()
- _reload_all_scripts()
- _reload_scripts(scripts: Array, soft_reload: bool)
- _reload_tool_script(script: Script, soft_reload: bool)
- _remove_named_global_constant(name: StringName)
- _supports_builtin_mode() -> bool
- _supports_documentation() -> bool
- _thread_enter()
- _thread_exit()
- _validate(script: String, path: String, validate_functions: bool, validate_errors: bool, validate_warnings: bool, validate_safe_lines: bool) -> Dictionary
- _validate_path(path: String) -> String

**Enums:**
**LookupResultType:** LOOKUP_RESULT_SCRIPT_LOCATION=0, LOOKUP_RESULT_CLASS=1, LOOKUP_RESULT_CLASS_CONSTANT=2, LOOKUP_RESULT_CLASS_PROPERTY=3, LOOKUP_RESULT_CLASS_METHOD=4, LOOKUP_RESULT_CLASS_SIGNAL=5, LOOKUP_RESULT_CLASS_ENUM=6, LOOKUP_RESULT_CLASS_TBD_GLOBALSCOPE=7, LOOKUP_RESULT_CLASS_ANNOTATION=8, LOOKUP_RESULT_LOCAL_CONSTANT=9, ...
**CodeCompletionLocation:** LOCATION_LOCAL=0, LOCATION_PARENT_MASK=256, LOCATION_OTHER_USER_CODE=512, LOCATION_OTHER=1024
  - LOCATION_LOCAL: The option is local to the location of the code completion query - e.g. a local variable. Subsequent value of location represent options from the outer class, the exact value represent how far they are (in terms of inner classes).
  - LOCATION_PARENT_MASK: The option is from the containing class or a parent class, relative to the location of the code completion query. Perform a bitwise OR with the class depth (e.g. `0` for the local class, `1` for the parent, `2` for the grandparent, etc.) to store the depth of an option in the class or a parent class.
  - LOCATION_OTHER_USER_CODE: The option is from user code which is not local and not in a derived class (e.g. Autoload Singletons).
  - LOCATION_OTHER: The option is from other engine code, not covered by the other enum constants - e.g. built-in classes.
**CodeCompletionKind:** CODE_COMPLETION_KIND_CLASS=0, CODE_COMPLETION_KIND_FUNCTION=1, CODE_COMPLETION_KIND_SIGNAL=2, CODE_COMPLETION_KIND_VARIABLE=3, CODE_COMPLETION_KIND_MEMBER=4, CODE_COMPLETION_KIND_ENUM=5, CODE_COMPLETION_KIND_CONSTANT=6, CODE_COMPLETION_KIND_NODE_PATH=7, CODE_COMPLETION_KIND_FILE_PATH=8, CODE_COMPLETION_KIND_PLAIN_TEXT=9, ...

