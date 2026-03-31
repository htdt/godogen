## NavigationServer2DManager <- Object

NavigationServer2DManager is the API for registering NavigationServer2D implementations and setting the default implementation. **Note:** It is not possible to switch servers at runtime. This class is only used on startup at the server initialization level.

**Methods:**
- register_server(name: String, create_callback: Callable) - Registers a NavigationServer2D implementation by passing a `name` and a Callable that returns a NavigationServer2D object.
- set_default_server(name: String, priority: int) - Sets the default NavigationServer2D implementation to the one identified by `name`, if `priority` is greater than the priority of the current default implementation.

