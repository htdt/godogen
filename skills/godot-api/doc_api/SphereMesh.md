## SphereMesh <- PrimitiveMesh

Class representing a spherical PrimitiveMesh.

**Props:**
- height: float = 1.0
- is_hemisphere: bool = false
- radial_segments: int = 64
- radius: float = 0.5
- rings: int = 32

- **height**: Full height of the sphere.
- **is_hemisphere**: If `true`, a hemisphere is created rather than a full sphere. **Note:** To get a regular hemisphere, the height and radius of the sphere must be equal.
- **radial_segments**: Number of radial segments on the sphere.
- **radius**: Radius of sphere.
- **rings**: Number of segments along the height of the sphere.

