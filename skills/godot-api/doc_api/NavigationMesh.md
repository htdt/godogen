## NavigationMesh <- Resource

A navigation mesh is a collection of polygons that define which areas of an environment are traversable to aid agents in pathfinding through complicated spaces.

**Props:**
- agent_height: float = 1.5
- agent_max_climb: float = 0.25
- agent_max_slope: float = 45.0
- agent_radius: float = 0.5
- border_size: float = 0.0
- cell_height: float = 0.25
- cell_size: float = 0.25
- detail_sample_distance: float = 6.0
- detail_sample_max_error: float = 1.0
- edge_max_error: float = 1.3
- edge_max_length: float = 0.0
- filter_baking_aabb: AABB = AABB(0, 0, 0, 0, 0, 0)
- filter_baking_aabb_offset: Vector3 = Vector3(0, 0, 0)
- filter_ledge_spans: bool = false
- filter_low_hanging_obstacles: bool = false
- filter_walkable_low_height_spans: bool = false
- geometry_collision_mask: int = 4294967295
- geometry_parsed_geometry_type: int (NavigationMesh.ParsedGeometryType) = 2
- geometry_source_geometry_mode: int (NavigationMesh.SourceGeometryMode) = 0
- geometry_source_group_name: StringName = &"navigation_mesh_source_group"
- region_merge_size: float = 20.0
- region_min_size: float = 2.0
- sample_partition_type: int (NavigationMesh.SamplePartitionType) = 0
- vertices_per_polygon: float = 6.0

- **agent_height**: The minimum floor to ceiling height that will still allow the floor area to be considered walkable. **Note:** While baking, this value will be rounded up to the nearest multiple of `cell_height`.
- **agent_max_climb**: The minimum ledge height that is considered to still be traversable. **Note:** While baking, this value will be rounded down to the nearest multiple of `cell_height`.
- **agent_max_slope**: The maximum slope that is considered walkable, in degrees.
- **agent_radius**: The distance to erode/shrink the walkable area of the heightfield away from obstructions. **Note:** While baking, this value will be rounded up to the nearest multiple of `cell_size`. **Note:** The radius must be equal or higher than `0.0`. If the radius is `0.0`, it won't be possible to fix invalid outline overlaps and other precision errors during the baking process. As a result, some obstacles may be excluded incorrectly from the final navigation mesh, or may delete the navigation mesh's polygons.
- **border_size**: The size of the non-navigable border around the bake bounding area. In conjunction with the `filter_baking_aabb` and a `edge_max_error` value at `1.0` or below the border size can be used to bake tile aligned navigation meshes without the tile edges being shrunk by `agent_radius`. **Note:** If this value is not `0.0`, it will be rounded up to the nearest multiple of `cell_size` during baking.
- **cell_height**: The cell height used to rasterize the navigation mesh vertices on the Y axis. Must match with the cell height on the navigation map.
- **cell_size**: The cell size used to rasterize the navigation mesh vertices on the XZ plane. Must match with the cell size on the navigation map.
- **detail_sample_distance**: The sampling distance to use when generating the detail mesh, in cell unit.
- **detail_sample_max_error**: The maximum distance the detail mesh surface should deviate from heightfield, in cell unit.
- **edge_max_error**: The maximum distance a simplified contour's border edges should deviate the original raw contour.
- **edge_max_length**: The maximum allowed length for contour edges along the border of the mesh. A value of `0.0` disables this feature. **Note:** While baking, this value will be rounded up to the nearest multiple of `cell_size`.
- **filter_baking_aabb**: If the baking AABB has a volume the navigation mesh baking will be restricted to its enclosing area.
- **filter_baking_aabb_offset**: The position offset applied to the `filter_baking_aabb` AABB.
- **filter_ledge_spans**: If `true`, marks spans that are ledges as non-walkable.
- **filter_low_hanging_obstacles**: If `true`, marks non-walkable spans as walkable if their maximum is within `agent_max_climb` of a walkable neighbor.
- **filter_walkable_low_height_spans**: If `true`, marks walkable spans as not walkable if the clearance above the span is less than `agent_height`.
- **geometry_collision_mask**: The physics layers to scan for static colliders. Only used when `geometry_parsed_geometry_type` is `PARSED_GEOMETRY_STATIC_COLLIDERS` or `PARSED_GEOMETRY_BOTH`.
- **geometry_parsed_geometry_type**: Determines which type of nodes will be parsed as geometry.
- **geometry_source_geometry_mode**: The source of the geometry used when baking.
- **geometry_source_group_name**: The name of the group to scan for geometry. Only used when `geometry_source_geometry_mode` is `SOURCE_GEOMETRY_GROUPS_WITH_CHILDREN` or `SOURCE_GEOMETRY_GROUPS_EXPLICIT`.
- **region_merge_size**: Any regions with a size smaller than this will be merged with larger regions if possible. **Note:** This value will be squared to calculate the number of cells. For example, a value of 20 will set the number of cells to 400.
- **region_min_size**: The minimum size of a region for it to be created. **Note:** This value will be squared to calculate the minimum number of cells allowed to form isolated island areas. For example, a value of 8 will set the number of cells to 64.
- **sample_partition_type**: Partitioning algorithm for creating the navigation mesh polys.
- **vertices_per_polygon**: The maximum number of vertices allowed for polygons generated during the contour to polygon conversion process.

