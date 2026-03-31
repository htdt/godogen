## TileSetSource <- Resource

Exposes a set of tiles for a TileSet resource. Tiles in a source are indexed with two IDs, coordinates ID (of type Vector2i) and an alternative ID (of type int), named according to their use in the TileSetAtlasSource class. Depending on the TileSet source type, those IDs might have restrictions on their values, this is why the base TileSetSource class only exposes getters for them. You can iterate over all tiles exposed by a TileSetSource by first iterating over coordinates IDs using `get_tiles_count` and `get_tile_id`, then over alternative IDs using `get_alternative_tiles_count` and `get_alternative_tile_id`. **Warning:** TileSetSource can only be added to one TileSet at the same time. Calling `TileSet.add_source` on a second TileSet will remove the source from the first one.

**Methods:**
- get_alternative_tile_id(atlas_coords: Vector2i, index: int) -> int - Returns the alternative ID for the tile with coordinates ID `atlas_coords` at index `index`.
- get_alternative_tiles_count(atlas_coords: Vector2i) -> int - Returns the number of alternatives tiles for the coordinates ID `atlas_coords`. For TileSetAtlasSource, this always return at least 1, as the base tile with ID 0 is always part of the alternatives list. Returns -1 if there is not tile at the given coords.
- get_tile_id(index: int) -> Vector2i - Returns the tile coordinates ID of the tile with index `index`.
- get_tiles_count() -> int - Returns how many tiles this atlas source defines (not including alternative tiles).
- has_alternative_tile(atlas_coords: Vector2i, alternative_tile: int) -> bool - Returns if the base tile at coordinates `atlas_coords` has an alternative with ID `alternative_tile`.
- has_tile(atlas_coords: Vector2i) -> bool - Returns if this atlas has a tile with coordinates ID `atlas_coords`.

