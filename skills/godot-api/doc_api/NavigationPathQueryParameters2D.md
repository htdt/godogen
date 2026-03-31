## NavigationPathQueryParameters2D <- RefCounted

By changing various properties of this object, such as the start and target position, you can configure path queries to the NavigationServer2D.

**Props:**
- excluded_regions: RID[] = []
- included_regions: RID[] = []
- map: RID = RID()
- metadata_flags: int (NavigationPathQueryParameters2D.PathMetadataFlags) = 7
- navigation_layers: int = 1
- path_postprocessing: int (NavigationPathQueryParameters2D.PathPostProcessing) = 0
- path_return_max_length: float = 0.0
- path_return_max_radius: float = 0.0
- path_search_max_distance: float = 0.0
- path_search_max_polygons: int = 4096
- pathfinding_algorithm: int (NavigationPathQueryParameters2D.PathfindingAlgorithm) = 0
- simplify_epsilon: float = 0.0
- simplify_path: bool = false
- start_position: Vector2 = Vector2(0, 0)
- target_position: Vector2 = Vector2(0, 0)

- **excluded_regions**: The list of region RIDs that will be excluded from the path query. Use `NavigationRegion2D.get_rid` to get the RID associated with a NavigationRegion2D node. **Note:** The returned array is copied and any changes to it will not update the original property value. To update the value you need to modify the returned array, and then set it to the property again.
- **included_regions**: The list of region RIDs that will be included by the path query. Use `NavigationRegion2D.get_rid` to get the RID associated with a NavigationRegion2D node. If left empty all regions are included. If a region ends up being both included and excluded at the same time it will be excluded. **Note:** The returned array is copied and any changes to it will not update the original property value. To update the value you need to modify the returned array, and then set it to the property again.
- **map**: The navigation map RID used in the path query.
- **metadata_flags**: Additional information to include with the navigation path.
- **navigation_layers**: The navigation layers the query will use (as a bitmask).
- **path_postprocessing**: The path postprocessing applied to the raw path corridor found by the `pathfinding_algorithm`.
- **path_return_max_length**: The maximum allowed length of the returned path in world units. A path will be clipped when going over this length. A value of `0` or below counts as disabled.
- **path_return_max_radius**: The maximum allowed radius in world units that the returned path can be from the path start. The path will be clipped when going over this radius. A value of `0` or below counts as disabled. **Note:** This will perform a circle shaped clip operation on the path with the first path position being the circle's center position.
- **path_search_max_distance**: The maximum distance a searched polygon can be away from the start polygon before the pathfinding cancels the search for a path to the (possibly unreachable or very far away) target position polygon. In this case the pathfinding resets and builds a path from the start polygon to the polygon that was found closest to the target position so far. A value of `0` or below counts as unlimited. In case of unlimited the pathfinding will search all polygons connected with the start polygon until either the target position polygon is found or all available polygon search options are exhausted.
- **path_search_max_polygons**: The maximum number of polygons that are searched before the pathfinding cancels the search for a path to the (possibly unreachable or very far away) target position polygon. In this case the pathfinding resets and builds a path from the start polygon to the polygon that was found closest to the target position so far. A value of `0` or below counts as unlimited. In case of unlimited the pathfinding will search all polygons connected with the start polygon until either the target position polygon is found or all available polygon search options are exhausted.
- **pathfinding_algorithm**: The pathfinding algorithm used in the path query.
- **simplify_epsilon**: The path simplification amount in worlds units.
- **simplify_path**: If `true` a simplified version of the path will be returned with less critical path points removed. The simplification amount is controlled by `simplify_epsilon`. The simplification uses a variant of Ramer-Douglas-Peucker algorithm for curve point decimation. Path simplification can be helpful to mitigate various path following issues that can arise with certain agent types and script behaviors. E.g. "steering" agents or avoidance in "open fields".
- **start_position**: The pathfinding start position in global coordinates.
- **target_position**: The pathfinding target position in global coordinates.

**Enums:**
**PathfindingAlgorithm:** PATHFINDING_ALGORITHM_ASTAR=0
  - PATHFINDING_ALGORITHM_ASTAR: The path query uses the default A* pathfinding algorithm.
**PathPostProcessing:** PATH_POSTPROCESSING_CORRIDORFUNNEL=0, PATH_POSTPROCESSING_EDGECENTERED=1, PATH_POSTPROCESSING_NONE=2
  - PATH_POSTPROCESSING_CORRIDORFUNNEL: Applies a funnel algorithm to the raw path corridor found by the pathfinding algorithm. This will result in the shortest path possible inside the path corridor. This postprocessing very much depends on the navigation mesh polygon layout and the created corridor. Especially tile- or gridbased layouts can face artificial corners with diagonal movement due to a jagged path corridor imposed by the cell shapes.
  - PATH_POSTPROCESSING_EDGECENTERED: Centers every path position in the middle of the traveled navigation mesh polygon edge. This creates better paths for tile- or gridbased layouts that restrict the movement to the cells center.
  - PATH_POSTPROCESSING_NONE: Applies no postprocessing and returns the raw path corridor as found by the pathfinding algorithm.
**PathMetadataFlags:** PATH_METADATA_INCLUDE_NONE=0, PATH_METADATA_INCLUDE_TYPES=1, PATH_METADATA_INCLUDE_RIDS=2, PATH_METADATA_INCLUDE_OWNERS=4, PATH_METADATA_INCLUDE_ALL=7
  - PATH_METADATA_INCLUDE_NONE: Don't include any additional metadata about the returned path.
  - PATH_METADATA_INCLUDE_TYPES: Include the type of navigation primitive (region or link) that each point of the path goes through.
  - PATH_METADATA_INCLUDE_RIDS: Include the RIDs of the regions and links that each point of the path goes through.
  - PATH_METADATA_INCLUDE_OWNERS: Include the `ObjectID`s of the Objects which manage the regions and links each point of the path goes through.
  - PATH_METADATA_INCLUDE_ALL: Include all available metadata about the returned path.

