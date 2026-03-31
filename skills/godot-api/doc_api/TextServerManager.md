## TextServerManager <- Object

TextServerManager is the API backend for loading, enumerating, and switching TextServers. **Note:** Switching text server at runtime is possible, but will invalidate all fonts and text buffers. Make sure to unload all controls, fonts, and themes before doing so.

**Methods:**
- add_interface(interface: TextServer) - Registers a TextServer interface.
- find_interface(name: String) -> TextServer - Finds an interface by its `name`.
- get_interface(idx: int) -> TextServer - Returns the interface registered at a given index.
- get_interface_count() -> int - Returns the number of interfaces currently registered.
- get_interfaces() -> Dictionary[] - Returns a list of available interfaces, with the index and name of each interface.
- get_primary_interface() -> TextServer - Returns the primary TextServer interface currently in use.
- remove_interface(interface: TextServer) - Removes an interface. All fonts and shaped text caches should be freed before removing an interface.
- set_primary_interface(index: TextServer) - Sets the primary TextServer interface.

**Signals:**
- interface_added(interface_name: StringName) - Emitted when a new interface has been added.
- interface_removed(interface_name: StringName) - Emitted when an interface is removed.

