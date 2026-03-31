## PlaneMesh <- PrimitiveMesh

Class representing a planar PrimitiveMesh. This flat mesh does not have a thickness. By default, this mesh is aligned on the X and Z axes; this default rotation isn't suited for use with billboarded materials. For billboarded materials, change `orientation` to `FACE_Z`. **Note:** When using a large textured PlaneMesh (e.g. as a floor), you may stumble upon UV jittering issues depending on the camera angle. To solve this, increase `subdivide_depth` and `subdivide_width` until you no longer notice UV jittering.

**Props:**
- center_offset: Vector3 = Vector3(0, 0, 0)
- orientation: int (PlaneMesh.Orientation) = 1
- size: Vector2 = Vector2(2, 2)
- subdivide_depth: int = 0
- subdivide_width: int = 0

- **center_offset**: Offset of the generated plane. Useful for particles.
- **orientation**: Direction that the PlaneMesh is facing.
- **size**: Size of the generated plane.
- **subdivide_depth**: Number of subdivision along the Z axis.
- **subdivide_width**: Number of subdivision along the X axis.

**Enums:**
**Orientation:** FACE_X=0, FACE_Y=1, FACE_Z=2
  - FACE_X: PlaneMesh will face the positive X-axis.
  - FACE_Y: PlaneMesh will face the positive Y-axis. This matches the behavior of the PlaneMesh in Godot 3.x.
  - FACE_Z: PlaneMesh will face the positive Z-axis. This matches the behavior of the QuadMesh in Godot 3.x.

