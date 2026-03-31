## GDExtension <- Resource

The GDExtension resource type represents a which can expand the functionality of the engine. The GDExtensionManager singleton is responsible for loading, reloading, and unloading GDExtension resources. **Note:** GDExtension itself is not a scripting language and has no relation to GDScript resources.

**Methods:**
- get_minimum_library_initialization_level() -> int - Returns the lowest level required for this extension to be properly initialized (see the `InitializationLevel` enum).
- is_library_open() -> bool - Returns `true` if this extension's library has been opened.

**Enums:**
**InitializationLevel:** INITIALIZATION_LEVEL_CORE=0, INITIALIZATION_LEVEL_SERVERS=1, INITIALIZATION_LEVEL_SCENE=2, INITIALIZATION_LEVEL_EDITOR=3
  - INITIALIZATION_LEVEL_CORE: The library is initialized at the same time as the core features of the engine.
  - INITIALIZATION_LEVEL_SERVERS: The library is initialized at the same time as the engine's servers (such as RenderingServer or PhysicsServer3D).
  - INITIALIZATION_LEVEL_SCENE: The library is initialized at the same time as the engine's scene-related classes.
  - INITIALIZATION_LEVEL_EDITOR: The library is initialized at the same time as the engine's editor classes. Only happens when loading the GDExtension in the editor.

