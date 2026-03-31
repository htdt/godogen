## GDExtensionManager <- Object

The GDExtensionManager loads, initializes, and keeps track of all available GDExtension libraries in the project. **Note:** Do not worry about GDExtension unless you know what you are doing.

**Methods:**
- get_extension(path: String) -> GDExtension - Returns the GDExtension at the given file `path`, or `null` if it has not been loaded or does not exist.
- get_loaded_extensions() -> PackedStringArray - Returns the file paths of all currently loaded extensions.
- is_extension_loaded(path: String) -> bool - Returns `true` if the extension at the given file `path` has already been loaded successfully. See also `get_loaded_extensions`.
- load_extension(path: String) -> int - Loads an extension by absolute file path. The `path` needs to point to a valid GDExtension. Returns `LOAD_STATUS_OK` if successful.
- load_extension_from_function(path: String, init_func: const GDExtensionInitializationFunction*) -> int - Loads the extension already in address space via the given path and initialization function. The `path` needs to be unique and start with `"libgodot://"`. Returns `LOAD_STATUS_OK` if successful.
- reload_extension(path: String) -> int - Reloads the extension at the given file path. The `path` needs to point to a valid GDExtension, otherwise this method may return either `LOAD_STATUS_NOT_LOADED` or `LOAD_STATUS_FAILED`. **Note:** You can only reload extensions in the editor. In release builds, this method always fails and returns `LOAD_STATUS_FAILED`.
- unload_extension(path: String) -> int - Unloads an extension by file path. The `path` needs to point to an already loaded GDExtension, otherwise this method returns `LOAD_STATUS_NOT_LOADED`.

**Signals:**
- extension_loaded(extension: GDExtension) - Emitted after the editor has finished loading a new extension. **Note:** This signal is only emitted in editor builds.
- extension_unloading(extension: GDExtension) - Emitted before the editor starts unloading an extension. **Note:** This signal is only emitted in editor builds.
- extensions_reloaded - Emitted after the editor has finished reloading one or more extensions.

**Enums:**
**LoadStatus:** LOAD_STATUS_OK=0, LOAD_STATUS_FAILED=1, LOAD_STATUS_ALREADY_LOADED=2, LOAD_STATUS_NOT_LOADED=3, LOAD_STATUS_NEEDS_RESTART=4
  - LOAD_STATUS_OK: The extension has loaded successfully.
  - LOAD_STATUS_FAILED: The extension has failed to load, possibly because it does not exist or has missing dependencies.
  - LOAD_STATUS_ALREADY_LOADED: The extension has already been loaded.
  - LOAD_STATUS_NOT_LOADED: The extension has not been loaded.
  - LOAD_STATUS_NEEDS_RESTART: The extension requires the application to restart to fully load.

