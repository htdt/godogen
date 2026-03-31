## Plane

Represents a normalized plane equation. `normal` is the normal of the plane (a, b, c normalized), and `d` is the distance from the origin to the plane (in the direction of "normal"). "Over" or "Above" the plane is considered the side of the plane towards where the normal is pointing. **Note:** In a boolean context, a plane will evaluate to `false` if all its components equal `0`. Otherwise, a plane will always evaluate to `true`.

**Props:**
- d: float = 0.0
- normal: Vector3 = Vector3(0, 0, 0)
- x: float = 0.0
- y: float = 0.0
- z: float = 0.0

- **d**: The distance from the origin to the plane, expressed in terms of `normal` (according to its direction and magnitude). Actual absolute distance from the origin to the plane can be calculated as `abs(d) / normal.length()` (if `normal` has zero length then this Plane does not represent a valid plane). In the scalar equation of the plane `ax + by + cz = d`, this is [code skip-lint]d[/code], while the `(a, b, c)` coordinates are represented by the `normal` property.
- **normal**: The normal of the plane, typically a unit vector. Shouldn't be a zero vector as Plane with such `normal` does not represent a valid plane. In the scalar equation of the plane `ax + by + cz = d`, this is the vector `(a, b, c)`, where [code skip-lint]d[/code] is the `d` property.
- **x**: The X component of the plane's `normal` vector.
- **y**: The Y component of the plane's `normal` vector.
- **z**: The Z component of the plane's `normal` vector.

**Methods:**
- distance_to(point: Vector3) -> float - Returns the shortest distance from the plane to the position `point`. If the point is above the plane, the distance will be positive. If below, the distance will be negative.
- get_center() -> Vector3 - Returns the center of the plane.
- has_point(point: Vector3, tolerance: float = 1e-05) -> bool - Returns `true` if `point` is inside the plane. Comparison uses a custom minimum `tolerance` threshold.
- intersect_3(b: Plane, c: Plane) -> Variant - Returns the intersection point of the three planes `b`, `c` and this plane. If no intersection is found, `null` is returned.
- intersects_ray(from: Vector3, dir: Vector3) -> Variant - Returns the intersection point of a ray consisting of the position `from` and the direction normal `dir` with this plane. If no intersection is found, `null` is returned.
- intersects_segment(from: Vector3, to: Vector3) -> Variant - Returns the intersection point of a segment from position `from` to position `to` with this plane. If no intersection is found, `null` is returned.
- is_equal_approx(to_plane: Plane) -> bool - Returns `true` if this plane and `to_plane` are approximately equal, by running `@GlobalScope.is_equal_approx` on each component.
- is_finite() -> bool - Returns `true` if this plane is finite, by calling `@GlobalScope.is_finite` on each component.
- is_point_over(point: Vector3) -> bool - Returns `true` if `point` is located above the plane.
- normalized() -> Plane - Returns a copy of the plane, with normalized `normal` (so it's a unit vector). Returns `Plane(0, 0, 0, 0)` if `normal` can't be normalized (it has zero length).
- project(point: Vector3) -> Vector3 - Returns the orthogonal projection of `point` into a point in the plane.

**Enums:**
**Constants:** PLANE_YZ=Plane(1, 0, 0, 0), PLANE_XZ=Plane(0, 1, 0, 0), PLANE_XY=Plane(0, 0, 1, 0)
  - PLANE_YZ: A plane that extends in the Y and Z axes (normal vector points +X).
  - PLANE_XZ: A plane that extends in the X and Z axes (normal vector points +Y).
  - PLANE_XY: A plane that extends in the X and Y axes (normal vector points +Z).

