## JNISingleton <- Object

The JNISingleton is implemented only in the Android export. It's used to call methods and connect signals from an Android plugin written in Java or Kotlin. Methods and signals can be called and connected to the JNISingleton as if it is a Node. See for more information.

**Methods:**
- has_java_method(method: StringName) -> bool - Returns `true` if the given `method` name exists in the JNISingleton's Java methods.

