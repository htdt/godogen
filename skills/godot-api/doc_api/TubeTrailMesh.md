## TubeTrailMesh <- PrimitiveMesh

TubeTrailMesh represents a straight tube-shaped mesh with variable width. The tube is composed of a number of cylindrical sections, each with the same `section_length` and number of `section_rings`. A `curve` is sampled along the total length of the tube, meaning that the curve determines the radius of the tube along its length. This primitive mesh is usually used for particle trails.

**Props:**
- cap_bottom: bool = true
- cap_top: bool = true
- curve: Curve
- radial_steps: int = 8
- radius: float = 0.5
- section_length: float = 0.2
- section_rings: int = 3
- sections: int = 5

- **cap_bottom**: If `true`, generates a cap at the bottom of the tube. This can be set to `false` to speed up generation and rendering when the cap is never seen by the camera.
- **cap_top**: If `true`, generates a cap at the top of the tube. This can be set to `false` to speed up generation and rendering when the cap is never seen by the camera.
- **curve**: Determines the radius of the tube along its length. The radius of a particular section ring is obtained by multiplying the baseline `radius` by the value of this curve at the given distance. For values smaller than `0`, the faces will be inverted. Should be a unit Curve.
- **radial_steps**: The number of sides on the tube. For example, a value of `5` means the tube will be pentagonal. Higher values result in a more detailed tube at the cost of performance.
- **radius**: The baseline radius of the tube. The radius of a particular section ring is obtained by multiplying this radius by the value of the `curve` at the given distance.
- **section_length**: The length of a section of the tube.
- **section_rings**: The number of rings in a section. The `curve` is sampled on each ring to determine its radius. Higher values result in a more detailed tube at the cost of performance.
- **sections**: The total number of sections on the tube.

