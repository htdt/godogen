## Vector2

A 2-element structure that can be used to represent 2D coordinates or any other pair of numeric values. It uses floating-point coordinates. By default, these floating-point values use 32-bit precision, unlike [float] which is always 64-bit. If double precision is needed, compile the engine with the option `precision=double`. See Vector2i for its integer counterpart. **Note:** In a boolean context, a Vector2 will evaluate to `false` if it's equal to `Vector2(0, 0)`. Otherwise, a Vector2 will always evaluate to `true`.

**Props:**
- x: float = 0.0
- y: float = 0.0

- **x**: The vector's X component. Also accessible by using the index position `[0]`.
- **y**: The vector's Y component. Also accessible by using the index position `[1]`.

**Methods:**
- abs() -> Vector2 - Returns a new vector with all components in absolute values (i.e. positive).
- angle() -> float - Returns this vector's angle with respect to the positive X axis, or `(1, 0)` vector, in radians. For example, `Vector2.RIGHT.angle()` will return zero, `Vector2.DOWN.angle()` will return `PI / 2` (a quarter turn, or 90 degrees), and `Vector2(1, -1).angle()` will return `-PI / 4` (a negative eighth turn, or -45 degrees). This is equivalent to calling `@GlobalScope.atan2` with `y` and `x`.
- angle_to(to: Vector2) -> float - Returns the signed angle to the given vector, in radians. The result ranges from `-PI` to `PI` (inclusive).
- angle_to_point(to: Vector2) -> float - Returns the signed angle between the X axis and the line from this vector to point `to`, in radians. The result ranges from `-PI` to `PI` (inclusive). `a.angle_to_point(b)` is equivalent to `(b - a).angle()`. See also `angle`.
- aspect() -> float - Returns this vector's aspect ratio, which is `x` divided by `y`.
- bezier_derivative(control_1: Vector2, control_2: Vector2, end: Vector2, t: float) -> Vector2 - Returns the derivative at the given `t` on the defined by this vector and the given `control_1`, `control_2`, and `end` points.
- bezier_interpolate(control_1: Vector2, control_2: Vector2, end: Vector2, t: float) -> Vector2 - Returns the point at the given `t` on the defined by this vector and the given `control_1`, `control_2`, and `end` points.
- bounce(n: Vector2) -> Vector2 - Returns the vector "bounced off" from a line defined by the given normal `n` perpendicular to the line. **Note:** `bounce` performs the operation that most engines and frameworks call [code skip-lint]reflect()[/code].
- ceil() -> Vector2 - Returns a new vector with all components rounded up (towards positive infinity).
- clamp(min: Vector2, max: Vector2) -> Vector2 - Returns a new vector with all components clamped between the components of `min` and `max`, by running `@GlobalScope.clamp` on each component.
- clampf(min: float, max: float) -> Vector2 - Returns a new vector with all components clamped between `min` and `max`, by running `@GlobalScope.clamp` on each component.
- cross(with: Vector2) -> float - Returns the 2D analog of the cross product for this vector and `with`. This is the signed area of the parallelogram formed by the two vectors. If the second vector is clockwise from the first vector, then the cross product is the positive area. If counter-clockwise, the cross product is the negative area. If the two vectors are parallel this returns zero, making it useful for testing if two vectors are parallel. **Note:** Cross product is not defined in 2D mathematically. This method embeds the 2D vectors in the XY plane of 3D space and uses their cross product's Z component as the analog.
- cubic_interpolate(b: Vector2, pre_a: Vector2, post_b: Vector2, weight: float) -> Vector2 - Performs a cubic interpolation between this vector and `b` using `pre_a` and `post_b` as handles, and returns the result at position `weight`. `weight` is on the range of 0.0 to 1.0, representing the amount of interpolation.
- cubic_interpolate_in_time(b: Vector2, pre_a: Vector2, post_b: Vector2, weight: float, b_t: float, pre_a_t: float, post_b_t: float) -> Vector2 - Performs a cubic interpolation between this vector and `b` using `pre_a` and `post_b` as handles, and returns the result at position `weight`. `weight` is on the range of 0.0 to 1.0, representing the amount of interpolation. It can perform smoother interpolation than `cubic_interpolate` by the time values.
- direction_to(to: Vector2) -> Vector2 - Returns the normalized vector pointing from this vector to `to`. `a.direction_to(b)` is equivalent to `(b - a).normalized()`. See also `normalized`.
- distance_squared_to(to: Vector2) -> float - Returns the squared distance between this vector and `to`. This method runs faster than `distance_to`, so prefer it if you need to compare vectors or need the squared distance for some formula.
- distance_to(to: Vector2) -> float - Returns the distance between this vector and `to`.
- dot(with: Vector2) -> float - Returns the dot product of this vector and `with`. This can be used to compare the angle between two vectors. For example, this can be used to determine whether an enemy is facing the player. The dot product will be `0` for a right angle (90 degrees), greater than 0 for angles narrower than 90 degrees and lower than 0 for angles wider than 90 degrees. When using unit (normalized) vectors, the result will always be between `-1.0` (180 degree angle) when the vectors are facing opposite directions, and `1.0` (0 degree angle) when the vectors are aligned. **Note:** `a.dot(b)` is equivalent to `b.dot(a)`.
- floor() -> Vector2 - Returns a new vector with all components rounded down (towards negative infinity).
- from_angle(angle: float) -> Vector2 - Creates a Vector2 rotated to the given `angle` in radians. This is equivalent to doing `Vector2(cos(angle), sin(angle))` or `Vector2.RIGHT.rotated(angle)`. **Note:** The length of the returned Vector2 is *approximately* `1.0`, but is is not guaranteed to be exactly `1.0` due to floating-point precision issues. Call `normalized` on the returned Vector2 if you require a unit vector.
- is_equal_approx(to: Vector2) -> bool - Returns `true` if this vector and `to` are approximately equal, by running `@GlobalScope.is_equal_approx` on each component.
- is_finite() -> bool - Returns `true` if this vector is finite, by calling `@GlobalScope.is_finite` on each component.
- is_normalized() -> bool - Returns `true` if the vector is normalized, i.e. its length is approximately equal to 1.
- is_zero_approx() -> bool - Returns `true` if this vector's values are approximately zero, by running `@GlobalScope.is_zero_approx` on each component. This method is faster than using `is_equal_approx` with one value as a zero vector.
- length() -> float - Returns the length (magnitude) of this vector.
- length_squared() -> float - Returns the squared length (squared magnitude) of this vector. This method runs faster than `length`, so prefer it if you need to compare vectors or need the squared distance for some formula.
- lerp(to: Vector2, weight: float) -> Vector2 - Returns the result of the linear interpolation between this vector and `to` by amount `weight`. `weight` is on the range of `0.0` to `1.0`, representing the amount of interpolation.
- limit_length(length: float = 1.0) -> Vector2 - Returns the vector with a maximum length by limiting its length to `length`. If the vector is non-finite, the result is undefined.
- max(with: Vector2) -> Vector2 - Returns the component-wise maximum of this and `with`, equivalent to `Vector2(maxf(x, with.x), maxf(y, with.y))`.
- max_axis_index() -> int - Returns the axis of the vector's highest value. See `AXIS_*` constants. If all components are equal, this method returns `AXIS_X`.
- maxf(with: float) -> Vector2 - Returns the component-wise maximum of this and `with`, equivalent to `Vector2(maxf(x, with), maxf(y, with))`.
- min(with: Vector2) -> Vector2 - Returns the component-wise minimum of this and `with`, equivalent to `Vector2(minf(x, with.x), minf(y, with.y))`.
- min_axis_index() -> int - Returns the axis of the vector's lowest value. See `AXIS_*` constants. If all components are equal, this method returns `AXIS_Y`.
- minf(with: float) -> Vector2 - Returns the component-wise minimum of this and `with`, equivalent to `Vector2(minf(x, with), minf(y, with))`.
- move_toward(to: Vector2, delta: float) -> Vector2 - Returns a new vector moved toward `to` by the fixed `delta` amount. Will not go past the final value.
- normalized() -> Vector2 - Returns the result of scaling the vector to unit length. Equivalent to `v / v.length()`. Returns `(0, 0)` if `v.length() == 0`. See also `is_normalized`. **Note:** This function may return incorrect values if the input vector length is near zero.
- orthogonal() -> Vector2 - Returns a perpendicular vector rotated 90 degrees counter-clockwise compared to the original, with the same length.
- posmod(mod: float) -> Vector2 - Returns a vector composed of the `@GlobalScope.fposmod` of this vector's components and `mod`.
- posmodv(modv: Vector2) -> Vector2 - Returns a vector composed of the `@GlobalScope.fposmod` of this vector's components and `modv`'s components.
- project(b: Vector2) -> Vector2 - Returns a new vector resulting from projecting this vector onto the given vector `b`. The resulting new vector is parallel to `b`. See also `slide`. **Note:** If the vector `b` is a zero vector, the components of the resulting new vector will be `@GDScript.NAN`.
- reflect(line: Vector2) -> Vector2 - Returns the result of reflecting the vector from a line defined by the given direction vector `line`. **Note:** `reflect` differs from what other engines and frameworks call [code skip-lint]reflect()[/code]. In other engines, [code skip-lint]reflect()[/code] takes a normal direction which is a direction perpendicular to the line. In Godot, you specify the direction of the line directly. See also `bounce` which does what most engines call [code skip-lint]reflect()[/code].
- rotated(angle: float) -> Vector2 - Returns the result of rotating this vector by `angle` (in radians). See also `@GlobalScope.deg_to_rad`.
- round() -> Vector2 - Returns a new vector with all components rounded to the nearest integer, with halfway cases rounded away from zero.
- sign() -> Vector2 - Returns a new vector with each component set to `1.0` if it's positive, `-1.0` if it's negative, and `0.0` if it's zero. The result is identical to calling `@GlobalScope.sign` on each component.
- slerp(to: Vector2, weight: float) -> Vector2 - Returns the result of spherical linear interpolation between this vector and `to`, by amount `weight`. `weight` is on the range of 0.0 to 1.0, representing the amount of interpolation. This method also handles interpolating the lengths if the input vectors have different lengths. For the special case of one or both input vectors having zero length, this method behaves like `lerp`.
- slide(n: Vector2) -> Vector2 - Returns a new vector resulting from sliding this vector along a line with normal `n`. The resulting new vector is perpendicular to `n`, and is equivalent to this vector minus its projection on `n`. See also `project`. **Note:** The vector `n` must be normalized. See also `normalized`.
- snapped(step: Vector2) -> Vector2 - Returns a new vector with each component snapped to the nearest multiple of the corresponding component in `step`. This can also be used to round the components to an arbitrary number of decimals.
- snappedf(step: float) -> Vector2 - Returns a new vector with each component snapped to the nearest multiple of `step`. This can also be used to round the components to an arbitrary number of decimals.

**Enums:**
**Axis:** AXIS_X=0, AXIS_Y=1
  - AXIS_X: Enumerated value for the X axis. Returned by `max_axis_index` and `min_axis_index`.
  - AXIS_Y: Enumerated value for the Y axis. Returned by `max_axis_index` and `min_axis_index`.
**Constants:** ZERO=Vector2(0, 0), ONE=Vector2(1, 1), INF=Vector2(inf, inf), LEFT=Vector2(-1, 0), RIGHT=Vector2(1, 0), UP=Vector2(0, -1), DOWN=Vector2(0, 1)
  - ZERO: Zero vector, a vector with all components set to `0`.
  - ONE: One vector, a vector with all components set to `1`.
  - INF: Infinity vector, a vector with all components set to `@GDScript.INF`.
  - LEFT: Left unit vector. Represents the direction of left.
  - RIGHT: Right unit vector. Represents the direction of right.
  - UP: Up unit vector. Y is down in 2D, so this vector points -Y.
  - DOWN: Down unit vector. Y is down in 2D, so this vector points +Y.

