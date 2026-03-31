## MeshLibrary <- Resource

A library of meshes. Contains a list of Mesh resources, each with a name and ID. Each item can also include collision and navigation shapes. This resource is used in GridMap.

**Methods:**
- clear() - Clears the library.
- create_item(id: int) - Creates a new item in the library with the given ID. You can get an unused ID from `get_last_unused_item_id`.
- find_item_by_name(name: String) -> int - Returns the first item with the given name, or `-1` if no item is found.
- get_item_count() -> int - Returns the number of items present in the library.
- get_item_list() -> PackedInt32Array - Returns the list of item IDs in use.
- get_item_mesh(id: int) -> Mesh - Returns the item's mesh.
- get_item_mesh_cast_shadow(id: int) -> int - Returns the item's shadow casting mode.
- get_item_mesh_transform(id: int) -> Transform3D - Returns the transform applied to the item's mesh.
- get_item_name(id: int) -> String - Returns the item's name.
- get_item_navigation_layers(id: int) -> int - Returns the item's navigation layers bitmask.
- get_item_navigation_mesh(id: int) -> NavigationMesh - Returns the item's navigation mesh.
- get_item_navigation_mesh_transform(id: int) -> Transform3D - Returns the transform applied to the item's navigation mesh.
- get_item_preview(id: int) -> Texture2D - When running in the editor, returns a generated item preview (a 3D rendering in isometric perspective). When used in a running project, returns the manually-defined item preview which can be set using `set_item_preview`. Returns an empty Texture2D if no preview was manually set in a running project.
- get_item_shapes(id: int) -> Array - Returns an item's collision shapes. The array consists of each Shape3D followed by its Transform3D.
- get_last_unused_item_id() -> int - Gets an unused ID for a new item.
- remove_item(id: int) - Removes the item.
- set_item_mesh(id: int, mesh: Mesh) - Sets the item's mesh.
- set_item_mesh_cast_shadow(id: int, shadow_casting_setting: int) - Sets the item's shadow casting mode to `shadow_casting_setting`.
- set_item_mesh_transform(id: int, mesh_transform: Transform3D) - Sets the transform to apply to the item's mesh.
- set_item_name(id: int, name: String) - Sets the item's name. This name is shown in the editor. It can also be used to look up the item later using `find_item_by_name`.
- set_item_navigation_layers(id: int, navigation_layers: int) - Sets the item's navigation layers bitmask.
- set_item_navigation_mesh(id: int, navigation_mesh: NavigationMesh) - Sets the item's navigation mesh.
- set_item_navigation_mesh_transform(id: int, navigation_mesh: Transform3D) - Sets the transform to apply to the item's navigation mesh.
- set_item_preview(id: int, texture: Texture2D) - Sets a texture to use as the item's preview icon in the editor.
- set_item_shapes(id: int, shapes: Array) - Sets an item's collision shapes. The array should consist of Shape3D objects, each followed by a Transform3D that will be applied to it. For shapes that should not have a transform, use `Transform3D.IDENTITY`.

