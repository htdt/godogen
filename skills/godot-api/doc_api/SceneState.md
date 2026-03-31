## SceneState <- RefCounted

Maintains a list of resources, nodes, exported and overridden properties, and built-in scripts associated with a scene. They cannot be modified from a SceneState, only accessed. Useful for peeking into what a PackedScene contains without instantiating it. This class cannot be instantiated directly, it is retrieved for a given scene as the result of `PackedScene.get_state`.

**Methods:**
- get_base_scene_state() -> SceneState - Returns the SceneState of the scene that this scene inherits from, or `null` if it doesn't inherit from any scene.
- get_connection_binds(idx: int) -> Array - Returns the list of bound parameters for the signal at `idx`.
- get_connection_count() -> int - Returns the number of signal connections in the scene. The `idx` argument used to query connection metadata in other `get_connection_*` methods in the interval `[0, get_connection_count() - 1]`.
- get_connection_flags(idx: int) -> int - Returns the connection flags for the signal at `idx`. See `Object.ConnectFlags` constants.
- get_connection_method(idx: int) -> StringName - Returns the method connected to the signal at `idx`.
- get_connection_signal(idx: int) -> StringName - Returns the name of the signal at `idx`.
- get_connection_source(idx: int) -> NodePath - Returns the path to the node that owns the signal at `idx`, relative to the root node.
- get_connection_target(idx: int) -> NodePath - Returns the path to the node that owns the method connected to the signal at `idx`, relative to the root node.
- get_connection_unbinds(idx: int) -> int - Returns the number of unbound parameters for the signal at `idx`.
- get_node_count() -> int - Returns the number of nodes in the scene. The `idx` argument used to query node data in other `get_node_*` methods in the interval `[0, get_node_count() - 1]`.
- get_node_groups(idx: int) -> PackedStringArray - Returns the list of group names associated with the node at `idx`.
- get_node_index(idx: int) -> int - Returns the node's index, which is its position relative to its siblings. This is only relevant and saved in scenes for cases where new nodes are added to an instantiated or inherited scene among siblings from the base scene. Despite the name, this index is not related to the `idx` argument used here and in other methods.
- get_node_instance(idx: int) -> PackedScene - Returns a PackedScene for the node at `idx` (i.e. the whole branch starting at this node, with its child nodes and resources), or `null` if the node is not an instance.
- get_node_instance_placeholder(idx: int) -> String - Returns the path to the represented scene file if the node at `idx` is an InstancePlaceholder.
- get_node_name(idx: int) -> StringName - Returns the name of the node at `idx`.
- get_node_owner_path(idx: int) -> NodePath - Returns the path to the owner of the node at `idx`, relative to the root node.
- get_node_path(idx: int, for_parent: bool = false) -> NodePath - Returns the path to the node at `idx`. If `for_parent` is `true`, returns the path of the `idx` node's parent instead.
- get_node_property_count(idx: int) -> int - Returns the number of exported or overridden properties for the node at `idx`. The `prop_idx` argument used to query node property data in other `get_node_property_*` methods in the interval `[0, get_node_property_count() - 1]`.
- get_node_property_name(idx: int, prop_idx: int) -> StringName - Returns the name of the property at `prop_idx` for the node at `idx`.
- get_node_property_value(idx: int, prop_idx: int) -> Variant - Returns the value of the property at `prop_idx` for the node at `idx`.
- get_node_type(idx: int) -> StringName - Returns the type of the node at `idx`.
- get_path() -> String - Returns the resource path to the represented PackedScene.
- is_node_instance_placeholder(idx: int) -> bool - Returns `true` if the node at `idx` is an InstancePlaceholder.

**Enums:**
**GenEditState:** GEN_EDIT_STATE_DISABLED=0, GEN_EDIT_STATE_INSTANCE=1, GEN_EDIT_STATE_MAIN=2, GEN_EDIT_STATE_MAIN_INHERITED=3
  - GEN_EDIT_STATE_DISABLED: If passed to `PackedScene.instantiate`, blocks edits to the scene state.
  - GEN_EDIT_STATE_INSTANCE: If passed to `PackedScene.instantiate`, provides inherited scene resources to the local scene. **Note:** Only available in editor builds.
  - GEN_EDIT_STATE_MAIN: If passed to `PackedScene.instantiate`, provides local scene resources to the local scene. Only the main scene should receive the main edit state. **Note:** Only available in editor builds.
  - GEN_EDIT_STATE_MAIN_INHERITED: If passed to `PackedScene.instantiate`, it's similar to `GEN_EDIT_STATE_MAIN`, but for the case where the scene is being instantiated to be the base of another one. **Note:** Only available in editor builds.

