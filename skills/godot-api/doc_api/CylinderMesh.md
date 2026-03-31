## CylinderMesh <- PrimitiveMesh

Class representing a cylindrical PrimitiveMesh. This class can be used to create cones by setting either the `top_radius` or `bottom_radius` properties to `0.0`.

**Props:**
- bottom_radius: float = 0.5
- cap_bottom: bool = true
- cap_top: bool = true
- height: float = 2.0
- radial_segments: int = 64
- rings: int = 4
- top_radius: float = 0.5

- **bottom_radius**: Bottom radius of the cylinder. If set to `0.0`, the bottom faces will not be generated, resulting in a conic shape. See also `cap_bottom`.
- **cap_bottom**: If `true`, generates a cap at the bottom of the cylinder. This can be set to `false` to speed up generation and rendering when the cap is never seen by the camera. See also `bottom_radius`. **Note:** If `bottom_radius` is `0.0`, cap generation is always skipped even if `cap_bottom` is `true`.
- **cap_top**: If `true`, generates a cap at the top of the cylinder. This can be set to `false` to speed up generation and rendering when the cap is never seen by the camera. See also `top_radius`. **Note:** If `top_radius` is `0.0`, cap generation is always skipped even if `cap_top` is `true`.
- **height**: Full height of the cylinder.
- **radial_segments**: Number of radial segments on the cylinder. Higher values result in a more detailed cylinder/cone at the cost of performance.
- **rings**: Number of edge rings along the height of the cylinder. Changing `rings` does not have any visual impact unless a shader or procedural mesh tool is used to alter the vertex data. Higher values result in more subdivisions, which can be used to create smoother-looking effects with shaders or procedural mesh tools (at the cost of performance). When not altering the vertex data using a shader or procedural mesh tool, `rings` should be kept to its default value.
- **top_radius**: Top radius of the cylinder. If set to `0.0`, the top faces will not be generated, resulting in a conic shape. See also `cap_top`.

