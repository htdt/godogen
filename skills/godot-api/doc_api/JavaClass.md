## JavaClass <- RefCounted

Represents a class from the Java Native Interface. It is returned from `JavaClassWrapper.wrap`. **Note:** This class only works on Android. On any other platform, this class does nothing. **Note:** This class is not to be confused with JavaScriptObject.

**Methods:**
- get_java_class_name() -> String - Returns the Java class name.
- get_java_method_list() -> Dictionary[] - Returns the object's Java methods and their signatures as an Array of dictionaries, in the same format as `Object.get_method_list`.
- get_java_parent_class() -> JavaClass - Returns a JavaClass representing the Java parent class of this class.
- has_java_method(method: StringName) -> bool - Returns `true` if the given `method` name exists in the object's Java methods.

