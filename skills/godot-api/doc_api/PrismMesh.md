## PrismMesh <- PrimitiveMesh

Class representing a prism-shaped PrimitiveMesh.

**Props:**
- left_to_right: float = 0.5
- size: Vector3 = Vector3(1, 1, 1)
- subdivide_depth: int = 0
- subdivide_height: int = 0
- subdivide_width: int = 0

- **left_to_right**: Displacement of the upper edge along the X axis. 0.0 positions edge straight above the bottom-left edge.
- **size**: Size of the prism.
- **subdivide_depth**: Number of added edge loops along the Z axis.
- **subdivide_height**: Number of added edge loops along the Y axis.
- **subdivide_width**: Number of added edge loops along the X axis.

