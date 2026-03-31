## Curve3D <- Resource

This class describes a Bézier curve in 3D space. It is mainly used to give a shape to a Path3D, but can be manually sampled for other purposes. It keeps a cache of precalculated points along the curve, to speed up further calculations.

**Props:**
- bake_interval: float = 0.2
- closed: bool = false
- point_count: int = 0
- point_{index}/in: Vector3 = Vector3(0, 0, 0)
- point_{index}/out: Vector3 = Vector3(0, 0, 0)
- point_{index}/position: Vector3 = Vector3(0, 0, 0)
- point_{index}/tilt: float = 0.0
- up_vector_enabled: bool = true

- **bake_interval**: The distance in meters between two adjacent cached points. Changing it forces the cache to be recomputed the next time the `get_baked_points` or `get_baked_length` function is called. The smaller the distance, the more points in the cache and the more memory it will consume, so use with care.
- **closed**: If `true`, and the curve has more than 2 control points, the last point and the first one will be connected in a loop.
- **point_count**: The number of points describing the curve.
- **point_{index}/in**: The position of the control point leading to the vertex at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.
- **point_{index}/out**: The position of the control point leading out of the vertex at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.
- **point_{index}/position**: The position of for the vertex at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.
- **point_{index}/tilt**: The tilt angle in radians for the point at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.
- **up_vector_enabled**: If `true`, the curve will bake up vectors used for orientation. This is used when `PathFollow3D.rotation_mode` is set to `PathFollow3D.ROTATION_ORIENTED`. Changing it forces the cache to be recomputed.

