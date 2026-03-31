## Vector3

A 3-element structure that can be used to represent 3D coordinates or any other triplet of numeric values. It uses floating-point coordinates. By default, these floating-point values use 32-bit precision, unlike [float] which is always 64-bit. If double precision is needed, compile the engine with the option `precision=double`. See Vector3i for its integer counterpart. **Note:** In a boolean context, a Vector3 will evaluate to `false` if it's equal to `Vector3(0, 0, 0)`. Otherwise, a Vector3 will always evaluate to `true`.

**Props:**
- x: float = 0.0
- y: float = 0.0
- z: float = 0.0

- **x**: The vector's X component. Also accessible by using the index position `[0]`.
- **y**: The vector's Y component. Also accessible by using the index position `[1]`.
- **z**: The vector's Z component. Also accessible by using the index position `[2]`.

**Methods:**
- abs() -> Vector3 - Returns a new vector with all components in absolute values (i.e. positive).
- angle_to(to: Vector3) -> float - Returns the unsigned minimum angle to the given vector, in radians.
- bezier_derivative(control_1: Vector3, control_2: Vector3, end: Vector3, t: float) -> Vector3 - Returns the derivative at the given `t` on the defined by this vector and the given `control_1`, `control_2`, and `end` points.
- bezier_interpolate(control_1: Vector3, control_2: Vector3, end: Vector3, t: float) -> Vector3 - Returns the point at the given `t` on the defined by this vector and the given `control_1`, `control_2`, and `end` points.
- bounce(n: Vector3) -> Vector3 - Returns the vector "bounced off" from a plane defined by the given normal `n`. **Note:** `bounce` performs the operation that most engines and frameworks call [code skip-lint]reflect()[/code].
- ceil() -> Vector3 - Returns a new vector with all components rounded up (towards positive infinity).
- clamp(min: Vector3, max: Vector3) -> Vector3 - Returns a new vector with all components clamped between the components of `min` and `max`, by running `@GlobalScope.clamp` on each component.
- clampf(min: float, max: float) -> Vector3 - Returns a new vector with all components clamped between `min` and `max`, by running `@GlobalScope.clamp` on each component.
- cross(with: Vector3) -> Vector3 - Returns the cross product of this vector and `with`. This returns a vector perpendicular to both this and `with`, which would be the normal vector of the plane defined by the two vectors. As there are two such vectors, in opposite directions, this method returns the vector defined by a right-handed coordinate system. If the two vectors are parallel this returns an empty vector, making it useful for testing if two vectors are parallel.
- cubic_interpolate(b: Vector3, pre_a: Vector3, post_b: Vector3, weight: float) -> Vector3 - Performs a cubic interpolation between this vector and `b` using `pre_a` and `post_b` as handles, and returns the result at position `weight`. `weight` is on the range of 0.0 to 1.0, representing the amount of interpolation.
- cubic_interpolate_in_time(b: Vector3, pre_a: Vector3, post_b: Vector3, weight: float, b_t: float, pre_a_t: float, post_b_t: float) -> Vector3 - Performs a cubic interpolation between this vector and `b` using `pre_a` and `post_b` as handles, and returns the result at position `weight`. `weight` is on the range of 0.0 to 1.0, representing the amount of interpolation. It can perform smoother interpolation than `cubic_interpolate` by the time values.
- direction_to(to: Vector3) -> Vector3 - Returns the normalized vector pointing from this vector to `to`. This is equivalent to using `(b - a).normalized()`.
- distance_squared_to(to: Vector3) -> float - Returns the squared distance between this vector and `to`. This method runs faster than `distance_to`, so prefer it if you need to compare vectors or need the squared distance for some formula.
- distance_to(to: Vector3) -> float - Returns the distance between this vector and `to`.
- dot(with: Vector3) -> float - Returns the dot product of this vector and `with`. This can be used to compare the angle between two vectors. For example, this can be used to determine whether an enemy is facing the player. The dot product will be `0` for a right angle (90 degrees), greater than 0 for angles narrower than 90 degrees and lower than 0 for angles wider than 90 degrees. When using unit (normalized) vectors, the result will always be between `-1.0` (180 degree angle) when the vectors are facing opposite directions, and `1.0` (0 degree angle) when the vectors are aligned. **Note:** `a.dot(b)` is equivalent to `b.dot(a)`.
- floor() -> Vector3 - Returns a new vector with all components rounded down (towards negative infinity).
- inverse() -> Vector3 - Returns the inverse of the vector. This is the same as `Vector3(1.0 / v.x, 1.0 / v.y, 1.0 / v.z)`.
- is_equal_approx(to: Vector3) -> bool - Returns `true` if this vector and `to` are approximately equal, by running `@GlobalScope.is_equal_approx` on each component.
- is_finite() -> bool - Returns `true` if this vector is finite, by calling `@GlobalScope.is_finite` on each component.
- is_normalized() -> bool - Returns `true` if the vector is normalized, i.e. its length is approximately equal to 1.
- is_zero_approx() -> bool - Returns `true` if this vector's values are approximately zero, by running `@GlobalScope.is_zero_approx` on each component. This method is faster than using `is_equal_approx` with one value as a zero vector.
- length() -> float - Returns the length (magnitude) of this vector.
- length_squared() -> float - Returns the squared length (squared magnitude) of this vector. This method runs faster than `length`, so prefer it if you need to compare vectors or need the squared distance for some formula.
- lerp(to: Vector3, weight: float) -> Vector3 - Returns the result of the linear interpolation between this vector and `to` by amount `weight`. `weight` is on the range of `0.0` to `1.0`, representing the amount of interpolation.
- limit_length(length: float = 1.0) -> Vector3 - Returns the vector with a maximum length by limiting its length to `length`. If the vector is non-finite, the result is undefined.
- max(with: Vector3) -> Vector3 - Returns the component-wise maximum of this and `with`, equivalent to `Vector3(maxf(x, with.x), maxf(y, with.y), maxf(z, with.z))`.
- max_axis_index() -> int - Returns the axis of the vector's highest value. See `AXIS_*` constants. If all components are equal, this method returns `AXIS_X`.
- maxf(with: float) -> Vector3 - Returns the component-wise maximum of this and `with`, equivalent to `Vector3(maxf(x, with), maxf(y, with), maxf(z, with))`.
- min(with: Vector3) -> Vector3 - Returns the component-wise minimum of this and `with`, equivalent to `Vector3(minf(x, with.x), minf(y, with.y), minf(z, with.z))`.
- min_axis_index() -> int - Returns the axis of the vector's lowest value. See `AXIS_*` constants. If all components are equal, this method returns `AXIS_Z`.
- minf(with: float) -> Vector3 - Returns the component-wise minimum of this and `with`, equivalent to `Vector3(minf(x, with), minf(y, with), minf(z, with))`.
- move_toward(to: Vector3, delta: float) -> Vector3 - Returns a new vector moved toward `to` by the fixed `delta` amount. Will not go past the final value.
- normalized() -> Vector3 - Returns the result of scaling the vector to unit length. Equivalent to `v / v.length()`. Returns `(0, 0, 0)` if `v.length() == 0`. See also `is_normalized`. **Note:** This function may return incorrect values if the input vector length is near zero.
- octahedron_decode(uv: Vector2) -> Vector3 - Returns the Vector3 from an octahedral-compressed form created using `octahedron_encode` (stored as a Vector2).
- octahedron_encode() -> Vector2 - Returns the octahedral-encoded (oct32) form of this Vector3 as a Vector2. Since a Vector2 occupies 1/3 less memory compared to Vector3, this form of compression can be used to pass greater amounts of `normalized` Vector3s without increasing storage or memory requirements. See also `octahedron_decode`. **Note:** `octahedron_encode` can only be used for `normalized` vectors. `octahedron_encode` does *not* check whether this Vector3 is normalized, and will return a value that does not decompress to the original value if the Vector3 is not normalized. **Note:** Octahedral compression is *lossy*, although visual differences are rarely perceptible in real world scenarios.
- outer(with: Vector3) -> Basis - Returns the outer product with `with`.
- posmod(mod: float) -> Vector3 - Returns a vector composed of the `@GlobalScope.fposmod` of this vector's components and `mod`.
- posmodv(modv: Vector3) -> Vector3 - Returns a vector composed of the `@GlobalScope.fposmod` of this vector's components and `modv`'s components.
- project(b: Vector3) -> Vector3 - Returns a new vector resulting from projecting this vector onto the given vector `b`. The resulting new vector is parallel to `b`. See also `slide`. **Note:** If the vector `b` is a zero vector, the components of the resulting new vector will be `@GDScript.NAN`.
- reflect(n: Vector3) -> Vector3 - Returns the result of reflecting the vector through a plane defined by the given normal vector `n`. **Note:** `reflect` differs from what other engines and frameworks call [code skip-lint]reflect()[/code]. In other engines, [code skip-lint]reflect()[/code] returns the result of the vector reflected by the given plane. The reflection thus passes through the given normal. While in Godot the reflection passes through the plane and can be thought of as bouncing off the normal. See also `bounce` which does what most engines call [code skip-lint]reflect()[/code].
- rotated(axis: Vector3, angle: float) -> Vector3 - Returns the result of rotating this vector around a given axis by `angle` (in radians). The axis must be a normalized vector. See also `@GlobalScope.deg_to_rad`.
- round() -> Vector3 - Returns a new vector with all components rounded to the nearest integer, with halfway cases rounded away from zero.
- sign() -> Vector3 - Returns a new vector with each component set to `1.0` if it's positive, `-1.0` if it's negative, and `0.0` if it's zero. The result is identical to calling `@GlobalScope.sign` on each component.
- signed_angle_to(to: Vector3, axis: Vector3) -> float - Returns the signed angle to the given vector, in radians. The sign of the angle is positive in a counter-clockwise direction and negative in a clockwise direction when viewed from the side specified by the `axis`.
- slerp(to: Vector3, weight: float) -> Vector3 - Returns the result of spherical linear interpolation between this vector and `to`, by amount `weight`. `weight` is on the range of 0.0 to 1.0, representing the amount of interpolation. This method also handles interpolating the lengths if the input vectors have different lengths. For the special case of one or both input vectors having zero length, this method behaves like `lerp`.
- slide(n: Vector3) -> Vector3 - Returns a new vector resulting from sliding this vector along a plane with normal `n`. The resulting new vector is perpendicular to `n`, and is equivalent to this vector minus its projection on `n`. See also `project`. **Note:** The vector `n` must be normalized. See also `normalized`.
- snapped(step: Vector3) -> Vector3 - Returns a new vector with each component snapped to the nearest multiple of the corresponding component in `step`. This can also be used to round the components to an arbitrary number of decimals.
- snappedf(step: float) -> Vector3 - Returns a new vector with each component snapped to the nearest multiple of `step`. This can also be used to round the components to an arbitrary number of decimals.

