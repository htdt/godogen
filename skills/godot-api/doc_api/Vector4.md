## Vector4

A 4-element structure that can be used to represent 4D coordinates or any other quadruplet of numeric values. It uses floating-point coordinates. By default, these floating-point values use 32-bit precision, unlike [float] which is always 64-bit. If double precision is needed, compile the engine with the option `precision=double`. See Vector4i for its integer counterpart. **Note:** In a boolean context, a Vector4 will evaluate to `false` if it's equal to `Vector4(0, 0, 0, 0)`. Otherwise, a Vector4 will always evaluate to `true`.

**Props:**
- w: float = 0.0
- x: float = 0.0
- y: float = 0.0
- z: float = 0.0

- **w**: The vector's W component. Also accessible by using the index position `[3]`.
- **x**: The vector's X component. Also accessible by using the index position `[0]`.
- **y**: The vector's Y component. Also accessible by using the index position `[1]`.
- **z**: The vector's Z component. Also accessible by using the index position `[2]`.

**Methods:**
- abs() -> Vector4 - Returns a new vector with all components in absolute values (i.e. positive).
- ceil() -> Vector4 - Returns a new vector with all components rounded up (towards positive infinity).
- clamp(min: Vector4, max: Vector4) -> Vector4 - Returns a new vector with all components clamped between the components of `min` and `max`, by running `@GlobalScope.clamp` on each component.
- clampf(min: float, max: float) -> Vector4 - Returns a new vector with all components clamped between `min` and `max`, by running `@GlobalScope.clamp` on each component.
- cubic_interpolate(b: Vector4, pre_a: Vector4, post_b: Vector4, weight: float) -> Vector4 - Performs a cubic interpolation between this vector and `b` using `pre_a` and `post_b` as handles, and returns the result at position `weight`. `weight` is on the range of 0.0 to 1.0, representing the amount of interpolation.
- cubic_interpolate_in_time(b: Vector4, pre_a: Vector4, post_b: Vector4, weight: float, b_t: float, pre_a_t: float, post_b_t: float) -> Vector4 - Performs a cubic interpolation between this vector and `b` using `pre_a` and `post_b` as handles, and returns the result at position `weight`. `weight` is on the range of 0.0 to 1.0, representing the amount of interpolation. It can perform smoother interpolation than `cubic_interpolate` by the time values.
- direction_to(to: Vector4) -> Vector4 - Returns the normalized vector pointing from this vector to `to`. This is equivalent to using `(b - a).normalized()`.
- distance_squared_to(to: Vector4) -> float - Returns the squared distance between this vector and `to`. This method runs faster than `distance_to`, so prefer it if you need to compare vectors or need the squared distance for some formula.
- distance_to(to: Vector4) -> float - Returns the distance between this vector and `to`.
- dot(with: Vector4) -> float - Returns the dot product of this vector and `with`.
- floor() -> Vector4 - Returns a new vector with all components rounded down (towards negative infinity).
- inverse() -> Vector4 - Returns the inverse of the vector. This is the same as `Vector4(1.0 / v.x, 1.0 / v.y, 1.0 / v.z, 1.0 / v.w)`.
- is_equal_approx(to: Vector4) -> bool - Returns `true` if this vector and `to` are approximately equal, by running `@GlobalScope.is_equal_approx` on each component.
- is_finite() -> bool - Returns `true` if this vector is finite, by calling `@GlobalScope.is_finite` on each component.
- is_normalized() -> bool - Returns `true` if the vector is normalized, i.e. its length is approximately equal to 1.
- is_zero_approx() -> bool - Returns `true` if this vector's values are approximately zero, by running `@GlobalScope.is_zero_approx` on each component. This method is faster than using `is_equal_approx` with one value as a zero vector.
- length() -> float - Returns the length (magnitude) of this vector.
- length_squared() -> float - Returns the squared length (squared magnitude) of this vector. This method runs faster than `length`, so prefer it if you need to compare vectors or need the squared distance for some formula.
- lerp(to: Vector4, weight: float) -> Vector4 - Returns the result of the linear interpolation between this vector and `to` by amount `weight`. `weight` is on the range of `0.0` to `1.0`, representing the amount of interpolation.
- max(with: Vector4) -> Vector4 - Returns the component-wise maximum of this and `with`, equivalent to `Vector4(maxf(x, with.x), maxf(y, with.y), maxf(z, with.z), maxf(w, with.w))`.
- max_axis_index() -> int - Returns the axis of the vector's highest value. See `AXIS_*` constants. If all components are equal, this method returns `AXIS_X`.
- maxf(with: float) -> Vector4 - Returns the component-wise maximum of this and `with`, equivalent to `Vector4(maxf(x, with), maxf(y, with), maxf(z, with), maxf(w, with))`.
- min(with: Vector4) -> Vector4 - Returns the component-wise minimum of this and `with`, equivalent to `Vector4(minf(x, with.x), minf(y, with.y), minf(z, with.z), minf(w, with.w))`.
- min_axis_index() -> int - Returns the axis of the vector's lowest value. See `AXIS_*` constants. If all components are equal, this method returns `AXIS_W`.
- minf(with: float) -> Vector4 - Returns the component-wise minimum of this and `with`, equivalent to `Vector4(minf(x, with), minf(y, with), minf(z, with), minf(w, with))`.
- normalized() -> Vector4 - Returns the result of scaling the vector to unit length. Equivalent to `v / v.length()`. Returns `(0, 0, 0, 0)` if `v.length() == 0`. See also `is_normalized`. **Note:** This function may return incorrect values if the input vector length is near zero.
- posmod(mod: float) -> Vector4 - Returns a vector composed of the `@GlobalScope.fposmod` of this vector's components and `mod`.
- posmodv(modv: Vector4) -> Vector4 - Returns a vector composed of the `@GlobalScope.fposmod` of this vector's components and `modv`'s components.
- round() -> Vector4 - Returns a new vector with all components rounded to the nearest integer, with halfway cases rounded away from zero.
- sign() -> Vector4 - Returns a new vector with each component set to `1.0` if it's positive, `-1.0` if it's negative, and `0.0` if it's zero. The result is identical to calling `@GlobalScope.sign` on each component.
- snapped(step: Vector4) -> Vector4 - Returns a new vector with each component snapped to the nearest multiple of the corresponding component in `step`. This can also be used to round the components to an arbitrary number of decimals.
- snappedf(step: float) -> Vector4 - Returns a new vector with each component snapped to the nearest multiple of `step`. This can also be used to round the components to an arbitrary number of decimals.

**Enums:**
**Axis:** AXIS_X=0, AXIS_Y=1, AXIS_Z=2, AXIS_W=3
  - AXIS_X: Enumerated value for the X axis. Returned by `max_axis_index` and `min_axis_index`.
  - AXIS_Y: Enumerated value for the Y axis. Returned by `max_axis_index` and `min_axis_index`.
  - AXIS_Z: Enumerated value for the Z axis. Returned by `max_axis_index` and `min_axis_index`.
  - AXIS_W: Enumerated value for the W axis. Returned by `max_axis_index` and `min_axis_index`.
**Constants:** ZERO=Vector4(0, 0, 0, 0), ONE=Vector4(1, 1, 1, 1), INF=Vector4(inf, inf, inf, inf)
  - ZERO: Zero vector, a vector with all components set to `0`.
  - ONE: One vector, a vector with all components set to `1`.
  - INF: Infinity vector, a vector with all components set to `@GDScript.INF`.

