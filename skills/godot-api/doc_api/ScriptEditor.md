## ScriptEditor <- PanelContainer

Godot editor's script editor. **Note:** This class shouldn't be instantiated directly. Instead, access the singleton using `EditorInterface.get_script_editor`.

**Methods:**
- clear_docs_from_script(script: Script) - Removes the documentation for the given `script`. **Note:** This should be called whenever the script is changed to keep the open documentation state up to date.
- get_breakpoints() -> PackedStringArray - Returns array of breakpoints.
- get_current_editor() -> ScriptEditorBase - Returns the ScriptEditorBase object that the user is currently editing.
- get_current_script() -> Script - Returns a Script that is currently active in editor.
- get_open_script_editors() -> ScriptEditorBase[] - Returns an array with all ScriptEditorBase objects which are currently open in editor.
- get_open_scripts() -> Script[] - Returns an array with all Script objects which are currently open in editor.
- get_unsaved_files() -> PackedStringArray - Returns an array of file paths of scripts with unsaved changes open in the editor.
- goto_help(topic: String) - Opens help for the given topic. The `topic` is an encoded string that controls which class, method, constant, signal, annotation, property, or theme item should be focused. The supported `topic` formats include `class_name:class`, `class_method:class:method`, `class_constant:class:constant`, `class_signal:class:signal`, `class_annotation:class:@annotation`, `class_property:class:property`, and `class_theme_item:class:item`, where `class` is the class name, `method` is the method name, `constant` is the constant name, `signal` is the signal name, `annotation` is the annotation name, `property` is the property name, and `item` is the theme item.
- goto_line(line_number: int) - Goes to the specified line in the current script.
- open_script_create_dialog(base_name: String, base_path: String) - Opens the script create dialog. The script will extend `base_name`. The file extension can be omitted from `base_path`. It will be added based on the selected scripting language.
- register_syntax_highlighter(syntax_highlighter: EditorSyntaxHighlighter) - Registers the EditorSyntaxHighlighter to the editor, the EditorSyntaxHighlighter will be available on all open scripts. **Note:** Does not apply to scripts that are already opened.
- reload_open_files() - Reloads all currently opened files. This should be used when opened files are changed outside of the script editor. The user may be prompted to resolve file conflicts, see `EditorSettings.text_editor/behavior/files/auto_reload_scripts_on_external_change`.
- save_all_scripts() - Saves all open scripts.
- unregister_syntax_highlighter(syntax_highlighter: EditorSyntaxHighlighter) - Unregisters the EditorSyntaxHighlighter from the editor. **Note:** The EditorSyntaxHighlighter will still be applied to scripts that are already opened.
- update_docs_from_script(script: Script) - Updates the documentation for the given `script`. **Note:** This should be called whenever the script is changed to keep the open documentation state up to date.

**Signals:**
- editor_script_changed(script: Script) - Emitted when user changed active script. Argument is a freshly activated Script.
- script_close(script: Script) - Emitted when editor is about to close the active script. Argument is a Script that is going to be closed.

