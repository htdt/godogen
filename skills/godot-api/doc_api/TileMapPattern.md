## TileMapPattern <- Resource

This resource holds a set of cells to help bulk manipulations of TileMap. A pattern always starts at the `(0, 0)` coordinates and cannot have cells with negative coordinates.

**Methods:**
- get_cell_alternative_tile(coords: Vector2i) -> int - Returns the tile alternative ID of the cell at `coords`.
- get_cell_atlas_coords(coords: Vector2i) -> Vector2i - Returns the tile atlas coordinates ID of the cell at `coords`.
- get_cell_source_id(coords: Vector2i) -> int - Returns the tile source ID of the cell at `coords`.
- get_size() -> Vector2i - Returns the size, in cells, of the pattern.
- get_used_cells() -> Vector2i[] - Returns the list of used cell coordinates in the pattern.
- has_cell(coords: Vector2i) -> bool - Returns whether the pattern has a tile at the given coordinates.
- is_empty() -> bool - Returns whether the pattern is empty or not.
- remove_cell(coords: Vector2i, update_size: bool) - Remove the cell at the given coordinates.
- set_cell(coords: Vector2i, source_id: int = -1, atlas_coords: Vector2i = Vector2i(-1, -1), alternative_tile: int = -1) - Sets the tile identifiers for the cell at coordinates `coords`. See `TileMap.set_cell`.
- set_size(size: Vector2i) - Sets the size of the pattern.

