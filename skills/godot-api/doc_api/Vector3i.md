## Vector3i

A 3-element structure that can be used to represent 3D grid coordinates or any other triplet of integers. It uses integer coordinates and is therefore preferable to Vector3 when exact precision is required. Note that the values are limited to 32 bits, and unlike Vector3 this cannot be configured with an engine build option. Use [int] or PackedInt64Array if 64-bit values are needed. **Note:** In a boolean context, a Vector3i will evaluate to `false` if it's equal to `Vector3i(0, 0, 0)`. Otherwise, a Vector3i will always evaluate to `true`.

**Props:**
- x: int = 0
- y: int = 0
- z: int = 0

- **x**: The vector's X component. Also accessible by using the index position `[0]`.
- **y**: The vector's Y component. Also accessible by using the index position `[1]`.
- **z**: The vector's Z component. Also accessible by using the index position `[2]`.

**Methods:**
- abs() -> Vector3i - Returns a new vector with all components in absolute values (i.e. positive).
- clamp(min: Vector3i, max: Vector3i) -> Vector3i - Returns a new vector with all components clamped between the components of `min` and `max`, by running `@GlobalScope.clamp` on each component.
- clampi(min: int, max: int) -> Vector3i - Returns a new vector with all components clamped between `min` and `max`, by running `@GlobalScope.clamp` on each component.
- distance_squared_to(to: Vector3i) -> int - Returns the squared distance between this vector and `to`. This method runs faster than `distance_to`, so prefer it if you need to compare vectors or need the squared distance for some formula.
- distance_to(to: Vector3i) -> float - Returns the distance between this vector and `to`.
- length() -> float - Returns the length (magnitude) of this vector.
- length_squared() -> int - Returns the squared length (squared magnitude) of this vector. This method runs faster than `length`, so prefer it if you need to compare vectors or need the squared distance for some formula.
- max(with: Vector3i) -> Vector3i - Returns the component-wise maximum of this and `with`, equivalent to `Vector3i(maxi(x, with.x), maxi(y, with.y), maxi(z, with.z))`.
- max_axis_index() -> int - Returns the axis of the vector's highest value. See `AXIS_*` constants. If all components are equal, this method returns `AXIS_X`.
- maxi(with: int) -> Vector3i - Returns the component-wise maximum of this and `with`, equivalent to `Vector3i(maxi(x, with), maxi(y, with), maxi(z, with))`.
- min(with: Vector3i) -> Vector3i - Returns the component-wise minimum of this and `with`, equivalent to `Vector3i(mini(x, with.x), mini(y, with.y), mini(z, with.z))`.
- min_axis_index() -> int - Returns the axis of the vector's lowest value. See `AXIS_*` constants. If all components are equal, this method returns `AXIS_Z`.
- mini(with: int) -> Vector3i - Returns the component-wise minimum of this and `with`, equivalent to `Vector3i(mini(x, with), mini(y, with), mini(z, with))`.
- sign() -> Vector3i - Returns a new vector with each component set to `1` if it's positive, `-1` if it's negative, and `0` if it's zero. The result is identical to calling `@GlobalScope.sign` on each component.
- snapped(step: Vector3i) -> Vector3i - Returns a new vector with each component snapped to the closest multiple of the corresponding component in `step`.
- snappedi(step: int) -> Vector3i - Returns a new vector with each component snapped to the closest multiple of `step`.

**Enums:**
**Axis:** AXIS_X=0, AXIS_Y=1, AXIS_Z=2
  - AXIS_X: Enumerated value for the X axis. Returned by `max_axis_index` and `min_axis_index`.
  - AXIS_Y: Enumerated value for the Y axis. Returned by `max_axis_index` and `min_axis_index`.
  - AXIS_Z: Enumerated value for the Z axis. Returned by `max_axis_index` and `min_axis_index`.
**Constants:** ZERO=Vector3i(0, 0, 0), ONE=Vector3i(1, 1, 1), MIN=Vector3i(-2147483648, -2147483648, -2147483648), MAX=Vector3i(2147483647, 2147483647, 2147483647), LEFT=Vector3i(-1, 0, 0), RIGHT=Vector3i(1, 0, 0), UP=Vector3i(0, 1, 0), DOWN=Vector3i(0, -1, 0), FORWARD=Vector3i(0, 0, -1), BACK=Vector3i(0, 0, 1)
  - ZERO: Zero vector, a vector with all components set to `0`.
  - ONE: One vector, a vector with all components set to `1`.
  - MIN: Min vector, a vector with all components equal to `INT32_MIN`. Can be used as a negative integer equivalent of `Vector3.INF`.
  - MAX: Max vector, a vector with all components equal to `INT32_MAX`. Can be used as an integer equivalent of `Vector3.INF`.
  - LEFT: Left unit vector. Represents the local direction of left, and the global direction of west.
  - RIGHT: Right unit vector. Represents the local direction of right, and the global direction of east.
  - UP: Up unit vector.
  - DOWN: Down unit vector.
  - FORWARD: Forward unit vector. Represents the local direction of forward, and the global direction of north.
  - BACK: Back unit vector. Represents the local direction of back, and the global direction of south.

