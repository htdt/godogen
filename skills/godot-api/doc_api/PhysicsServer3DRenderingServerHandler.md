## PhysicsServer3DRenderingServerHandler <- Object

**Methods:**
- _set_aabb(aabb: AABB) - Called by the PhysicsServer3D to set the bounding box for the SoftBody3D.
- _set_normal(vertex_id: int, normal: Vector3) - Called by the PhysicsServer3D to set the normal for the SoftBody3D vertex at the index specified by `vertex_id`. **Note:** The `normal` parameter used to be of type `const void*` prior to Godot 4.2.
- _set_vertex(vertex_id: int, vertex: Vector3) - Called by the PhysicsServer3D to set the position for the SoftBody3D vertex at the index specified by `vertex_id`. **Note:** The `vertex` parameter used to be of type `const void*` prior to Godot 4.2.
- set_aabb(aabb: AABB) - Sets the bounding box for the SoftBody3D.
- set_normal(vertex_id: int, normal: Vector3) - Sets the normal for the SoftBody3D vertex at the index specified by `vertex_id`.
- set_vertex(vertex_id: int, vertex: Vector3) - Sets the position for the SoftBody3D vertex at the index specified by `vertex_id`.

