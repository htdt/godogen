## Polygon2D <- Node2D

A Polygon2D is defined by a set of points. Each point is connected to the next, with the final point being connected to the first, resulting in a closed polygon. Polygon2Ds can be filled with color (solid or gradient) or filled with a given texture.

**Props:**
- antialiased: bool = false
- color: Color = Color(1, 1, 1, 1)
- internal_vertex_count: int = 0
- invert_border: float = 100.0
- invert_enabled: bool = false
- offset: Vector2 = Vector2(0, 0)
- polygon: PackedVector2Array = PackedVector2Array()
- polygons: Array = []
- skeleton: NodePath = NodePath("")
- texture: Texture2D
- texture_offset: Vector2 = Vector2(0, 0)
- texture_rotation: float = 0.0
- texture_scale: Vector2 = Vector2(1, 1)
- uv: PackedVector2Array = PackedVector2Array()
- vertex_colors: PackedColorArray = PackedColorArray()

- **antialiased**: If `true`, polygon edges will be anti-aliased.
- **color**: The polygon's fill color. If `texture` is set, it will be multiplied by this color. It will also be the default color for vertices not set in `vertex_colors`.
- **internal_vertex_count**: Number of internal vertices, used for UV mapping.
- **invert_border**: Added padding applied to the bounding box when `invert_enabled` is set to `true`. Setting this value too small may result in a "Bad Polygon" error.
- **invert_enabled**: If `true`, the polygon will be inverted, containing the area outside the defined points and extending to the `invert_border`.
- **offset**: The offset applied to each vertex.
- **polygon**: The polygon's list of vertices. The final point will be connected to the first.
- **polygons**: The list of polygons, in case more than one is being represented. Every individual polygon is stored as a PackedInt32Array where each [int] is an index to a point in `polygon`. If empty, this property will be ignored, and the resulting single polygon will be composed of all points in `polygon`, using the order they are stored in.
- **skeleton**: Path to a Skeleton2D node used for skeleton-based deformations of this polygon. If empty or invalid, skeletal deformations will not be used.
- **texture**: The polygon's fill texture. Use `uv` to set texture coordinates.
- **texture_offset**: Amount to offset the polygon's `texture`. If set to `Vector2(0, 0)`, the texture's origin (its top-left corner) will be placed at the polygon's position.
- **texture_rotation**: The texture's rotation in radians.
- **texture_scale**: Amount to multiply the `uv` coordinates when using `texture`. Larger values make the texture smaller, and vice versa.
- **uv**: Texture coordinates for each vertex of the polygon. There should be one UV value per polygon vertex. If there are fewer, undefined vertices will use `Vector2(0, 0)`.
- **vertex_colors**: Color for each vertex. Colors are interpolated between vertices, resulting in smooth gradients. There should be one per polygon vertex. If there are fewer, undefined vertices will use `color`.

**Methods:**
- add_bone(path: NodePath, weights: PackedFloat32Array) - Adds a bone with the specified `path` and `weights`.
- clear_bones() - Removes all bones from this Polygon2D.
- erase_bone(index: int) - Removes the specified bone from this Polygon2D.
- get_bone_count() -> int - Returns the number of bones in this Polygon2D.
- get_bone_path(index: int) -> NodePath - Returns the path to the node associated with the specified bone.
- get_bone_weights(index: int) -> PackedFloat32Array - Returns the weight values of the specified bone.
- set_bone_path(index: int, path: NodePath) - Sets the path to the node associated with the specified bone.
- set_bone_weights(index: int, weights: PackedFloat32Array) - Sets the weight values for the specified bone.

