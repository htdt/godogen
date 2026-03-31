## Mesh <- Resource

Mesh is a type of Resource that contains vertex array-based geometry, divided in *surfaces*. Each surface contains a completely separate array and a material used to draw it. Design wise, a mesh with multiple surfaces is preferred to a single surface, because objects created in 3D editing software commonly contain multiple materials. The maximum number of surfaces per mesh is `RenderingServer.MAX_MESH_SURFACES`.

**Props:**
- lightmap_size_hint: Vector2i = Vector2i(0, 0)

- **lightmap_size_hint**: Sets a hint to be used for lightmap resolution.

**Methods:**
- _get_aabb() -> AABB - Virtual method to override the AABB for a custom class extending Mesh.
- _get_blend_shape_count() -> int - Virtual method to override the number of blend shapes for a custom class extending Mesh.
- _get_blend_shape_name(index: int) -> StringName - Virtual method to override the retrieval of blend shape names for a custom class extending Mesh.
- _get_surface_count() -> int - Virtual method to override the surface count for a custom class extending Mesh.
- _set_blend_shape_name(index: int, name: StringName) - Virtual method to override the names of blend shapes for a custom class extending Mesh.
- _surface_get_array_index_len(index: int) -> int - Virtual method to override the surface array index length for a custom class extending Mesh.
- _surface_get_array_len(index: int) -> int - Virtual method to override the surface array length for a custom class extending Mesh.
- _surface_get_arrays(index: int) -> Array - Virtual method to override the surface arrays for a custom class extending Mesh.
- _surface_get_blend_shape_arrays(index: int) -> Array[] - Virtual method to override the blend shape arrays for a custom class extending Mesh.
- _surface_get_format(index: int) -> int - Virtual method to override the surface format for a custom class extending Mesh.
- _surface_get_lods(index: int) -> Dictionary - Virtual method to override the surface LODs for a custom class extending Mesh.
- _surface_get_material(index: int) -> Material - Virtual method to override the surface material for a custom class extending Mesh.
- _surface_get_primitive_type(index: int) -> int - Virtual method to override the surface primitive type for a custom class extending Mesh.
- _surface_set_material(index: int, material: Material) - Virtual method to override the setting of a `material` at the given `index` for a custom class extending Mesh.
- create_convex_shape(clean: bool = true, simplify: bool = false) -> ConvexPolygonShape3D - Calculate a ConvexPolygonShape3D from the mesh. If `clean` is `true` (default), duplicate and interior vertices are removed automatically. You can set it to `false` to make the process faster if not needed. If `simplify` is `true`, the geometry can be further simplified to reduce the number of vertices. Disabled by default.
- create_outline(margin: float) -> Mesh - Calculate an outline mesh at a defined offset (margin) from the original mesh. **Note:** This method typically returns the vertices in reverse order (e.g. clockwise to counterclockwise).
- create_placeholder() -> Resource - Creates a placeholder version of this resource (PlaceholderMesh).
- create_trimesh_shape() -> ConcavePolygonShape3D - Calculate a ConcavePolygonShape3D from the mesh.
- generate_triangle_mesh() -> TriangleMesh - Generate a TriangleMesh from the mesh. Considers only surfaces using one of these primitive types: `PRIMITIVE_TRIANGLES`, `PRIMITIVE_TRIANGLE_STRIP`.
- get_aabb() -> AABB - Returns the smallest AABB enclosing this mesh in local space. Not affected by `custom_aabb`. **Note:** This is only implemented for ArrayMesh and PrimitiveMesh.
- get_faces() -> PackedVector3Array - Returns all the vertices that make up the faces of the mesh. Each three vertices represent one triangle.
- get_surface_count() -> int - Returns the number of surfaces that the Mesh holds. This is equivalent to `MeshInstance3D.get_surface_override_material_count`.
- surface_get_arrays(surf_idx: int) -> Array - Returns the arrays for the vertices, normals, UVs, etc. that make up the requested surface (see `ArrayMesh.add_surface_from_arrays`).
- surface_get_blend_shape_arrays(surf_idx: int) -> Array[] - Returns the blend shape arrays for the requested surface.
- surface_get_material(surf_idx: int) -> Material - Returns a Material in a given surface. Surface is rendered using this material. **Note:** This returns the material within the Mesh resource, not the Material associated to the MeshInstance3D's Surface Material Override properties. To get the Material associated to the MeshInstance3D's Surface Material Override properties, use `MeshInstance3D.get_surface_override_material` instead.
- surface_set_material(surf_idx: int, material: Material) - Sets a Material for a given surface. Surface will be rendered using this material. **Note:** This assigns the material within the Mesh resource, not the Material associated to the MeshInstance3D's Surface Material Override properties. To set the Material associated to the MeshInstance3D's Surface Material Override properties, use `MeshInstance3D.set_surface_override_material` instead.