**Enums:**
**Axis:** AXIS_X=0, AXIS_Y=1, AXIS_Z=2
  - AXIS_X: Enumerated value for the X axis. Returned by `max_axis_index` and `min_axis_index`.
  - AXIS_Y: Enumerated value for the Y axis. Returned by `max_axis_index` and `min_axis_index`.
  - AXIS_Z: Enumerated value for the Z axis. Returned by `max_axis_index` and `min_axis_index`.
**Constants:** ZERO=Vector3(0, 0, 0), ONE=Vector3(1, 1, 1), INF=Vector3(inf, inf, inf), LEFT=Vector3(-1, 0, 0), RIGHT=Vector3(1, 0, 0), UP=Vector3(0, 1, 0), DOWN=Vector3(0, -1, 0), FORWARD=Vector3(0, 0, -1), BACK=Vector3(0, 0, 1), MODEL_LEFT=Vector3(1, 0, 0), ...
  - ZERO: Zero vector, a vector with all components set to `0`.
  - ONE: One vector, a vector with all components set to `1`.
  - INF: Infinity vector, a vector with all components set to `@GDScript.INF`.
  - LEFT: Left unit vector. Represents the local direction of left, and the global direction of west.
  - RIGHT: Right unit vector. Represents the local direction of right, and the global direction of east.
  - UP: Up unit vector.
  - DOWN: Down unit vector.
  - FORWARD: Forward unit vector. Represents the local direction of forward, and the global direction of north. Keep in mind that the forward direction for lights, cameras, etc is different from 3D assets like characters, which face towards the camera by convention. Use `Vector3.MODEL_FRONT` and similar constants when working in 3D asset space.
  - BACK: Back unit vector. Represents the local direction of back, and the global direction of south.
  - MODEL_LEFT: Unit vector pointing towards the left side of imported 3D assets.
  - MODEL_RIGHT: Unit vector pointing towards the right side of imported 3D assets.
  - MODEL_TOP: Unit vector pointing towards the top side (up) of imported 3D assets.
  - MODEL_BOTTOM: Unit vector pointing towards the bottom side (down) of imported 3D assets.
  - MODEL_FRONT: Unit vector pointing towards the front side (facing forward) of imported 3D assets.
  - MODEL_REAR: Unit vector pointing towards the rear side (back) of imported 3D assets.

