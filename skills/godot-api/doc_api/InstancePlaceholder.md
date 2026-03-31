## InstancePlaceholder <- Node

Turning on the option **Load As Placeholder** for an instantiated scene in the editor causes it to be replaced by an InstancePlaceholder when running the game, this will not replace the node in the editor. This makes it possible to delay actually loading the scene until calling `create_instance`. This is useful to avoid loading large scenes all at once by loading parts of it selectively. **Note:** Like Node, InstancePlaceholder does not have a transform. This causes any child nodes to be positioned relatively to the Viewport origin, rather than their parent as displayed in the editor. Replacing the placeholder with a scene with a transform will transform children relatively to their parent again.

**Methods:**
- create_instance(replace: bool = false, custom_scene: PackedScene = null) -> Node - Call this method to actually load in the node. The created node will be placed as a sibling *above* the InstancePlaceholder in the scene tree. The Node's reference is also returned for convenience. **Note:** `create_instance` is not thread-safe. Use `Object.call_deferred` if calling from a thread.
- get_instance_path() -> String - Gets the path to the PackedScene resource file that is loaded by default when calling `create_instance`. Not thread-safe. Use `Object.call_deferred` if calling from a thread.
- get_stored_values(with_order: bool = false) -> Dictionary - Returns the list of properties that will be applied to the node when `create_instance` is called. If `with_order` is `true`, a key named `.order` (note the leading period) is added to the dictionary. This `.order` key is an Array of String property names specifying the order in which properties will be applied (with index 0 being the first).