**Enums:**
**PrimitiveType:** PRIMITIVE_POINTS=0, PRIMITIVE_LINES=1, PRIMITIVE_LINE_STRIP=2, PRIMITIVE_TRIANGLES=3, PRIMITIVE_TRIANGLE_STRIP=4
  - PRIMITIVE_POINTS: Render array as points (one vertex equals one point).
  - PRIMITIVE_LINES: Render array as lines (every two vertices a line is created).
  - PRIMITIVE_LINE_STRIP: Render array as line strip.
  - PRIMITIVE_TRIANGLES: Render array as triangles (every three vertices a triangle is created).
  - PRIMITIVE_TRIANGLE_STRIP: Render array as triangle strips.
**ArrayType:** ARRAY_VERTEX=0, ARRAY_NORMAL=1, ARRAY_TANGENT=2, ARRAY_COLOR=3, ARRAY_TEX_UV=4, ARRAY_TEX_UV2=5, ARRAY_CUSTOM0=6, ARRAY_CUSTOM1=7, ARRAY_CUSTOM2=8, ARRAY_CUSTOM3=9, ...
  - ARRAY_VERTEX: PackedVector3Array, PackedVector2Array, or Array of vertex positions.
  - ARRAY_NORMAL: PackedVector3Array of vertex normals. **Note:** The array has to consist of normal vectors, otherwise they will be normalized by the engine, potentially causing visual discrepancies.
  - ARRAY_TANGENT: PackedFloat32Array of vertex tangents. Each element in groups of 4 floats, first 3 floats determine the tangent, and the last the binormal direction as -1 or 1.
  - ARRAY_COLOR: PackedColorArray of vertex colors.
  - ARRAY_TEX_UV: PackedVector2Array for UV coordinates.
  - ARRAY_TEX_UV2: PackedVector2Array for second UV coordinates.
  - ARRAY_CUSTOM0: Contains custom color channel 0. PackedByteArray if `(format >> Mesh.ARRAY_FORMAT_CUSTOM0_SHIFT) & Mesh.ARRAY_FORMAT_CUSTOM_MASK` is `ARRAY_CUSTOM_RGBA8_UNORM`, `ARRAY_CUSTOM_RGBA8_SNORM`, `ARRAY_CUSTOM_RG_HALF`, or `ARRAY_CUSTOM_RGBA_HALF`. PackedFloat32Array otherwise.
  - ARRAY_CUSTOM1: Contains custom color channel 1. PackedByteArray if `(format >> Mesh.ARRAY_FORMAT_CUSTOM1_SHIFT) & Mesh.ARRAY_FORMAT_CUSTOM_MASK` is `ARRAY_CUSTOM_RGBA8_UNORM`, `ARRAY_CUSTOM_RGBA8_SNORM`, `ARRAY_CUSTOM_RG_HALF`, or `ARRAY_CUSTOM_RGBA_HALF`. PackedFloat32Array otherwise.
  - ARRAY_CUSTOM2: Contains custom color channel 2. PackedByteArray if `(format >> Mesh.ARRAY_FORMAT_CUSTOM2_SHIFT) & Mesh.ARRAY_FORMAT_CUSTOM_MASK` is `ARRAY_CUSTOM_RGBA8_UNORM`, `ARRAY_CUSTOM_RGBA8_SNORM`, `ARRAY_CUSTOM_RG_HALF`, or `ARRAY_CUSTOM_RGBA_HALF`. PackedFloat32Array otherwise.
  - ARRAY_CUSTOM3: Contains custom color channel 3. PackedByteArray if `(format >> Mesh.ARRAY_FORMAT_CUSTOM3_SHIFT) & Mesh.ARRAY_FORMAT_CUSTOM_MASK` is `ARRAY_CUSTOM_RGBA8_UNORM`, `ARRAY_CUSTOM_RGBA8_SNORM`, `ARRAY_CUSTOM_RG_HALF`, or `ARRAY_CUSTOM_RGBA_HALF`. PackedFloat32Array otherwise.
  - ARRAY_BONES: PackedFloat32Array or PackedInt32Array of bone indices. Contains either 4 or 8 numbers per vertex depending on the presence of the `ARRAY_FLAG_USE_8_BONE_WEIGHTS` flag.
  - ARRAY_WEIGHTS: PackedFloat32Array or PackedFloat64Array of bone weights in the range `0.0` to `1.0` (inclusive). Contains either 4 or 8 numbers per vertex depending on the presence of the `ARRAY_FLAG_USE_8_BONE_WEIGHTS` flag.
  - ARRAY_INDEX: PackedInt32Array of integers used as indices referencing vertices, colors, normals, tangents, and textures. All of those arrays must have the same number of elements as the vertex array. No index can be beyond the vertex array size. When this index array is present, it puts the function into "index mode," where the index selects the *i*'th vertex, normal, tangent, color, UV, etc. This means if you want to have different normals or colors along an edge, you have to duplicate the vertices. For triangles, the index array is interpreted as triples, referring to the vertices of each triangle. For lines, the index array is in pairs indicating the start and end of each line.
  - ARRAY_MAX: Represents the size of the `ArrayType` enum.
