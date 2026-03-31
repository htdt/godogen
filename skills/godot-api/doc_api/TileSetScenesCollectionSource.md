## TileSetScenesCollectionSource <- TileSetSource

When placed on a TileMapLayer, tiles from TileSetScenesCollectionSource will automatically instantiate an associated scene at the cell's position in the TileMapLayer. Scenes are instantiated as children of the TileMapLayer after it enters the tree, at the end of the frame (their creation is deferred). If you add/remove a scene tile in the TileMapLayer that is already inside the tree, the TileMapLayer will automatically instantiate/free the scene accordingly. **Note:** Scene tiles all occupy one tile slot and instead use alternate tile ID to identify scene index. `TileSetSource.get_tiles_count` will always return `1`. Use `get_scene_tiles_count` to get a number of scenes in a TileSetScenesCollectionSource. Use this code if you want to find the scene path at a given tile in TileMapLayer:

**Methods:**
- create_scene_tile(packed_scene: PackedScene, id_override: int = -1) -> int - Creates a scene-based tile out of the given scene. Returns a newly generated unique ID.
- get_next_scene_tile_id() -> int - Returns the scene ID a following call to `create_scene_tile` would return.
- get_scene_tile_display_placeholder(id: int) -> bool - Returns whether the scene tile with `id` displays a placeholder in the editor.
- get_scene_tile_id(index: int) -> int - Returns the scene tile ID of the scene tile at `index`.
- get_scene_tile_scene(id: int) -> PackedScene - Returns the PackedScene resource of scene tile with `id`.
- get_scene_tiles_count() -> int - Returns the number or scene tiles this TileSet source has.
- has_scene_tile_id(id: int) -> bool - Returns whether this TileSet source has a scene tile with `id`.
- remove_scene_tile(id: int) - Remove the scene tile with `id`.
- set_scene_tile_display_placeholder(id: int, display_placeholder: bool) - Sets whether or not the scene tile with `id` should display a placeholder in the editor. This might be useful for scenes that are not visible.
- set_scene_tile_id(id: int, new_id: int) - Changes a scene tile's ID from `id` to `new_id`. This will fail if there is already a tile with an ID equal to `new_id`.
- set_scene_tile_scene(id: int, packed_scene: PackedScene) - Assigns a PackedScene resource to the scene tile with `id`. This will fail if the scene does not extend CanvasItem, as positioning properties are needed to place the scene on the TileMapLayer.

