## AnimationNodeStateMachine <- AnimationRootNode

Contains multiple AnimationRootNodes representing animation states, connected in a graph. State transitions can be configured to happen automatically or via code, using a shortest-path algorithm. Retrieve the AnimationNodeStateMachinePlayback object from the AnimationTree node to control it programmatically.

**Props:**
- allow_transition_to_self: bool = false
- reset_ends: bool = false
- state_machine_type: int (AnimationNodeStateMachine.StateMachineType) = 0

- **allow_transition_to_self**: If `true`, allows teleport to the self state with `AnimationNodeStateMachinePlayback.travel`. When the reset option is enabled in `AnimationNodeStateMachinePlayback.travel`, the animation is restarted. If `false`, nothing happens on the teleportation to the self state.
- **reset_ends**: If `true`, treat the cross-fade to the start and end nodes as a blend with the RESET animation. In most cases, when additional cross-fades are performed in the parent AnimationNode of the state machine, setting this property to `false` and matching the cross-fade time of the parent AnimationNode and the state machine's start node and end node gives good results.
- **state_machine_type**: This property can define the process of transitions for different use cases. See also `AnimationNodeStateMachine.StateMachineType`.

**Methods:**
- add_node(name: StringName, node: AnimationNode, position: Vector2 = Vector2(0, 0)) - Adds a new animation node to the graph. The `position` is used for display in the editor.
- add_transition(from: StringName, to: StringName, transition: AnimationNodeStateMachineTransition) - Adds a transition between the given animation nodes.
- get_graph_offset() -> Vector2 - Returns the draw offset of the graph. Used for display in the editor.
- get_node(name: StringName) -> AnimationNode - Returns the animation node with the given name.
- get_node_list() -> StringName[] - Returns a list containing the names of all animation nodes in this state machine.
- get_node_name(node: AnimationNode) -> StringName - Returns the given animation node's name.
- get_node_position(name: StringName) -> Vector2 - Returns the given animation node's coordinates. Used for display in the editor.
- get_transition(idx: int) -> AnimationNodeStateMachineTransition - Returns the given transition.
- get_transition_count() -> int - Returns the number of connections in the graph.
- get_transition_from(idx: int) -> StringName - Returns the given transition's start node.
- get_transition_to(idx: int) -> StringName - Returns the given transition's end node.
- has_node(name: StringName) -> bool - Returns `true` if the graph contains the given animation node.
- has_transition(from: StringName, to: StringName) -> bool - Returns `true` if there is a transition between the given animation nodes.
- remove_node(name: StringName) - Deletes the given animation node from the graph.
- remove_transition(from: StringName, to: StringName) - Deletes the transition between the two specified animation nodes.
- remove_transition_by_index(idx: int) - Deletes the given transition by index.
- rename_node(name: StringName, new_name: StringName) - Renames the given animation node.
- replace_node(name: StringName, node: AnimationNode) - Replaces the given animation node with a new animation node.
- set_graph_offset(offset: Vector2) - Sets the draw offset of the graph. Used for display in the editor.
- set_node_position(name: StringName, position: Vector2) - Sets the animation node's coordinates. Used for display in the editor.

**Enums:**
**StateMachineType:** STATE_MACHINE_TYPE_ROOT=0, STATE_MACHINE_TYPE_NESTED=1, STATE_MACHINE_TYPE_GROUPED=2
  - STATE_MACHINE_TYPE_ROOT: Seeking to the beginning is treated as playing from the start state. Transition to the end state is treated as exiting the state machine.
  - STATE_MACHINE_TYPE_NESTED: Seeking to the beginning is treated as seeking to the beginning of the animation in the current state. Transition to the end state, or the absence of transitions in each state, is treated as exiting the state machine.
  - STATE_MACHINE_TYPE_GROUPED: This is a grouped state machine that can be controlled from a parent state machine. It does not work independently. There must be a state machine with `state_machine_type` of `STATE_MACHINE_TYPE_ROOT` or `STATE_MACHINE_TYPE_NESTED` in the parent or ancestor.