**ArrayCustomFormat:** ARRAY_CUSTOM_RGBA8_UNORM=0, ARRAY_CUSTOM_RGBA8_SNORM=1, ARRAY_CUSTOM_RG_HALF=2, ARRAY_CUSTOM_RGBA_HALF=3, ARRAY_CUSTOM_R_FLOAT=4, ARRAY_CUSTOM_RG_FLOAT=5, ARRAY_CUSTOM_RGB_FLOAT=6, ARRAY_CUSTOM_RGBA_FLOAT=7, ARRAY_CUSTOM_MAX=8
  - ARRAY_CUSTOM_RGBA8_UNORM: Indicates this custom channel contains unsigned normalized byte colors from 0 to 1, encoded as PackedByteArray.
  - ARRAY_CUSTOM_RGBA8_SNORM: Indicates this custom channel contains signed normalized byte colors from -1 to 1, encoded as PackedByteArray.
  - ARRAY_CUSTOM_RG_HALF: Indicates this custom channel contains half precision float colors, encoded as PackedByteArray. Only red and green channels are used.
  - ARRAY_CUSTOM_RGBA_HALF: Indicates this custom channel contains half precision float colors, encoded as PackedByteArray.
  - ARRAY_CUSTOM_R_FLOAT: Indicates this custom channel contains full float colors, in a PackedFloat32Array. Only the red channel is used.
  - ARRAY_CUSTOM_RG_FLOAT: Indicates this custom channel contains full float colors, in a PackedFloat32Array. Only red and green channels are used.
  - ARRAY_CUSTOM_RGB_FLOAT: Indicates this custom channel contains full float colors, in a PackedFloat32Array. Only red, green and blue channels are used.
  - ARRAY_CUSTOM_RGBA_FLOAT: Indicates this custom channel contains full float colors, in a PackedFloat32Array.
  - ARRAY_CUSTOM_MAX: Represents the size of the `ArrayCustomFormat` enum.
