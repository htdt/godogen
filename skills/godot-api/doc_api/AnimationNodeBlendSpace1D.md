## AnimationNodeBlendSpace1D <- AnimationRootNode

A resource used by AnimationNodeBlendTree. AnimationNodeBlendSpace1D represents a virtual axis on which any type of AnimationRootNodes can be added using `add_blend_point`. Outputs the linear blend of the two AnimationRootNodes adjacent to the current value. You can set the extents of the axis with `min_space` and `max_space`.

**Props:**
- blend_mode: int (AnimationNodeBlendSpace1D.BlendMode) = 0
- max_space: float = 1.0
- min_space: float = -1.0
- snap: float = 0.1
- sync: bool = false
- value_label: String = "value"

- **blend_mode**: Controls the interpolation between animations.
- **max_space**: The blend space's axis's upper limit for the points' position. See `add_blend_point`.
- **min_space**: The blend space's axis's lower limit for the points' position. See `add_blend_point`.
- **snap**: Position increment to snap to when moving a point on the axis.
- **sync**: If `false`, the blended animations' frame are stopped when the blend value is `0`. If `true`, forcing the blended animations to advance frame.
- **value_label**: Label of the virtual axis of the blend space.

**Methods:**
- add_blend_point(node: AnimationRootNode, pos: float, at_index: int = -1, name: StringName = &"") - Adds a new point with `name` that represents a `node` on the virtual axis at a given position set by `pos`. You can insert it at a specific index using the `at_index` argument. If you use the default value for `at_index`, the point is inserted at the end of the blend points array. **Note:** If no name is provided, safe index is used as reference. In the future, empty names will be deprecated, so explicitly passing a name is recommended.
- find_blend_point_by_name(name: StringName) -> int - Returns the index of the blend point with the given `name`. Returns `-1` if no blend point with that name is found.
- get_blend_point_count() -> int - Returns the number of points on the blend axis.
- get_blend_point_name(point: int) -> StringName - Returns the name of the blend point at index `point`.
- get_blend_point_node(point: int) -> AnimationRootNode - Returns the AnimationNode referenced by the point at index `point`.
- get_blend_point_position(point: int) -> float - Returns the position of the point at index `point`.
- remove_blend_point(point: int) - Removes the point at index `point` from the blend axis.
- reorder_blend_point(from_index: int, to_index: int) - Swaps the blend points at indices `from_index` and `to_index`, exchanging their positions and properties.
- set_blend_point_name(point: int, name: StringName) - Sets the name of the blend point at index `point`. If the name conflicts with an existing point, a unique name will be generated automatically.
- set_blend_point_node(point: int, node: AnimationRootNode) - Changes the AnimationNode referenced by the point at index `point`.
- set_blend_point_position(point: int, pos: float) - Updates the position of the point at index `point` on the blend axis.

**Enums:**
**BlendMode:** BLEND_MODE_INTERPOLATED=0, BLEND_MODE_DISCRETE=1, BLEND_MODE_DISCRETE_CARRY=2
  - BLEND_MODE_INTERPOLATED: The interpolation between animations is linear.
  - BLEND_MODE_DISCRETE: The blend space plays the animation of the animation node which blending position is closest to. Useful for frame-by-frame 2D animations.
  - BLEND_MODE_DISCRETE_CARRY: Similar to `BLEND_MODE_DISCRETE`, but starts the new animation at the last animation's playback position.

