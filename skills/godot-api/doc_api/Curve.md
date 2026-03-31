## Curve <- Resource

This resource describes a mathematical curve by defining a set of points and tangents at each point. By default, it ranges between `0` and `1` on the X and Y axes, but these ranges can be changed. Please note that many resources and nodes assume they are given *unit curves*. A unit curve is a curve whose domain (the X axis) is between `0` and `1`. Some examples of unit curve usage are `CPUParticles2D.angle_curve` and `Line2D.width_curve`.

**Props:**
- bake_resolution: int = 100
- max_domain: float = 1.0
- max_value: float = 1.0
- min_domain: float = 0.0
- min_value: float = 0.0
- point_count: int = 0
- point_{index}/left_mode: int = 0
- point_{index}/left_tangent: float = 0.0
- point_{index}/position: Vector2 = Vector2(0, 0)
- point_{index}/right_mode: int = 0
- point_{index}/right_tangent: float = 0.0

- **bake_resolution**: The number of points to include in the baked (i.e. cached) curve data.
- **max_domain**: The maximum domain (x-coordinate) that points can have.
- **max_value**: The maximum value (y-coordinate) that points can have. Tangents can cause higher values between points.
- **min_domain**: The minimum domain (x-coordinate) that points can have.
- **min_value**: The minimum value (y-coordinate) that points can have. Tangents can cause lower values between points.
- **point_count**: The number of points describing the curve.
- **point_{index}/left_mode**: The left `TangentMode` for the point at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.
- **point_{index}/left_tangent**: The left tangent angle (in degrees) for the point at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.
- **point_{index}/position**: The position of the point at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.
- **point_{index}/right_mode**: The right `TangentMode` for the point at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.
- **point_{index}/right_tangent**: The right tangent angle (in degrees) for the point at `index`. **Note:** `index` is a value in the `0 .. point_count - 1` range.

**Methods:**
- add_point(position: Vector2, left_tangent: float = 0, right_tangent: float = 0, left_mode: int = 0, right_mode: int = 0) -> int - Adds a point to the curve. For each side, if the `*_mode` is `TANGENT_LINEAR`, the `*_tangent` angle (in degrees) uses the slope of the curve halfway to the adjacent point. Allows custom assignments to the `*_tangent` angle if `*_mode` is set to `TANGENT_FREE`.
- bake() - Recomputes the baked cache of points for the curve.
- clean_dupes() - Removes duplicate points, i.e. points that are less than 0.00001 units (engine epsilon value) away from their neighbor on the curve.
- clear_points() - Removes all points from the curve.
- get_domain_range() -> float - Returns the difference between `min_domain` and `max_domain`.
- get_point_left_mode(index: int) -> int - Returns the left `TangentMode` for the point at `index`.
- get_point_left_tangent(index: int) -> float - Returns the left tangent angle (in degrees) for the point at `index`.
- get_point_position(index: int) -> Vector2 - Returns the curve coordinates for the point at `index`.
- get_point_right_mode(index: int) -> int - Returns the right `TangentMode` for the point at `index`.
- get_point_right_tangent(index: int) -> float - Returns the right tangent angle (in degrees) for the point at `index`.
- get_value_range() -> float - Returns the difference between `min_value` and `max_value`.
- remove_point(index: int) - Removes the point at `index` from the curve.
- sample(offset: float) -> float - Returns the Y value for the point that would exist at the X position `offset` along the curve.
- sample_baked(offset: float) -> float - Returns the Y value for the point that would exist at the X position `offset` along the curve using the baked cache. Bakes the curve's points if not already baked.
- set_point_left_mode(index: int, mode: int) - Sets the left `TangentMode` for the point at `index` to `mode`.
- set_point_left_tangent(index: int, tangent: float) - Sets the left tangent angle for the point at `index` to `tangent`.
- set_point_offset(index: int, offset: float) -> int - Sets the offset from `0.5`.
- set_point_right_mode(index: int, mode: int) - Sets the right `TangentMode` for the point at `index` to `mode`.
- set_point_right_tangent(index: int, tangent: float) - Sets the right tangent angle for the point at `index` to `tangent`.
- set_point_value(index: int, y: float) - Assigns the vertical position `y` to the point at `index`.

**Signals:**
- domain_changed - Emitted when `max_domain` or `min_domain` is changed.
- range_changed - Emitted when `max_value` or `min_value` is changed.

**Enums:**
**TangentMode:** TANGENT_FREE=0, TANGENT_LINEAR=1, TANGENT_MODE_COUNT=2
  - TANGENT_FREE: The tangent on this side of the point is user-defined.
  - TANGENT_LINEAR: The curve calculates the tangent on this side of the point as the slope halfway towards the adjacent point.
  - TANGENT_MODE_COUNT: The total number of available tangent modes.

