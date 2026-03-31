## MeshConvexDecompositionSettings <- RefCounted

Parameters to be used with a Mesh convex decomposition operation.

**Props:**
- convex_hull_approximation: bool = true
- convex_hull_downsampling: int = 4
- max_concavity: float = 1.0
- max_convex_hulls: int = 1
- max_num_vertices_per_convex_hull: int = 32
- min_volume_per_convex_hull: float = 0.0001
- mode: int (MeshConvexDecompositionSettings.Mode) = 0
- normalize_mesh: bool = false
- plane_downsampling: int = 4
- project_hull_vertices: bool = true
- resolution: int = 10000
- revolution_axes_clipping_bias: float = 0.05
- symmetry_planes_clipping_bias: float = 0.05

- **convex_hull_approximation**: If `true`, uses approximation for computing convex hulls.
- **convex_hull_downsampling**: Controls the precision of the convex-hull generation process during the clipping plane selection stage. Ranges from `1` to `16`.
- **max_concavity**: Maximum concavity. Ranges from `0.0` to `1.0`.
- **max_convex_hulls**: The maximum number of convex hulls to produce from the merge operation.
- **max_num_vertices_per_convex_hull**: Controls the maximum number of triangles per convex-hull. Ranges from `4` to `1024`.
- **min_volume_per_convex_hull**: Controls the adaptive sampling of the generated convex-hulls. Ranges from `0.0` to `0.01`.
- **mode**: Mode for the approximate convex decomposition.
- **normalize_mesh**: If `true`, normalizes the mesh before applying the convex decomposition.
- **plane_downsampling**: Controls the granularity of the search for the "best" clipping plane. Ranges from `1` to `16`.
- **project_hull_vertices**: If `true`, projects output convex hull vertices onto the original source mesh to increase floating-point accuracy of the results.
- **resolution**: Maximum number of voxels generated during the voxelization stage.
- **revolution_axes_clipping_bias**: Controls the bias toward clipping along revolution axes. Ranges from `0.0` to `1.0`.
- **symmetry_planes_clipping_bias**: Controls the bias toward clipping along symmetry planes. Ranges from `0.0` to `1.0`.

**Enums:**
**Mode:** CONVEX_DECOMPOSITION_MODE_VOXEL=0, CONVEX_DECOMPOSITION_MODE_TETRAHEDRON=1
  - CONVEX_DECOMPOSITION_MODE_VOXEL: Constant for voxel-based approximate convex decomposition.
  - CONVEX_DECOMPOSITION_MODE_TETRAHEDRON: Constant for tetrahedron-based approximate convex decomposition.

