## NavigationLink3D <- Node3D

A link between two positions on NavigationRegion3Ds that agents can be routed through. These positions can be on the same NavigationRegion3D or on two different ones. Links are useful to express navigation methods other than traveling along the surface of the navigation mesh, such as ziplines, teleporters, or gaps that can be jumped across.

**Props:**
- bidirectional: bool = true
- enabled: bool = true
- end_position: Vector3 = Vector3(0, 0, 0)
- enter_cost: float = 0.0
- navigation_layers: int = 1
- start_position: Vector3 = Vector3(0, 0, 0)
- travel_cost: float = 1.0

- **bidirectional**: Whether this link can be traveled in both directions or only from `start_position` to `end_position`.
- **enabled**: Whether this link is currently active. If `false`, `NavigationServer3D.map_get_path` will ignore this link.
- **end_position**: Ending position of the link. This position will search out the nearest polygon in the navigation mesh to attach to. The distance the link will search is controlled by `NavigationServer3D.map_set_link_connection_radius`.
- **enter_cost**: When pathfinding enters this link from another regions navigation mesh the `enter_cost` value is added to the path distance for determining the shortest path.
- **navigation_layers**: A bitfield determining all navigation layers the link belongs to. These navigation layers will be checked when requesting a path with `NavigationServer3D.map_get_path`.
- **start_position**: Starting position of the link. This position will search out the nearest polygon in the navigation mesh to attach to. The distance the link will search is controlled by `NavigationServer3D.map_set_link_connection_radius`.
- **travel_cost**: When pathfinding moves along the link the traveled distance is multiplied with `travel_cost` for determining the shortest path.

**Methods:**
- get_global_end_position() -> Vector3 - Returns the `end_position` that is relative to the link as a global position.
- get_global_start_position() -> Vector3 - Returns the `start_position` that is relative to the link as a global position.
- get_navigation_layer_value(layer_number: int) -> bool - Returns whether or not the specified layer of the `navigation_layers` bitmask is enabled, given a `layer_number` between 1 and 32.
- get_navigation_map() -> RID - Returns the current navigation map RID used by this link.
- get_rid() -> RID - Returns the RID of this link on the NavigationServer3D.
- set_global_end_position(position: Vector3) - Sets the `end_position` that is relative to the link from a global `position`.
- set_global_start_position(position: Vector3) - Sets the `start_position` that is relative to the link from a global `position`.
- set_navigation_layer_value(layer_number: int, value: bool) - Based on `value`, enables or disables the specified layer in the `navigation_layers` bitmask, given a `layer_number` between 1 and 32.
- set_navigation_map(navigation_map: RID) - Sets the RID of the navigation map this link should use. By default the link will automatically join the World3D default navigation map so this function is only required to override the default map.

