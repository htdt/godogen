## OccluderPolygon2D <- Resource

Editor facility that helps you draw a 2D polygon used as resource for LightOccluder2D.

**Props:**
- closed: bool = true
- cull_mode: int (OccluderPolygon2D.CullMode) = 0
- polygon: PackedVector2Array = PackedVector2Array()

- **closed**: If `true`, closes the polygon. A closed OccluderPolygon2D occludes the light coming from any direction. An opened OccluderPolygon2D occludes the light only at its outline's direction.
- **cull_mode**: The culling mode to use.
- **polygon**: A Vector2 array with the index for polygon's vertices positions.

**Enums:**
**CullMode:** CULL_DISABLED=0, CULL_CLOCKWISE=1, CULL_COUNTER_CLOCKWISE=2
  - CULL_DISABLED: Culling is disabled. See `cull_mode`.
  - CULL_CLOCKWISE: Culling is performed in the clockwise direction. See `cull_mode`.
  - CULL_COUNTER_CLOCKWISE: Culling is performed in the counterclockwise direction. See `cull_mode`.

