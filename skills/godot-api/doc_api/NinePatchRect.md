## NinePatchRect <- Control

Also known as 9-slice panels, NinePatchRect produces clean panels of any size based on a small texture. To do so, it splits the texture in a 3×3 grid. When you scale the node, it tiles the texture's edges horizontally or vertically, tiles the center on both axes, and leaves the corners unchanged.

**Props:**
- axis_stretch_horizontal: int (NinePatchRect.AxisStretchMode) = 0
- axis_stretch_vertical: int (NinePatchRect.AxisStretchMode) = 0
- draw_center: bool = true
- mouse_filter: int (Control.MouseFilter) = 2
- patch_margin_bottom: int = 0
- patch_margin_left: int = 0
- patch_margin_right: int = 0
- patch_margin_top: int = 0
- region_rect: Rect2 = Rect2(0, 0, 0, 0)
- texture: Texture2D

- **axis_stretch_horizontal**: The stretch mode to use for horizontal stretching/tiling.
- **axis_stretch_vertical**: The stretch mode to use for vertical stretching/tiling.
- **draw_center**: If `true`, draw the panel's center. Else, only draw the 9-slice's borders.
- **patch_margin_bottom**: The height of the 9-slice's bottom row. A margin of 16 means the 9-slice's bottom corners and side will have a height of 16 pixels. You can set all 4 margin values individually to create panels with non-uniform borders.
- **patch_margin_left**: The width of the 9-slice's left column. A margin of 16 means the 9-slice's left corners and side will have a width of 16 pixels. You can set all 4 margin values individually to create panels with non-uniform borders.
- **patch_margin_right**: The width of the 9-slice's right column. A margin of 16 means the 9-slice's right corners and side will have a width of 16 pixels. You can set all 4 margin values individually to create panels with non-uniform borders.
- **patch_margin_top**: The height of the 9-slice's top row. A margin of 16 means the 9-slice's top corners and side will have a height of 16 pixels. You can set all 4 margin values individually to create panels with non-uniform borders.
- **region_rect**: Rectangular region of the texture to sample from. If you're working with an atlas, use this property to define the area the 9-slice should use. All other properties are relative to this one. If the rect is empty, NinePatchRect will use the whole texture.
- **texture**: The node's texture resource.

**Methods:**
- get_patch_margin(margin: int) -> int - Returns the size of the margin on the specified `Side`.
- set_patch_margin(margin: int, value: int) - Sets the size of the margin on the specified `Side` to `value` pixels.

**Signals:**
- texture_changed - Emitted when the node's texture changes.

**Enums:**
**AxisStretchMode:** AXIS_STRETCH_MODE_STRETCH=0, AXIS_STRETCH_MODE_TILE=1, AXIS_STRETCH_MODE_TILE_FIT=2
  - AXIS_STRETCH_MODE_STRETCH: Stretches the center texture across the NinePatchRect. This may cause the texture to be distorted.
  - AXIS_STRETCH_MODE_TILE: Repeats the center texture across the NinePatchRect. This won't cause any visible distortion. The texture must be seamless for this to work without displaying artifacts between edges.
  - AXIS_STRETCH_MODE_TILE_FIT: Repeats the center texture across the NinePatchRect, but will also stretch the texture to make sure each tile is visible in full. This may cause the texture to be distorted, but less than `AXIS_STRETCH_MODE_STRETCH`. The texture must be seamless for this to work without displaying artifacts between edges.