**ArrayFormat:** ARRAY_FORMAT_VERTEX=1, ARRAY_FORMAT_NORMAL=2, ARRAY_FORMAT_TANGENT=4, ARRAY_FORMAT_COLOR=8, ARRAY_FORMAT_TEX_UV=16, ARRAY_FORMAT_TEX_UV2=32, ARRAY_FORMAT_CUSTOM0=64, ARRAY_FORMAT_CUSTOM1=128, ARRAY_FORMAT_CUSTOM2=256, ARRAY_FORMAT_CUSTOM3=512, ...
  - ARRAY_FORMAT_VERTEX: Mesh array contains vertices. All meshes require a vertex array so this should always be present.
  - ARRAY_FORMAT_NORMAL: Mesh array contains normals.
  - ARRAY_FORMAT_TANGENT: Mesh array contains tangents.
  - ARRAY_FORMAT_COLOR: Mesh array contains colors.
  - ARRAY_FORMAT_TEX_UV: Mesh array contains UVs.
  - ARRAY_FORMAT_TEX_UV2: Mesh array contains second UV.
  - ARRAY_FORMAT_CUSTOM0: Mesh array contains custom channel index 0.
  - ARRAY_FORMAT_CUSTOM1: Mesh array contains custom channel index 1.
  - ARRAY_FORMAT_CUSTOM2: Mesh array contains custom channel index 2.
  - ARRAY_FORMAT_CUSTOM3: Mesh array contains custom channel index 3.
  - ARRAY_FORMAT_BONES: Mesh array contains bones.
  - ARRAY_FORMAT_WEIGHTS: Mesh array contains bone weights.
  - ARRAY_FORMAT_INDEX: Mesh array uses indices.
  - ARRAY_FORMAT_BLEND_SHAPE_MASK: Mask of mesh channels permitted in blend shapes.
  - ARRAY_FORMAT_CUSTOM_BASE: Shift of first custom channel.
  - ARRAY_FORMAT_CUSTOM_BITS: Number of format bits per custom channel. See `ArrayCustomFormat`.
  - ARRAY_FORMAT_CUSTOM0_SHIFT: Amount to shift `ArrayCustomFormat` for custom channel index 0.
  - ARRAY_FORMAT_CUSTOM1_SHIFT: Amount to shift `ArrayCustomFormat` for custom channel index 1.
  - ARRAY_FORMAT_CUSTOM2_SHIFT: Amount to shift `ArrayCustomFormat` for custom channel index 2.
  - ARRAY_FORMAT_CUSTOM3_SHIFT: Amount to shift `ArrayCustomFormat` for custom channel index 3.
  - ARRAY_FORMAT_CUSTOM_MASK: Mask of custom format bits per custom channel. Must be shifted by one of the SHIFT constants. See `ArrayCustomFormat`.
  - ARRAY_COMPRESS_FLAGS_BASE: Shift of first compress flag. Compress flags should be passed to `ArrayMesh.add_surface_from_arrays` and `SurfaceTool.commit`.
  - ARRAY_FLAG_USE_2D_VERTICES: Flag used to mark that the array contains 2D vertices.
  - ARRAY_FLAG_USE_DYNAMIC_UPDATE: Flag used to mark that the mesh data will use `GL_DYNAMIC_DRAW` on GLES. Unused on Vulkan.
  - ARRAY_FLAG_USE_8_BONE_WEIGHTS: Flag used to mark that the mesh contains up to 8 bone influences per vertex. This flag indicates that `ARRAY_BONES` and `ARRAY_WEIGHTS` elements will have double length.
  - ARRAY_FLAG_USES_EMPTY_VERTEX_ARRAY: Flag used to mark that the mesh intentionally contains no vertex array.
  - ARRAY_FLAG_COMPRESS_ATTRIBUTES: Flag used to mark that a mesh is using compressed attributes (vertices, normals, tangents, UVs). When this form of compression is enabled, vertex positions will be packed into an RGBA16UNORM attribute and scaled in the vertex shader. The normal and tangent will be packed into an RG16UNORM representing an axis, and a 16-bit float stored in the A-channel of the vertex. UVs will use 16-bit normalized floats instead of full 32-bit signed floats. When using this compression mode you must use either vertices, normals, and tangents or only vertices. You cannot use normals without tangents. Importers will automatically enable this compression if they can.
**BlendShapeMode:** BLEND_SHAPE_MODE_NORMALIZED=0, BLEND_SHAPE_MODE_RELATIVE=1
  - BLEND_SHAPE_MODE_NORMALIZED: Blend shapes are normalized.
  - BLEND_SHAPE_MODE_RELATIVE: Blend shapes are relative to base weight.

