## AnimationNode <- Resource

Base resource for AnimationTree nodes. In general, it's not used directly, but you can create custom ones with custom blending formulas. Inherit this when creating animation nodes mainly for use in AnimationNodeBlendTree, otherwise AnimationRootNode should be used instead. You can access the time information as read-only parameter which is processed and stored in the previous frame for all nodes except AnimationNodeOutput. **Note:** If multiple inputs exist in the AnimationNode, which time information takes precedence depends on the type of AnimationNode.

**Props:**
- filter_enabled: bool

- **filter_enabled**: If `true`, filtering is enabled.

**Methods:**
- _get_caption() -> String - When inheriting from AnimationRootNode, implement this virtual method to override the text caption for this animation node.
- _get_child_by_name(name: StringName) -> AnimationNode - When inheriting from AnimationRootNode, implement this virtual method to return a child animation node by its `name`.
- _get_child_nodes() -> Dictionary - When inheriting from AnimationRootNode, implement this virtual method to return all child animation nodes in order as a `name: node` dictionary.
- _get_parameter_default_value(parameter: StringName) -> Variant - When inheriting from AnimationRootNode, implement this virtual method to return the default value of a `parameter`. Parameters are custom local memory used for your animation nodes, given a resource can be reused in multiple trees.
- _get_parameter_list() -> Array - When inheriting from AnimationRootNode, implement this virtual method to return a list of the properties on this animation node. Parameters are custom local memory used for your animation nodes, given a resource can be reused in multiple trees. Format is similar to `Object.get_property_list`.
- _has_filter() -> bool - When inheriting from AnimationRootNode, implement this virtual method to return whether the blend tree editor should display filter editing on this animation node.
- _is_parameter_read_only(parameter: StringName) -> bool - When inheriting from AnimationRootNode, implement this virtual method to return whether the `parameter` is read-only. Parameters are custom local memory used for your animation nodes, given a resource can be reused in multiple trees.
- _process(time: float, seek: bool, is_external_seeking: bool, test_only: bool) -> float - When inheriting from AnimationRootNode, implement this virtual method to run some code when this animation node is processed. The `time` parameter is a relative delta, unless `seek` is `true`, in which case it is absolute. Here, call the `blend_input`, `blend_node` or `blend_animation` functions. You can also use `get_parameter` and `set_parameter` to modify local memory. This function should return the delta.
- add_input(name: String) -> bool - Adds an input to the animation node. This is only useful for animation nodes created for use in an AnimationNodeBlendTree. If the addition fails, returns `false`.
- blend_animation(animation: StringName, time: float, delta: float, seeked: bool, is_external_seeking: bool, blend: float, looped_flag: int = 0) - Blends an animation by `blend` amount (name must be valid in the linked AnimationPlayer). A `time` and `delta` may be passed, as well as whether `seeked` happened. A `looped_flag` is used by internal processing immediately after the loop.
- blend_input(input_index: int, time: float, seek: bool, is_external_seeking: bool, blend: float, filter: int = 0, sync: bool = true, test_only: bool = false) -> float - Blends an input. This is only useful for animation nodes created for an AnimationNodeBlendTree. The `time` parameter is a relative delta, unless `seek` is `true`, in which case it is absolute. A filter mode may be optionally passed.
- blend_node(name: StringName, node: AnimationNode, time: float, seek: bool, is_external_seeking: bool, blend: float, filter: int = 0, sync: bool = true, test_only: bool = false) -> float - Blend another animation node (in case this animation node contains child animation nodes). This function is only useful if you inherit from AnimationRootNode instead, otherwise editors will not display your animation node for addition.
- find_input(name: String) -> int - Returns the input index which corresponds to `name`. If not found, returns `-1`.
- get_input_count() -> int - Amount of inputs in this animation node, only useful for animation nodes that go into AnimationNodeBlendTree.
- get_input_name(input: int) -> String - Gets the name of an input by index.
- get_parameter(name: StringName) -> Variant - Gets the value of a parameter. Parameters are custom local memory used for your animation nodes, given a resource can be reused in multiple trees.
- get_processing_animation_tree_instance_id() -> int - Returns the object id of the AnimationTree that owns this node. **Note:** This method should only be called from within the `AnimationNodeExtension._process_animation_node` method, and will return an invalid id otherwise.
- is_path_filtered(path: NodePath) -> bool - Returns `true` if the given path is filtered.
- is_process_testing() -> bool - Returns `true` if this animation node is being processed in test-only mode.
- remove_input(index: int) - Removes an input, call this only when inactive.
- set_filter_path(path: NodePath, enable: bool) - Adds or removes a path for the filter.
- set_input_name(input: int, name: String) -> bool - Sets the name of the input at the given `input` index. If the setting fails, returns `false`.
- set_parameter(name: StringName, value: Variant) - Sets a custom parameter. These are used as local memory, because resources can be reused across the tree or scenes.

**Signals:**
- animation_node_removed(object_id: int, name: String) - Emitted by nodes that inherit from this class and that have an internal tree when one of their animation nodes removes. The animation nodes that emit this signal are AnimationNodeBlendSpace1D, AnimationNodeBlendSpace2D, AnimationNodeStateMachine, and AnimationNodeBlendTree.
- animation_node_renamed(object_id: int, old_name: String, new_name: String) - Emitted by nodes that inherit from this class and that have an internal tree when one of their animation node names changes. The animation nodes that emit this signal are AnimationNodeBlendSpace1D, AnimationNodeBlendSpace2D, AnimationNodeStateMachine, and AnimationNodeBlendTree.
- node_updated(object_id: int) - Emitted by AnimationNodeAnimation when its `AnimationNodeAnimation.animation` resource is changed, or by AnimationNodeBlendTree when its connections change.
- tree_changed - Emitted by nodes that inherit from this class and that have an internal tree when one of their animation nodes changes. The animation nodes that emit this signal are AnimationNodeBlendSpace1D, AnimationNodeBlendSpace2D, AnimationNodeStateMachine, AnimationNodeBlendTree and AnimationNodeTransition.

**Enums:**
**FilterAction:** FILTER_IGNORE=0, FILTER_PASS=1, FILTER_STOP=2, FILTER_BLEND=3
  - FILTER_IGNORE: Do not use filtering.
  - FILTER_PASS: Paths matching the filter will be allowed to pass.
  - FILTER_STOP: Paths matching the filter will be discarded.
  - FILTER_BLEND: Paths matching the filter will be blended (by the blend value).

