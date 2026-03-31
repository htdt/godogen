## PolygonPathFinder <- Resource

**Methods:**
- find_path(from: Vector2, to: Vector2) -> PackedVector2Array
- get_bounds() -> Rect2
- get_closest_point(point: Vector2) -> Vector2
- get_intersections(from: Vector2, to: Vector2) -> PackedVector2Array
- get_point_penalty(idx: int) -> float
- is_point_inside(point: Vector2) -> bool - Returns `true` if `point` falls inside the polygon area.
- set_point_penalty(idx: int, penalty: float)
- setup(points: PackedVector2Array, connections: PackedInt32Array) - Sets up PolygonPathFinder with an array of points that define the vertices of the polygon, and an array of indices that determine the edges of the polygon. The length of `connections` must be even, returns an error if odd.

