## MeshDataTool <- RefCounted

MeshDataTool provides access to individual vertices in a Mesh. It allows users to read and edit vertex data of meshes. It also creates an array of faces and edges. To use MeshDataTool, load a mesh with `create_from_surface`. When you are finished editing the data commit the data to a mesh with `commit_to_surface`. Below is an example of how MeshDataTool may be used. See also ArrayMesh, ImmediateMesh and SurfaceTool for procedural geometry generation. **Note:** Godot uses clockwise for front faces of triangle primitive modes.

**Methods:**
- clear() - Clears all data currently in MeshDataTool.
- commit_to_surface(mesh: ArrayMesh, compression_flags: int = 0) -> int - Adds a new surface to specified Mesh with edited data.
- create_from_surface(mesh: ArrayMesh, surface: int) -> int - Uses specified surface of given Mesh to populate data for MeshDataTool. Requires Mesh with primitive type `Mesh.PRIMITIVE_TRIANGLES`.
- get_edge_count() -> int - Returns the number of edges in this Mesh.
- get_edge_faces(idx: int) -> PackedInt32Array - Returns array of faces that touch given edge.
- get_edge_meta(idx: int) -> Variant - Returns meta information assigned to given edge.
- get_edge_vertex(idx: int, vertex: int) -> int - Returns the index of the specified `vertex` connected to the edge at index `idx`. `vertex` can only be `0` or `1`, as edges are composed of two vertices.
- get_face_count() -> int - Returns the number of faces in this Mesh.
- get_face_edge(idx: int, edge: int) -> int - Returns the edge associated with the face at index `idx`. `edge` argument must be either `0`, `1`, or `2` because a face only has three edges.
- get_face_meta(idx: int) -> Variant - Returns the metadata associated with the given face.
- get_face_normal(idx: int) -> Vector3 - Calculates and returns the face normal of the given face.
- get_face_vertex(idx: int, vertex: int) -> int - Returns the specified vertex index of the given face. `vertex` must be either `0`, `1`, or `2` because faces contain three vertices.
- get_format() -> int - Returns the Mesh's format as a combination of the `Mesh.ArrayFormat` flags. For example, a mesh containing both vertices and normals would return a format of `3` because `Mesh.ARRAY_FORMAT_VERTEX` is `1` and `Mesh.ARRAY_FORMAT_NORMAL` is `2`.
- get_material() -> Material - Returns the material assigned to the Mesh.
- get_vertex(idx: int) -> Vector3 - Returns the position of the given vertex.
- get_vertex_bones(idx: int) -> PackedInt32Array - Returns the bones of the given vertex.
- get_vertex_color(idx: int) -> Color - Returns the color of the given vertex.
- get_vertex_count() -> int - Returns the total number of vertices in Mesh.
- get_vertex_edges(idx: int) -> PackedInt32Array - Returns an array of edges that share the given vertex.
- get_vertex_faces(idx: int) -> PackedInt32Array - Returns an array of faces that share the given vertex.
- get_vertex_meta(idx: int) -> Variant - Returns the metadata associated with the given vertex.
- get_vertex_normal(idx: int) -> Vector3 - Returns the normal of the given vertex.
- get_vertex_tangent(idx: int) -> Plane - Returns the tangent of the given vertex.
- get_vertex_uv(idx: int) -> Vector2 - Returns the UV of the given vertex.
- get_vertex_uv2(idx: int) -> Vector2 - Returns the UV2 of the given vertex.
- get_vertex_weights(idx: int) -> PackedFloat32Array - Returns bone weights of the given vertex.
- set_edge_meta(idx: int, meta: Variant) - Sets the metadata of the given edge.
- set_face_meta(idx: int, meta: Variant) - Sets the metadata of the given face.
- set_material(material: Material) - Sets the material to be used by newly-constructed Mesh.
- set_vertex(idx: int, vertex: Vector3) - Sets the position of the given vertex.
- set_vertex_bones(idx: int, bones: PackedInt32Array) - Sets the bones of the given vertex.
- set_vertex_color(idx: int, color: Color) - Sets the color of the given vertex.
- set_vertex_meta(idx: int, meta: Variant) - Sets the metadata associated with the given vertex.
- set_vertex_normal(idx: int, normal: Vector3) - Sets the normal of the given vertex.
- set_vertex_tangent(idx: int, tangent: Plane) - Sets the tangent of the given vertex. **Note:** Even though `tangent` is a Plane, it does not directly represent the tangent plane. Its `Plane.x`, `Plane.y`, and `Plane.z` represent the tangent vector and `Plane.d` should be either `-1` or `1`. See also `Mesh.ARRAY_TANGENT`.
- set_vertex_uv(idx: int, uv: Vector2) - Sets the UV of the given vertex.
- set_vertex_uv2(idx: int, uv2: Vector2) - Sets the UV2 of the given vertex.
- set_vertex_weights(idx: int, weights: PackedFloat32Array) - Sets the bone weights of the given vertex.

