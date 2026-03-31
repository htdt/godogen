## AnimationNodeBlendTree <- AnimationRootNode

This animation node may contain a sub-tree of any other type animation nodes, such as AnimationNodeTransition, AnimationNodeBlend2, AnimationNodeBlend3, AnimationNodeOneShot, etc. This is one of the most commonly used animation node roots. An AnimationNodeOutput node named `output` is created by default.

**Props:**
- graph_offset: Vector2 = Vector2(0, 0)

- **graph_offset**: The global offset of all sub animation nodes.

**Methods:**
- add_node(name: StringName, node: AnimationNode, position: Vector2 = Vector2(0, 0)) - Adds an AnimationNode at the given `position`. The `name` is used to identify the created sub animation node later.
- connect_node(input_node: StringName, input_index: int, output_node: StringName) - Connects the output of an AnimationNode as input for another AnimationNode, at the input port specified by `input_index`.
- disconnect_node(input_node: StringName, input_index: int) - Disconnects the animation node connected to the specified input.
- get_node(name: StringName) -> AnimationNode - Returns the sub animation node with the specified `name`.
- get_node_list() -> StringName[] - Returns a list containing the names of all sub animation nodes in this blend tree.
- get_node_position(name: StringName) -> Vector2 - Returns the position of the sub animation node with the specified `name`.
- has_node(name: StringName) -> bool - Returns `true` if a sub animation node with specified `name` exists.
- remove_node(name: StringName) - Removes a sub animation node.
- rename_node(name: StringName, new_name: StringName) - Changes the name of a sub animation node.
- set_node_position(name: StringName, position: Vector2) - Modifies the position of a sub animation node.

**Signals:**
- node_changed(node_name: StringName) - Emitted when the input port information is changed.

**Enums:**
**Constants:** CONNECTION_OK=0, CONNECTION_ERROR_NO_INPUT=1, CONNECTION_ERROR_NO_INPUT_INDEX=2, CONNECTION_ERROR_NO_OUTPUT=3, CONNECTION_ERROR_SAME_NODE=4, CONNECTION_ERROR_CONNECTION_EXISTS=5
  - CONNECTION_OK: The connection was successful.
  - CONNECTION_ERROR_NO_INPUT: The input node is `null`.
  - CONNECTION_ERROR_NO_INPUT_INDEX: The specified input port is out of range.
  - CONNECTION_ERROR_NO_OUTPUT: The output node is `null`.
  - CONNECTION_ERROR_SAME_NODE: Input and output nodes are the same.
  - CONNECTION_ERROR_CONNECTION_EXISTS: The specified connection already exists.

