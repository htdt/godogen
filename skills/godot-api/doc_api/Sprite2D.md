## Sprite2D <- Node2D

A node that displays a 2D texture. The texture displayed can be a region from a larger atlas texture, or a frame from a sprite sheet animation.

**Props:**
- centered: bool = true
- flip_h: bool = false
- flip_v: bool = false
- frame: int = 0
- frame_coords: Vector2i = Vector2i(0, 0)
- hframes: int = 1
- offset: Vector2 = Vector2(0, 0)
- region_enabled: bool = false
- region_filter_clip_enabled: bool = false
- region_rect: Rect2 = Rect2(0, 0, 0, 0)
- texture: Texture2D
- vframes: int = 1

- **centered**: If `true`, texture is centered. **Note:** For games with a pixel art aesthetic, textures may appear deformed when centered. This is caused by their position being between pixels. To prevent this, set this property to `false`, or consider enabling `ProjectSettings.rendering/2d/snap/snap_2d_vertices_to_pixel` and `ProjectSettings.rendering/2d/snap/snap_2d_transforms_to_pixel`.
- **flip_h**: If `true`, texture is flipped horizontally.
- **flip_v**: If `true`, texture is flipped vertically.
- **frame**: Current frame to display from sprite sheet. `hframes` or `vframes` must be greater than 1. This property is automatically adjusted when `hframes` or `vframes` are changed to keep pointing to the same visual frame (same column and row). If that's impossible, this value is reset to `0`.
- **frame_coords**: Coordinates of the frame to display from sprite sheet. This is as an alias for the `frame` property. `hframes` or `vframes` must be greater than 1.
- **hframes**: The number of columns in the sprite sheet. When this property is changed, `frame` is adjusted so that the same visual frame is maintained (same row and column). If that's impossible, `frame` is reset to `0`.
- **offset**: The texture's drawing offset. **Note:** When you increase `offset`.y in Sprite2D, the sprite moves downward on screen (i.e., +Y is down).
- **region_enabled**: If `true`, texture is cut from a larger atlas texture. See `region_rect`. **Note:** When using a custom Shader on a Sprite2D, the `UV` shader built-in will refer to the entire texture space. Use the `REGION_RECT` built-in to get the currently visible region defined in `region_rect` instead. See for details.
- **region_filter_clip_enabled**: If `true`, the area outside of the `region_rect` is clipped to avoid bleeding of the surrounding texture pixels. `region_enabled` must be `true`.
- **region_rect**: The region of the atlas texture to display. `region_enabled` must be `true`.
- **texture**: Texture2D object to draw.
- **vframes**: The number of rows in the sprite sheet. When this property is changed, `frame` is adjusted so that the same visual frame is maintained (same row and column). If that's impossible, `frame` is reset to `0`.

**Methods:**
- get_rect() -> Rect2 - Returns a Rect2 representing the Sprite2D's boundary in local coordinates. **Example:** Detect if the Sprite2D was clicked:
- is_pixel_opaque(pos: Vector2) -> bool - Returns `true` if the pixel at the given position is opaque, `false` otherwise. Also returns `false` if the given position is out of bounds or this sprite's `texture` is `null`. `pos` is in local coordinates.

**Signals:**
- frame_changed - Emitted when the `frame` changes.
- texture_changed - Emitted when the `texture` changes.

