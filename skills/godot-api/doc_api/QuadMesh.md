## QuadMesh <- PlaneMesh

Class representing a square PrimitiveMesh. This flat mesh does not have a thickness. By default, this mesh is aligned on the X and Y axes; this rotation is more suited for use with billboarded materials. A QuadMesh is equivalent to a PlaneMesh except its default `PlaneMesh.orientation` is `PlaneMesh.FACE_Z`.

**Props:**
- orientation: int (PlaneMesh.Orientation) = 2
- size: Vector2 = Vector2(1, 1)


