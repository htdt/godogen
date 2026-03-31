## Sprite3D <- SpriteBase3D

A node that displays a 2D texture in a 3D environment. The texture displayed can be a region from a larger atlas texture, or a frame from a sprite sheet animation. See also SpriteBase3D where properties such as the billboard mode are defined.

**Props:**
- frame: int = 0
- frame_coords: Vector2i = Vector2i(0, 0)
- hframes: int = 1
- region_enabled: bool = false
- region_rect: Rect2 = Rect2(0, 0, 0, 0)
- texture: Texture2D
- vframes: int = 1

- **frame**: Current frame to display from sprite sheet. `hframes` or `vframes` must be greater than 1. This property is automatically adjusted when `hframes` or `vframes` are changed to keep pointing to the same visual frame (same column and row). If that's impossible, this value is reset to `0`.
- **frame_coords**: Coordinates of the frame to display from sprite sheet. This is as an alias for the `frame` property. `hframes` or `vframes` must be greater than 1.
- **hframes**: The number of columns in the sprite sheet. When this property is changed, `frame` is adjusted so that the same visual frame is maintained (same row and column). If that's impossible, `frame` is reset to `0`.
- **region_enabled**: If `true`, the sprite will use `region_rect` and display only the specified part of its texture.
- **region_rect**: The region of the atlas texture to display. `region_enabled` must be `true`.
- **texture**: Texture2D object to draw. If `GeometryInstance3D.material_override` is used, this will be overridden. The size information is still used.
- **vframes**: The number of rows in the sprite sheet. When this property is changed, `frame` is adjusted so that the same visual frame is maintained (same row and column). If that's impossible, `frame` is reset to `0`.

**Signals:**
- frame_changed - Emitted when the `frame` changes.
- texture_changed - Emitted when the `texture` changes.

