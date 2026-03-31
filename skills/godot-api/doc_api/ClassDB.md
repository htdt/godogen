## ClassDB <- Object

Provides access to metadata stored for every available engine class. **Note:** Script-defined classes with `class_name` are not part of ClassDB, so they will not return reflection data such as a method or property list. However, GDExtension-defined classes *are* part of ClassDB, so they will return reflection data.

**Methods:**
- can_instantiate(class: StringName) -> bool - Returns `true` if objects can be instantiated from the specified `class`, otherwise returns `false`.
- class_call_static(class: StringName, method: StringName) -> Variant - Calls a static method on a class.
- class_exists(class: StringName) -> bool - Returns whether the specified `class` is available or not.
- class_get_api_type(class: StringName) -> int - Returns the API type of the specified `class`.
- class_get_enum_constants(class: StringName, enum: StringName, no_inheritance: bool = false) -> PackedStringArray - Returns an array with all the keys in `enum` of `class` or its ancestry.
- class_get_enum_list(class: StringName, no_inheritance: bool = false) -> PackedStringArray - Returns an array with all the enums of `class` or its ancestry.
- class_get_integer_constant(class: StringName, name: StringName) -> int - Returns the value of the integer constant `name` of `class` or its ancestry. Always returns 0 when the constant could not be found.
- class_get_integer_constant_enum(class: StringName, name: StringName, no_inheritance: bool = false) -> StringName - Returns which enum the integer constant `name` of `class` or its ancestry belongs to.
- class_get_integer_constant_list(class: StringName, no_inheritance: bool = false) -> PackedStringArray - Returns an array with the names all the integer constants of `class` or its ancestry.
- class_get_method_argument_count(class: StringName, method: StringName, no_inheritance: bool = false) -> int - Returns the number of arguments of the method `method` of `class` or its ancestry if `no_inheritance` is `false`.
- class_get_method_list(class: StringName, no_inheritance: bool = false) -> Dictionary[] - Returns an array with all the methods of `class` or its ancestry if `no_inheritance` is `false`. Every element of the array is a Dictionary with the following keys: `args`, `default_args`, `flags`, `id`, `name`, `return: (class_name, hint, hint_string, name, type, usage)`. **Note:** In exported release builds the debug info is not available, so the returned dictionaries will contain only method names.
- class_get_property(object: Object, property: StringName) -> Variant - Returns the value of `property` of `object` or its ancestry.
- class_get_property_default_value(class: StringName, property: StringName) -> Variant - Returns the default value of `property` of `class` or its ancestor classes.
- class_get_property_getter(class: StringName, property: StringName) -> StringName - Returns the getter method name of `property` of `class`.
- class_get_property_list(class: StringName, no_inheritance: bool = false) -> Dictionary[] - Returns an array with all the properties of `class` or its ancestry if `no_inheritance` is `false`.
- class_get_property_setter(class: StringName, property: StringName) -> StringName - Returns the setter method name of `property` of `class`.
- class_get_signal(class: StringName, signal: StringName) -> Dictionary - Returns the `signal` data of `class` or its ancestry. The returned value is a Dictionary with the following keys: `args`, `default_args`, `flags`, `id`, `name`, `return: (class_name, hint, hint_string, name, type, usage)`.
- class_get_signal_list(class: StringName, no_inheritance: bool = false) -> Dictionary[] - Returns an array with all the signals of `class` or its ancestry if `no_inheritance` is `false`. Every element of the array is a Dictionary as described in `class_get_signal`.
- class_has_enum(class: StringName, name: StringName, no_inheritance: bool = false) -> bool - Returns whether `class` or its ancestry has an enum called `name` or not.
- class_has_integer_constant(class: StringName, name: StringName) -> bool - Returns whether `class` or its ancestry has an integer constant called `name` or not.
- class_has_method(class: StringName, method: StringName, no_inheritance: bool = false) -> bool - Returns whether `class` (or its ancestry if `no_inheritance` is `false`) has a method called `method` or not.
- class_has_signal(class: StringName, signal: StringName) -> bool - Returns whether `class` or its ancestry has a signal called `signal` or not.
- class_set_property(object: Object, property: StringName, value: Variant) -> int - Sets `property` value of `object` to `value`.
- get_class_list() -> PackedStringArray - Returns the names of all engine classes available. **Note:** Script-defined classes with `class_name` are not included in this list. Use `ProjectSettings.get_global_class_list` to get a list of script-defined classes instead.
- get_inheriters_from_class(class: StringName) -> PackedStringArray - Returns the names of all engine classes that directly or indirectly inherit from `class`.
- get_parent_class(class: StringName) -> StringName - Returns the parent class of `class`.
- instantiate(class: StringName) -> Variant - Creates an instance of `class`.
- is_class_enabled(class: StringName) -> bool - Returns whether this `class` is enabled or not.
- is_class_enum_bitfield(class: StringName, enum: StringName, no_inheritance: bool = false) -> bool - Returns whether `class` (or its ancestor classes if `no_inheritance` is `false`) has an enum called `enum` that is a bitfield.
- is_parent_class(class: StringName, inherits: StringName) -> bool - Returns whether `inherits` is an ancestor of `class` or not.

**Enums:**
**APIType:** API_CORE=0, API_EDITOR=1, API_EXTENSION=2, API_EDITOR_EXTENSION=3, API_NONE=4
  - API_CORE: Native Core class type.
  - API_EDITOR: Native Editor class type.
  - API_EXTENSION: GDExtension class type.
  - API_EDITOR_EXTENSION: GDExtension Editor class type.
  - API_NONE: Unknown class type.