**Methods:**
- add_point(position: Vector3, in: Vector3 = Vector3(0, 0, 0), out: Vector3 = Vector3(0, 0, 0), index: int = -1) - Adds a point with the specified `position` relative to the curve's own position, with control points `in` and `out`. Appends the new point at the end of the point list. If `index` is given, the new point is inserted before the existing point identified by index `index`. Every existing point starting from `index` is shifted further down the list of points. The index must be greater than or equal to `0` and must not exceed the number of existing points in the line. See `point_count`.
- clear_points() - Removes all points from the curve.
- get_baked_length() -> float - Returns the total length of the curve, based on the cached points. Given enough density (see `bake_interval`), it should be approximate enough.
- get_baked_points() -> PackedVector3Array - Returns the cache of points as a PackedVector3Array.
- get_baked_tilts() -> PackedFloat32Array - Returns the cache of tilts as a PackedFloat32Array.
- get_baked_up_vectors() -> PackedVector3Array - Returns the cache of up vectors as a PackedVector3Array. If `up_vector_enabled` is `false`, the cache will be empty.
- get_closest_offset(to_point: Vector3) -> float - Returns the closest offset to `to_point`. This offset is meant to be used in `sample_baked` or `sample_baked_up_vector`. `to_point` must be in this curve's local space.
- get_closest_point(to_point: Vector3) -> Vector3 - Returns the closest point on baked segments (in curve's local space) to `to_point`. `to_point` must be in this curve's local space.
- get_point_in(idx: int) -> Vector3 - Returns the position of the control point leading to the vertex `idx`. The returned position is relative to the vertex `idx`. If the index is out of bounds, the function sends an error to the console, and returns `(0, 0, 0)`.
- get_point_out(idx: int) -> Vector3 - Returns the position of the control point leading out of the vertex `idx`. The returned position is relative to the vertex `idx`. If the index is out of bounds, the function sends an error to the console, and returns `(0, 0, 0)`.
- get_point_position(idx: int) -> Vector3 - Returns the position of the vertex `idx`. If the index is out of bounds, the function sends an error to the console, and returns `(0, 0, 0)`.
- get_point_tilt(idx: int) -> float - Returns the tilt angle in radians for the point `idx`. If the index is out of bounds, the function sends an error to the console, and returns `0`.
- remove_point(idx: int) - Deletes the point `idx` from the curve. Sends an error to the console if `idx` is out of bounds.
- sample(idx: int, t: float) -> Vector3 - Returns the position between the vertex `idx` and the vertex `idx + 1`, where `t` controls if the point is the first vertex (`t = 0.0`), the last vertex (`t = 1.0`), or in between. Values of `t` outside the range (`0.0 >= t <=1`) give strange, but predictable results. If `idx` is out of bounds it is truncated to the first or last vertex, and `t` is ignored. If the curve has no points, the function sends an error to the console, and returns `(0, 0, 0)`.
- sample_baked(offset: float = 0.0, cubic: bool = false) -> Vector3 - Returns a point within the curve at position `offset`, where `offset` is measured as a distance in 3D units along the curve. To do that, it finds the two cached points where the `offset` lies between, then interpolates the values. This interpolation is cubic if `cubic` is set to `true`, or linear if set to `false`. Cubic interpolation tends to follow the curves better, but linear is faster (and often, precise enough).
- sample_baked_up_vector(offset: float, apply_tilt: bool = false) -> Vector3 - Returns an up vector within the curve at position `offset`, where `offset` is measured as a distance in 3D units along the curve. To do that, it finds the two cached up vectors where the `offset` lies between, then interpolates the values. If `apply_tilt` is `true`, an interpolated tilt is applied to the interpolated up vector. If the curve has no up vectors, the function sends an error to the console, and returns `(0, 1, 0)`.
- sample_baked_with_rotation(offset: float = 0.0, cubic: bool = false, apply_tilt: bool = false) -> Transform3D - Returns a Transform3D with `origin` as point position, `basis.x` as sideway vector, `basis.y` as up vector, `basis.z` as forward vector. When the curve length is 0, there is no reasonable way to calculate the rotation, all vectors aligned with global space axes. See also `sample_baked`.
- samplef(fofs: float) -> Vector3 - Returns the position at the vertex `fofs`. It calls `sample` using the integer part of `fofs` as `idx`, and its fractional part as `t`.
- set_point_in(idx: int, position: Vector3) - Sets the position of the control point leading to the vertex `idx`. If the index is out of bounds, the function sends an error to the console. The position is relative to the vertex.
- set_point_out(idx: int, position: Vector3) - Sets the position of the control point leading out of the vertex `idx`. If the index is out of bounds, the function sends an error to the console. The position is relative to the vertex.
- set_point_position(idx: int, position: Vector3) - Sets the position for the vertex `idx`. If the index is out of bounds, the function sends an error to the console.
- set_point_tilt(idx: int, tilt: float) - Sets the tilt angle in radians for the point `idx`. If the index is out of bounds, the function sends an error to the console. The tilt controls the rotation along the look-at axis an object traveling the path would have. In the case of a curve controlling a PathFollow3D, this tilt is an offset over the natural tilt the PathFollow3D calculates.
- tessellate(max_stages: int = 5, tolerance_degrees: float = 4) -> PackedVector3Array - Returns a list of points along the curve, with a curvature controlled point density. That is, the curvier parts will have more points than the straighter parts. This approximation makes straight segments between each point, then subdivides those segments until the resulting shape is similar enough. `max_stages` controls how many subdivisions a curve segment may face before it is considered approximate enough. Each subdivision splits the segment in half, so the default 5 stages may mean up to 32 subdivisions per curve segment. Increase with care! `tolerance_degrees` controls how many degrees the midpoint of a segment may deviate from the real curve, before the segment has to be subdivided.
- tessellate_even_length(max_stages: int = 5, tolerance_length: float = 0.2) -> PackedVector3Array - Returns a list of points along the curve, with almost uniform density. `max_stages` controls how many subdivisions a curve segment may face before it is considered approximate enough. Each subdivision splits the segment in half, so the default 5 stages may mean up to 32 subdivisions per curve segment. Increase with care! `tolerance_length` controls the maximal distance between two neighboring points, before the segment has to be subdivided.

