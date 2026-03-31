## ArrayOccluder3D <- Occluder3D

ArrayOccluder3D stores an arbitrary 3D polygon shape that can be used by the engine's occlusion culling system. This is analogous to ArrayMesh, but for occluders. See OccluderInstance3D's documentation for instructions on setting up occlusion culling.

**Props:**
- indices: PackedInt32Array = PackedInt32Array()
- vertices: PackedVector3Array = PackedVector3Array()

- **indices**: The occluder's index position. Indices determine which points from the `vertices` array should be drawn, and in which order. **Note:** The occluder is always updated after setting this value. If creating occluders procedurally, consider using `set_arrays` instead to avoid updating the occluder twice when it's created.
- **vertices**: The occluder's vertex positions in local 3D coordinates. **Note:** The occluder is always updated after setting this value. If creating occluders procedurally, consider using `set_arrays` instead to avoid updating the occluder twice when it's created.

**Methods:**
- set_arrays(vertices: PackedVector3Array, indices: PackedInt32Array) - Sets `indices` and `vertices`, while updating the final occluder only once after both values are set.

