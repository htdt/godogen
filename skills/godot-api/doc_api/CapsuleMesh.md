## CapsuleMesh <- PrimitiveMesh

Class representing a capsule-shaped PrimitiveMesh.

**Props:**
- height: float = 2.0
- radial_segments: int = 64
- radius: float = 0.5
- rings: int = 8

- **height**: Total height of the capsule mesh (including the hemispherical ends). **Note:** The `height` of a capsule must be at least twice its `radius`. Otherwise, the capsule becomes a circle. If the `height` is less than twice the `radius`, the properties adjust to a valid value.
- **radial_segments**: Number of radial segments on the capsule mesh.
- **radius**: Radius of the capsule mesh. **Note:** The `radius` of a capsule cannot be greater than half of its `height`. Otherwise, the capsule becomes a circle. If the `radius` is greater than half of the `height`, the properties adjust to a valid value.
- **rings**: Number of rings along the height of the capsule.