**Methods:**
- add_polygon(polygon: PackedInt32Array) - Adds a polygon using the indices of the vertices you get when calling `get_vertices`.
- clear() - Clears the internal arrays for vertices and polygon indices.
- clear_polygons() - Clears the array of polygons, but it doesn't clear the array of vertices.
- create_from_mesh(mesh: Mesh) - Initializes the navigation mesh by setting the vertices and indices according to a Mesh. **Note:** The given `mesh` must be of type `Mesh.PRIMITIVE_TRIANGLES` and have an index array.
- get_collision_mask_value(layer_number: int) -> bool - Returns whether or not the specified layer of the `geometry_collision_mask` is enabled, given a `layer_number` between 1 and 32.
- get_polygon(idx: int) -> PackedInt32Array - Returns a PackedInt32Array containing the indices of the vertices of a created polygon.
- get_polygon_count() -> int - Returns the number of polygons in the navigation mesh.
- get_vertices() -> PackedVector3Array - Returns a PackedVector3Array containing all the vertices being used to create the polygons.
- set_collision_mask_value(layer_number: int, value: bool) - Based on `value`, enables or disables the specified layer in the `geometry_collision_mask`, given a `layer_number` between 1 and 32.
- set_vertices(vertices: PackedVector3Array) - Sets the vertices that can be then indexed to create polygons with the `add_polygon` method.

**Enums:**
**SamplePartitionType:** SAMPLE_PARTITION_WATERSHED=0, SAMPLE_PARTITION_MONOTONE=1, SAMPLE_PARTITION_LAYERS=2, SAMPLE_PARTITION_MAX=3
  - SAMPLE_PARTITION_WATERSHED: Watershed partitioning. Generally the best choice if you precompute the navigation mesh, use this if you have large open areas.
  - SAMPLE_PARTITION_MONOTONE: Monotone partitioning. Use this if you want fast navigation mesh generation.
  - SAMPLE_PARTITION_LAYERS: Layer partitioning. Good choice to use for tiled navigation mesh with medium and small sized tiles.
  - SAMPLE_PARTITION_MAX: Represents the size of the `SamplePartitionType` enum.
**ParsedGeometryType:** PARSED_GEOMETRY_MESH_INSTANCES=0, PARSED_GEOMETRY_STATIC_COLLIDERS=1, PARSED_GEOMETRY_BOTH=2, PARSED_GEOMETRY_MAX=3
  - PARSED_GEOMETRY_MESH_INSTANCES: Parses mesh instances as geometry. This includes MeshInstance3D, CSGShape3D, and GridMap nodes.
  - PARSED_GEOMETRY_STATIC_COLLIDERS: Parses StaticBody3D colliders as geometry. The collider should be in any of the layers specified by `geometry_collision_mask`.
  - PARSED_GEOMETRY_BOTH: Both `PARSED_GEOMETRY_MESH_INSTANCES` and `PARSED_GEOMETRY_STATIC_COLLIDERS`.
  - PARSED_GEOMETRY_MAX: Represents the size of the `ParsedGeometryType` enum.
**SourceGeometryMode:** SOURCE_GEOMETRY_ROOT_NODE_CHILDREN=0, SOURCE_GEOMETRY_GROUPS_WITH_CHILDREN=1, SOURCE_GEOMETRY_GROUPS_EXPLICIT=2, SOURCE_GEOMETRY_MAX=3
  - SOURCE_GEOMETRY_ROOT_NODE_CHILDREN: Scans the child nodes of the root node recursively for geometry.
  - SOURCE_GEOMETRY_GROUPS_WITH_CHILDREN: Scans nodes in a group and their child nodes recursively for geometry. The group is specified by `geometry_source_group_name`.
  - SOURCE_GEOMETRY_GROUPS_EXPLICIT: Uses nodes in a group for geometry. The group is specified by `geometry_source_group_name`.
  - SOURCE_GEOMETRY_MAX: Represents the size of the `SourceGeometryMode` enum.

