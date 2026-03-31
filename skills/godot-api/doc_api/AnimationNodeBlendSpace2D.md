## AnimationNodeBlendSpace2D <- AnimationRootNode

A resource used by AnimationNodeBlendTree. AnimationNodeBlendSpace2D represents a virtual 2D space on which AnimationRootNodes are placed. Outputs the linear blend of the three adjacent animations using a Vector2 weight. Adjacent in this context means the three AnimationRootNodes making up the triangle that contains the current value. You can add vertices to the blend space with `add_blend_point` and automatically triangulate it by setting `auto_triangles` to `true`. Otherwise, use `add_triangle` and `remove_triangle` to triangulate the blend space by hand.

**Props:**
- auto_triangles: bool = true
- blend_mode: int (AnimationNodeBlendSpace2D.BlendMode) = 0
- max_space: Vector2 = Vector2(1, 1)
- min_space: Vector2 = Vector2(-1, -1)
- snap: Vector2 = Vector2(0.1, 0.1)
- sync: bool = false
- x_label: String = "x"
- y_label: String = "y"

- **auto_triangles**: If `true`, the blend space is triangulated automatically. The mesh updates every time you add or remove points with `add_blend_point` and `remove_blend_point`.
- **blend_mode**: Controls the interpolation between animations.
- **max_space**: The blend space's X and Y axes' upper limit for the points' position. See `add_blend_point`.
- **min_space**: The blend space's X and Y axes' lower limit for the points' position. See `add_blend_point`.
- **snap**: Position increment to snap to when moving a point.
- **sync**: If `false`, the blended animations' frame are stopped when the blend value is `0`. If `true`, forcing the blended animations to advance frame.
- **x_label**: Name of the blend space's X axis.
- **y_label**: Name of the blend space's Y axis.

**Methods:**
- add_blend_point(node: AnimationRootNode, pos: Vector2, at_index: int = -1, name: StringName = &"") - Adds a new point with `name` that represents a `node` at the position set by `pos`. You can insert it at a specific index using the `at_index` argument. If you use the default value for `at_index`, the point is inserted at the end of the blend points array. **Note:** If no name is provided, safe index is used as reference. In the future, empty names will be deprecated, so explicitly passing a name is recommended.
- add_triangle(x: int, y: int, z: int, at_index: int = -1) - Creates a new triangle using three points `x`, `y`, and `z`. Triangles can overlap. You can insert the triangle at a specific index using the `at_index` argument. If you use the default value for `at_index`, the point is inserted at the end of the blend points array.
- find_blend_point_by_name(name: StringName) -> int - Returns the index of the blend point with the given `name`. Returns `-1` if no blend point with that name is found.
- get_blend_point_count() -> int - Returns the number of points in the blend space.
- get_blend_point_name(point: int) -> StringName - Returns the name of the blend point at index `point`.
- get_blend_point_node(point: int) -> AnimationRootNode - Returns the AnimationRootNode referenced by the point at index `point`.
- get_blend_point_position(point: int) -> Vector2 - Returns the position of the point at index `point`.
- get_triangle_count() -> int - Returns the number of triangles in the blend space.
- get_triangle_point(triangle: int, point: int) -> int - Returns the position of the point at index `point` in the triangle of index `triangle`.
- remove_blend_point(point: int) - Removes the point at index `point` from the blend space.
- remove_triangle(triangle: int) - Removes the triangle at index `triangle` from the blend space.
- reorder_blend_point(from_index: int, to_index: int) - Swaps the blend points at indices `from_index` and `to_index`, exchanging their positions and properties.
- set_blend_point_name(point: int, name: StringName) - Sets the name of the blend point at index `point`. If the name conflicts with an existing point, a unique name will be generated automatically.
- set_blend_point_node(point: int, node: AnimationRootNode) - Changes the AnimationNode referenced by the point at index `point`.
- set_blend_point_position(point: int, pos: Vector2) - Updates the position of the point at index `point` in the blend space.

**Signals:**
- triangles_updated - Emitted every time the blend space's triangles are created, removed, or when one of their vertices changes position.

**Enums:**
**BlendMode:** BLEND_MODE_INTERPOLATED=0, BLEND_MODE_DISCRETE=1, BLEND_MODE_DISCRETE_CARRY=2
  - BLEND_MODE_INTERPOLATED: The interpolation between animations is linear.
  - BLEND_MODE_DISCRETE: The blend space plays the animation of the animation node which blending position is closest to. Useful for frame-by-frame 2D animations.
  - BLEND_MODE_DISCRETE_CARRY: Similar to `BLEND_MODE_DISCRETE`, but starts the new animation at the last animation's playback position.

