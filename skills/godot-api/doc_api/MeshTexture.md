## MeshTexture <- Texture2D

Simple texture that uses a mesh to draw itself. It's limited because flags can't be changed and region drawing is not supported.

**Props:**
- base_texture: Texture2D
- image_size: Vector2 = Vector2(0, 0)
- mesh: Mesh
- resource_local_to_scene: bool = false

- **base_texture**: Sets the base texture that the Mesh will use to draw.
- **image_size**: Sets the size of the image, needed for reference.
- **mesh**: Sets the mesh used to draw. It must be a mesh using 2D vertices.

