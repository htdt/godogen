## JavaClassWrapper <- Object

The JavaClassWrapper singleton provides a way for the Godot application to send and receive data through the (JNI). **Note:** This singleton is only available in Android builds. **Warning:** When calling Java methods, be sure to check `JavaClassWrapper.get_exception` to check if the method threw an exception.

**Methods:**
- get_exception() -> JavaObject - Returns the Java exception from the last call into a Java class. If there was no exception, it will return `null`. **Note:** This method only works on Android. On every other platform, this method will always return `null`.
- wrap(name: String) -> JavaClass - Wraps a class defined in Java, and returns it as a JavaClass Object type that Godot can interact with. When wrapping inner (nested) classes, use `$` instead of `.` to separate them. For example, `JavaClassWrapper.wrap("android.view.WindowManager$LayoutParams")` wraps the **WindowManager.LayoutParams** class. **Note:** To invoke a constructor, call a method with the same name as the class. For example: **Note:** This method only works on Android. On every other platform, this method does nothing and returns an empty JavaClass.

