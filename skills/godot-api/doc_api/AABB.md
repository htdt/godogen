## AABB

The AABB built-in Variant type represents an axis-aligned bounding box in a 3D space. It is defined by its `position` and `size`, which are Vector3. It is frequently used for fast overlap tests (see `intersects`). Although AABB itself is axis-aligned, it can be combined with Transform3D to represent a rotated or skewed bounding box. It uses floating-point coordinates. The 2D counterpart to AABB is Rect2. There is no version of AABB that uses integer coordinates. **Note:** Negative values for `size` are not supported. With negative size, most AABB methods do not work correctly. Use `abs` to get an equivalent AABB with a non-negative size. **Note:** In a boolean context, an AABB evaluates to `false` if both `position` and `size` are zero (equal to `Vector3.ZERO`). Otherwise, it always evaluates to `true`.

**Props:**
- end: Vector3 = Vector3(0, 0, 0)
- position: Vector3 = Vector3(0, 0, 0)
- size: Vector3 = Vector3(0, 0, 0)

- **end**: The ending point. This is usually the corner on the top-right and back of the bounding box, and is equivalent to `position + size`. Setting this point affects the `size`.
- **position**: The origin point. This is usually the corner on the bottom-left and forward of the bounding box.
- **size**: The bounding box's width, height, and depth starting from `position`. Setting this value also affects the `end` point. **Note:** It's recommended setting the width, height, and depth to non-negative values. This is because most methods in Godot assume that the `position` is the bottom-left-forward corner, and the `end` is the top-right-back corner. To get an equivalent bounding box with non-negative size, use `abs`.

**Methods:**
- abs() -> AABB - Returns an AABB equivalent to this bounding box, with its width, height, and depth modified to be non-negative values. **Note:** It's recommended to use this method when `size` is negative, as most other methods in Godot assume that the `size`'s components are greater than `0`.
- encloses(with: AABB) -> bool - Returns `true` if this bounding box *completely* encloses the `with` box. The edges of both boxes are included.
- expand(to_point: Vector3) -> AABB - Returns a copy of this bounding box expanded to align the edges with the given `to_point`, if necessary.
- get_center() -> Vector3 - Returns the center point of the bounding box. This is the same as `position + (size / 2.0)`.
- get_endpoint(idx: int) -> Vector3 - Returns the position of one of the 8 vertices that compose this bounding box. With an `idx` of `0` this is the same as `position`, and an `idx` of `7` is the same as `end`.
- get_longest_axis() -> Vector3 - Returns the longest normalized axis of this bounding box's `size`, as a Vector3 (`Vector3.RIGHT`, `Vector3.UP`, or `Vector3.BACK`). See also `get_longest_axis_index` and `get_longest_axis_size`.
- get_longest_axis_index() -> int - Returns the index to the longest axis of this bounding box's `size` (see `Vector3.AXIS_X`, `Vector3.AXIS_Y`, and `Vector3.AXIS_Z`). For an example, see `get_longest_axis`.
- get_longest_axis_size() -> float - Returns the longest dimension of this bounding box's `size`. For an example, see `get_longest_axis`.
- get_shortest_axis() -> Vector3 - Returns the shortest normalized axis of this bounding box's `size`, as a Vector3 (`Vector3.RIGHT`, `Vector3.UP`, or `Vector3.BACK`). See also `get_shortest_axis_index` and `get_shortest_axis_size`.
- get_shortest_axis_index() -> int - Returns the index to the shortest axis of this bounding box's `size` (see `Vector3.AXIS_X`, `Vector3.AXIS_Y`, and `Vector3.AXIS_Z`). For an example, see `get_shortest_axis`.
- get_shortest_axis_size() -> float - Returns the shortest dimension of this bounding box's `size`. For an example, see `get_shortest_axis`.
- get_support(direction: Vector3) -> Vector3 - Returns the vertex's position of this bounding box that's the farthest in the given direction. This point is commonly known as the support point in collision detection algorithms.
- get_volume() -> float - Returns the bounding box's volume. This is equivalent to `size.x * size.y * size.z`. See also `has_volume`.
- grow(by: float) -> AABB - Returns a copy of this bounding box extended on all sides by the given amount `by`. A negative amount shrinks the box instead.
- has_point(point: Vector3) -> bool - Returns `true` if the bounding box contains the given `point`. By convention, points exactly on the right, top, and front sides are **not** included. **Note:** This method is not reliable for AABB with a *negative* `size`. Use `abs` first to get a valid bounding box.
- has_surface() -> bool - Returns `true` if this bounding box has a surface or a length, that is, at least one component of `size` is greater than `0`. Otherwise, returns `false`.
- has_volume() -> bool - Returns `true` if this bounding box's width, height, and depth are all positive. See also `get_volume`.
- intersection(with: AABB) -> AABB - Returns the intersection between this bounding box and `with`. If the boxes do not intersect, returns an empty AABB. If the boxes intersect at the edge, returns a flat AABB with no volume (see `has_surface` and `has_volume`). **Note:** If you only need to know whether two bounding boxes are intersecting, use `intersects`, instead.
- intersects(with: AABB) -> bool - Returns `true` if this bounding box overlaps with the box `with`. The edges of both boxes are *always* excluded.
- intersects_plane(plane: Plane) -> bool - Returns `true` if this bounding box is on both sides of the given `plane`.
- intersects_ray(from: Vector3, dir: Vector3) -> Variant - Returns the first point where this bounding box and the given ray intersect, as a Vector3. If no intersection occurs, returns `null`. The ray begin at `from`, faces `dir` and extends towards infinity.
- intersects_segment(from: Vector3, to: Vector3) -> Variant - Returns the first point where this bounding box and the given segment intersect, as a Vector3. If no intersection occurs, returns `null`. The segment begins at `from` and ends at `to`.
- is_equal_approx(aabb: AABB) -> bool - Returns `true` if this bounding box and `aabb` are approximately equal, by calling `Vector3.is_equal_approx` on the `position` and the `size`.
- is_finite() -> bool - Returns `true` if this bounding box's values are finite, by calling `Vector3.is_finite` on the `position` and the `size`.
- merge(with: AABB) -> AABB - Returns an AABB that encloses both this bounding box and `with` around the edges. See also `encloses`.

