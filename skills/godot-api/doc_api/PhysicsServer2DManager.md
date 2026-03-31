## PhysicsServer2DManager <- Object

PhysicsServer2DManager is the API for registering PhysicsServer2D implementations and for setting the default implementation. **Note:** It is not possible to switch physics servers at runtime. This class is only used on startup at the server initialization level, by Godot itself and possibly by GDExtensions.

**Methods:**
- register_server(name: String, create_callback: Callable) - Register a PhysicsServer2D implementation by passing a `name` and a Callable that returns a PhysicsServer2D object.
- set_default_server(name: String, priority: int) - Set the default PhysicsServer2D implementation to the one identified by `name`, if `priority` is greater than the priority of the current default implementation.

