## StyleBoxTexture <- StyleBox

A texture-based nine-patch StyleBox, in a way similar to NinePatchRect. This stylebox performs a 3×3 scaling of a texture, where only the center cell is fully stretched. This makes it possible to design bordered styles regardless of the stylebox's size.

**Props:**
- axis_stretch_horizontal: int (StyleBoxTexture.AxisStretchMode) = 0
- axis_stretch_vertical: int (StyleBoxTexture.AxisStretchMode) = 0
- draw_center: bool = true
- expand_margin_bottom: float = 0.0
- expand_margin_left: float = 0.0
- expand_margin_right: float = 0.0
- expand_margin_top: float = 0.0
- modulate_color: Color = Color(1, 1, 1, 1)
- region_rect: Rect2 = Rect2(0, 0, 0, 0)
- texture: Texture2D
- texture_margin_bottom: float = 0.0
- texture_margin_left: float = 0.0
- texture_margin_right: float = 0.0
- texture_margin_top: float = 0.0

- **axis_stretch_horizontal**: Controls how the stylebox's texture will be stretched or tiled horizontally.
- **axis_stretch_vertical**: Controls how the stylebox's texture will be stretched or tiled vertically.
- **draw_center**: If `true`, the nine-patch texture's center tile will be drawn.
- **expand_margin_bottom**: Expands the bottom margin of this style box when drawing, causing it to be drawn larger than requested.
- **expand_margin_left**: Expands the left margin of this style box when drawing, causing it to be drawn larger than requested.
- **expand_margin_right**: Expands the right margin of this style box when drawing, causing it to be drawn larger than requested.
- **expand_margin_top**: Expands the top margin of this style box when drawing, causing it to be drawn larger than requested.
- **modulate_color**: Modulates the color of the texture when this style box is drawn.
- **region_rect**: The region to use from the `texture`. This is equivalent to first wrapping the `texture` in an AtlasTexture with the same region. If empty (`Rect2(0, 0, 0, 0)`), the whole `texture` is used.
- **texture**: The texture to use when drawing this style box.
- **texture_margin_bottom**: Increases the bottom margin of the 3×3 texture box. A higher value means more of the source texture is considered to be part of the bottom border of the 3×3 box. This is also the value used as fallback for `StyleBox.content_margin_bottom` if it is negative.
- **texture_margin_left**: Increases the left margin of the 3×3 texture box. A higher value means more of the source texture is considered to be part of the left border of the 3×3 box. This is also the value used as fallback for `StyleBox.content_margin_left` if it is negative.
- **texture_margin_right**: Increases the right margin of the 3×3 texture box. A higher value means more of the source texture is considered to be part of the right border of the 3×3 box. This is also the value used as fallback for `StyleBox.content_margin_right` if it is negative.
- **texture_margin_top**: Increases the top margin of the 3×3 texture box. A higher value means more of the source texture is considered to be part of the top border of the 3×3 box. This is also the value used as fallback for `StyleBox.content_margin_top` if it is negative.

**Methods:**
- get_expand_margin(margin: int) -> float - Returns the expand margin size of the specified `Side`.
- get_texture_margin(margin: int) -> float - Returns the margin size of the specified `Side`.
- set_expand_margin(margin: int, size: float) - Sets the expand margin to `size` pixels for the specified `Side`.
- set_expand_margin_all(size: float) - Sets the expand margin to `size` pixels for all sides.
- set_texture_margin(margin: int, size: float) - Sets the margin to `size` pixels for the specified `Side`.
- set_texture_margin_all(size: float) - Sets the margin to `size` pixels for all sides.

**Enums:**
**AxisStretchMode:** AXIS_STRETCH_MODE_STRETCH=0, AXIS_STRETCH_MODE_TILE=1, AXIS_STRETCH_MODE_TILE_FIT=2
  - AXIS_STRETCH_MODE_STRETCH: Stretch the stylebox's texture. This results in visible distortion unless the texture size matches the stylebox's size perfectly.
  - AXIS_STRETCH_MODE_TILE: Repeats the stylebox's texture to match the stylebox's size according to the nine-patch system.
  - AXIS_STRETCH_MODE_TILE_FIT: Repeats the stylebox's texture to match the stylebox's size according to the nine-patch system. Unlike `AXIS_STRETCH_MODE_TILE`, the texture may be slightly stretched to make the nine-patch texture tile seamlessly.

