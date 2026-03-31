## PackedScene <- Resource

A simplified interface to a scene file. Provides access to operations and checks that can be performed on the scene resource itself. Can be used to save a node to a file. When saving, the node as well as all the nodes it owns get saved (see `Node.owner` property). **Note:** The node doesn't need to own itself. **Example:** Load a saved scene: **Example:** Save a node with different owners. The following example creates 3 objects: Node2D (`node`), RigidBody2D (`body`) and CollisionObject2D (`collision`). `collision` is a child of `body` which is a child of `node`. Only `body` is owned by `node` and `pack` will therefore only save those two nodes, but not `collision`.

**Methods:**
- can_instantiate() -> bool - Returns `true` if the scene file has nodes.
- get_state() -> SceneState - Returns the SceneState representing the scene file contents.
- instantiate(edit_state: int = 0) -> Node - Instantiates the scene's node hierarchy. Triggers child scene instantiation(s). Triggers a `Node.NOTIFICATION_SCENE_INSTANTIATED` notification on the root node.
- pack(path: Node) -> int - Packs the `path` node, and all owned sub-nodes, into this PackedScene. Any existing data will be cleared. See `Node.owner`.

**Enums:**
**GenEditState:** GEN_EDIT_STATE_DISABLED=0, GEN_EDIT_STATE_INSTANCE=1, GEN_EDIT_STATE_MAIN=2, GEN_EDIT_STATE_MAIN_INHERITED=3
  - GEN_EDIT_STATE_DISABLED: If passed to `instantiate`, blocks edits to the scene state.
  - GEN_EDIT_STATE_INSTANCE: If passed to `instantiate`, provides local scene resources to the local scene. **Note:** Only available in editor builds.
  - GEN_EDIT_STATE_MAIN: If passed to `instantiate`, provides local scene resources to the local scene. Only the main scene should receive the main edit state. **Note:** Only available in editor builds.
  - GEN_EDIT_STATE_MAIN_INHERITED: It's similar to `GEN_EDIT_STATE_MAIN`, but for the case where the scene is being instantiated to be the base of another one. **Note:** Only available in editor builds.

