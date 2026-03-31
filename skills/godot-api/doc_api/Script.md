## Script <- Resource

A class stored as a resource. A script extends the functionality of all objects that instantiate it. This is the base class for all scripts and should not be used directly. Trying to create a new script with this class will result in an error. The `new` method of a script subclass creates a new instance. `Object.set_script` extends an existing object, if that object's class matches one of the script's base classes.

**Props:**
- source_code: String

- **source_code**: The script source code or an empty string if source code is not available. When set, does not reload the class implementation automatically.

**Methods:**
- can_instantiate() -> bool - Returns `true` if the script can be instantiated.
- get_base_script() -> Script - Returns the script directly inherited by this script.
- get_global_name() -> StringName - Returns the class name associated with the script, if there is one. Returns an empty string otherwise. To give the script a global name, you can use the `class_name` keyword in GDScript and the `GlobalClass` attribute in C#.
- get_instance_base_type() -> StringName - Returns the script's base type.
- get_property_default_value(property: StringName) -> Variant - Returns the default value of the specified property.
- get_rpc_config() -> Variant - Returns a Dictionary mapping method names to their RPC configuration defined by this script.
- get_script_constant_map() -> Dictionary - Returns a dictionary containing constant names and their values.
- get_script_method_list() -> Dictionary[] - Returns the list of methods in this Script. **Note:** The dictionaries returned by this method are formatted identically to those returned by `Object.get_method_list`.
- get_script_property_list() -> Dictionary[] - Returns the list of properties in this Script. **Note:** The dictionaries returned by this method are formatted identically to those returned by `Object.get_property_list`.
- get_script_signal_list() -> Dictionary[] - Returns the list of signals defined in this Script. **Note:** The dictionaries returned by this method are formatted identically to those returned by `Object.get_signal_list`.
- has_script_method(method_name: StringName) -> bool - Returns `true` if the script, or a base class, defines a method with the given name.
- has_script_signal(signal_name: StringName) -> bool - Returns `true` if the script, or a base class, defines a signal with the given name.
- has_source_code() -> bool - Returns `true` if the script contains non-empty source code. **Note:** If a script does not have source code, this does not mean that it is invalid or unusable. For example, a GDScript that was exported with binary tokenization has no source code, but still behaves as expected and could be instantiated. This can be checked with `can_instantiate`.
- instance_has(base_object: Object) -> bool - Returns `true` if `base_object` is an instance of this script.
- is_abstract() -> bool - Returns `true` if the script is an abstract script. An abstract script does not have a constructor and cannot be instantiated.
- is_tool() -> bool - Returns `true` if the script is a tool script. A tool script can run in the editor.
- reload(keep_state: bool = false) -> int - Reloads the script's class implementation. Returns an error code.

