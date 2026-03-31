## TileData <- Object

TileData object represents a single tile in a TileSet. It is usually edited using the tileset editor, but it can be modified at runtime using `TileMapLayer._tile_data_runtime_update`.

**Props:**
- flip_h: bool = false
- flip_v: bool = false
- material: Material
- modulate: Color = Color(1, 1, 1, 1)
- probability: float = 1.0
- terrain: int = -1
- terrain_set: int = -1
- texture_origin: Vector2i = Vector2i(0, 0)
- transpose: bool = false
- y_sort_origin: int = 0
- z_index: int = 0

- **flip_h**: If `true`, the tile will have its texture flipped horizontally.
- **flip_v**: If `true`, the tile will have its texture flipped vertically.
- **material**: The Material to use for this TileData. This can be a CanvasItemMaterial to use the default shader, or a ShaderMaterial to use a custom shader.
- **modulate**: Color modulation of the tile.
- **probability**: Relative probability of this tile being selected when drawing a pattern of random tiles.
- **terrain**: ID of the terrain from the terrain set that the tile uses.
- **terrain_set**: ID of the terrain set that the tile uses.
- **texture_origin**: Offsets the position of where the tile is drawn.
- **transpose**: If `true`, the tile will display transposed, i.e. with horizontal and vertical texture UVs swapped.
- **y_sort_origin**: Vertical point of the tile used for determining y-sorted order.
- **z_index**: Ordering index of this tile, relative to TileMapLayer.

**Methods:**
- add_collision_polygon(layer_id: int) - Adds a collision polygon to the tile on the given TileSet physics layer.
- add_occluder_polygon(layer_id: int) - Adds an occlusion polygon to the tile on the TileSet occlusion layer with index `layer_id`.
- get_collision_polygon_one_way_margin(layer_id: int, polygon_index: int) -> float - Returns the one-way margin (for one-way platforms) of the polygon at index `polygon_index` for TileSet physics layer with index `layer_id`.
- get_collision_polygon_points(layer_id: int, polygon_index: int) -> PackedVector2Array - Returns the points of the polygon at index `polygon_index` for TileSet physics layer with index `layer_id`.
- get_collision_polygons_count(layer_id: int) -> int - Returns how many polygons the tile has for TileSet physics layer with index `layer_id`.
- get_constant_angular_velocity(layer_id: int) -> float - Returns the constant angular velocity applied to objects colliding with this tile.
- get_constant_linear_velocity(layer_id: int) -> Vector2 - Returns the constant linear velocity applied to objects colliding with this tile.
- get_custom_data(layer_name: String) -> Variant - Returns the custom data value for custom data layer named `layer_name`. To check if a custom data layer exists, use `has_custom_data`.
- get_custom_data_by_layer_id(layer_id: int) -> Variant - Returns the custom data value for custom data layer with index `layer_id`.
- get_navigation_polygon(layer_id: int, flip_h: bool = false, flip_v: bool = false, transpose: bool = false) -> NavigationPolygon - Returns the navigation polygon of the tile for the TileSet navigation layer with index `layer_id`. `flip_h`, `flip_v`, and `transpose` allow transforming the returned polygon.
- get_occluder(layer_id: int, flip_h: bool = false, flip_v: bool = false, transpose: bool = false) -> OccluderPolygon2D - Returns the occluder polygon of the tile for the TileSet occlusion layer with index `layer_id`. `flip_h`, `flip_v`, and `transpose` allow transforming the returned polygon.
- get_occluder_polygon(layer_id: int, polygon_index: int, flip_h: bool = false, flip_v: bool = false, transpose: bool = false) -> OccluderPolygon2D - Returns the occluder polygon at index `polygon_index` from the TileSet occlusion layer with index `layer_id`. The `flip_h`, `flip_v`, and `transpose` parameters can be `true` to transform the returned polygon.
- get_occluder_polygons_count(layer_id: int) -> int - Returns the number of occluder polygons of the tile in the TileSet occlusion layer with index `layer_id`.
- get_terrain_peering_bit(peering_bit: int) -> int - Returns the tile's terrain bit for the given `peering_bit` direction. To check that a direction is valid, use `is_valid_terrain_peering_bit`.
- has_custom_data(layer_name: String) -> bool - Returns whether there exists a custom data layer named `layer_name`.
- is_collision_polygon_one_way(layer_id: int, polygon_index: int) -> bool - Returns whether one-way collisions are enabled for the polygon at index `polygon_index` for TileSet physics layer with index `layer_id`.
- is_valid_terrain_peering_bit(peering_bit: int) -> bool - Returns whether the given `peering_bit` direction is valid for this tile.
- remove_collision_polygon(layer_id: int, polygon_index: int) - Removes the polygon at index `polygon_index` for TileSet physics layer with index `layer_id`.
- remove_occluder_polygon(layer_id: int, polygon_index: int) - Removes the polygon at index `polygon_index` for TileSet occlusion layer with index `layer_id`.
- set_collision_polygon_one_way(layer_id: int, polygon_index: int, one_way: bool) - Enables/disables one-way collisions on the polygon at index `polygon_index` for TileSet physics layer with index `layer_id`.
- set_collision_polygon_one_way_margin(layer_id: int, polygon_index: int, one_way_margin: float) - Sets the one-way margin (for one-way platforms) of the polygon at index `polygon_index` for TileSet physics layer with index `layer_id`.
- set_collision_polygon_points(layer_id: int, polygon_index: int, polygon: PackedVector2Array) - Sets the points of the polygon at index `polygon_index` for TileSet physics layer with index `layer_id`.
- set_collision_polygons_count(layer_id: int, polygons_count: int) - Sets the polygons count for TileSet physics layer with index `layer_id`.
- set_constant_angular_velocity(layer_id: int, velocity: float) - Sets the constant angular velocity. This does not rotate the tile. This angular velocity is applied to objects colliding with this tile.
- set_constant_linear_velocity(layer_id: int, velocity: Vector2) - Sets the constant linear velocity. This does not move the tile. This linear velocity is applied to objects colliding with this tile. This is useful to create conveyor belts.
- set_custom_data(layer_name: String, value: Variant) - Sets the tile's custom data value for the TileSet custom data layer with name `layer_name`.
- set_custom_data_by_layer_id(layer_id: int, value: Variant) - Sets the tile's custom data value for the TileSet custom data layer with index `layer_id`.
- set_navigation_polygon(layer_id: int, navigation_polygon: NavigationPolygon) - Sets the navigation polygon for the TileSet navigation layer with index `layer_id`.
- set_occluder(layer_id: int, occluder_polygon: OccluderPolygon2D) - Sets the occluder for the TileSet occlusion layer with index `layer_id`.
- set_occluder_polygon(layer_id: int, polygon_index: int, polygon: OccluderPolygon2D) - Sets the occluder for polygon with index `polygon_index` in the TileSet occlusion layer with index `layer_id`.
- set_occluder_polygons_count(layer_id: int, polygons_count: int) - Sets the occluder polygon count in the TileSet occlusion layer with index `layer_id`.
- set_terrain_peering_bit(peering_bit: int, terrain: int) - Sets the tile's terrain bit for the given `peering_bit` direction. To check that a direction is valid, use `is_valid_terrain_peering_bit`.

**Signals:**
- changed - Emitted when any of the properties are changed.

