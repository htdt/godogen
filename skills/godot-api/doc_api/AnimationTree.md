## AnimationTree <- AnimationMixer

A node used for advanced animation transitions in an AnimationPlayer. **Note:** When linked with an AnimationPlayer, several properties and methods of the corresponding AnimationPlayer will not function as expected. Playback and transitions should be handled using only the AnimationTree and its constituent AnimationNode(s). The AnimationPlayer node should be used solely for adding, deleting, and editing animations.

**Props:**
- advance_expression_base_node: NodePath = NodePath(".")
- anim_player: NodePath = NodePath("")
- callback_mode_discrete: int (AnimationMixer.AnimationCallbackModeDiscrete) = 2
- deterministic: bool = true
- tree_root: AnimationRootNode

- **advance_expression_base_node**: The path to the Node used to evaluate the AnimationNode Expression if one is not explicitly specified internally.
- **anim_player**: The path to the AnimationPlayer used for animating.
- **tree_root**: The root animation node of this AnimationTree. See AnimationRootNode.

**Methods:**
- get_process_callback() -> int - Returns the process notification in which to update animations.
- set_process_callback(mode: int) - Sets the process notification in which to update animations.

**Signals:**
- animation_player_changed - Emitted when the `anim_player` is changed.

**Enums:**
**AnimationProcessCallback:** ANIMATION_PROCESS_PHYSICS=0, ANIMATION_PROCESS_IDLE=1, ANIMATION_PROCESS_MANUAL=2

