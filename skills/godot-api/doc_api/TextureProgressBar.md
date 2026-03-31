## TextureProgressBar <- Range

TextureProgressBar works like ProgressBar, but uses up to 3 textures instead of Godot's Theme resource. It can be used to create horizontal, vertical and radial progress bars.

**Props:**
- fill_mode: int = 0
- mouse_filter: int (Control.MouseFilter) = 1
- nine_patch_stretch: bool = false
- radial_center_offset: Vector2 = Vector2(0, 0)
- radial_fill_degrees: float = 360.0
- radial_initial_angle: float = 0.0
- size_flags_vertical: int (Control.SizeFlags) = 1
- step: float = 1.0
- stretch_margin_bottom: int = 0
- stretch_margin_left: int = 0
- stretch_margin_right: int = 0
- stretch_margin_top: int = 0
- texture_over: Texture2D
- texture_progress: Texture2D
- texture_progress_offset: Vector2 = Vector2(0, 0)
- texture_under: Texture2D
- tint_over: Color = Color(1, 1, 1, 1)
- tint_progress: Color = Color(1, 1, 1, 1)
- tint_under: Color = Color(1, 1, 1, 1)

- **fill_mode**: The fill direction. See `FillMode` for possible values.
- **nine_patch_stretch**: If `true`, Godot treats the bar's textures like in NinePatchRect. Use the `stretch_margin_*` properties like `stretch_margin_bottom` to set up the nine patch's 3×3 grid. When using a radial `fill_mode`, this setting will only enable stretching for `texture_progress`, while `texture_under` and `texture_over` will be treated like in NinePatchRect.
- **radial_center_offset**: Offsets `texture_progress` if `fill_mode` is `FILL_CLOCKWISE`, `FILL_COUNTER_CLOCKWISE`, or `FILL_CLOCKWISE_AND_COUNTER_CLOCKWISE`. **Note:** The effective radial center always stays within the `texture_progress` bounds. If you need to move it outside the texture's bounds, modify the `texture_progress` to contain additional empty space where needed.
- **radial_fill_degrees**: Upper limit for the fill of `texture_progress` if `fill_mode` is `FILL_CLOCKWISE`, `FILL_COUNTER_CLOCKWISE`, or `FILL_CLOCKWISE_AND_COUNTER_CLOCKWISE`. When the node's `value` is equal to its `max_value`, the texture fills up to this angle. See `Range.value`, `Range.max_value`.
- **radial_initial_angle**: Starting angle for the fill of `texture_progress` if `fill_mode` is `FILL_CLOCKWISE`, `FILL_COUNTER_CLOCKWISE`, or `FILL_CLOCKWISE_AND_COUNTER_CLOCKWISE`. When the node's `value` is equal to its `min_value`, the texture doesn't show up at all. When the `value` increases, the texture fills and tends towards `radial_fill_degrees`. **Note:** `radial_initial_angle` is wrapped between `0` and `360` degrees (inclusive).
- **stretch_margin_bottom**: The height of the 9-patch's bottom row. A margin of 16 means the 9-slice's bottom corners and side will have a height of 16 pixels. You can set all 4 margin values individually to create panels with non-uniform borders. Only effective if `nine_patch_stretch` is `true`.
- **stretch_margin_left**: The width of the 9-patch's left column. Only effective if `nine_patch_stretch` is `true`.
- **stretch_margin_right**: The width of the 9-patch's right column. Only effective if `nine_patch_stretch` is `true`.
- **stretch_margin_top**: The height of the 9-patch's top row. Only effective if `nine_patch_stretch` is `true`.
- **texture_over**: Texture2D that draws over the progress bar. Use it to add highlights or an upper-frame that hides part of `texture_progress`.
- **texture_progress**: Texture2D that clips based on the node's `value` and `fill_mode`. As `value` increased, the texture fills up. It shows entirely when `value` reaches `max_value`. It doesn't show at all if `value` is equal to `min_value`. The `value` property comes from Range. See `Range.value`, `Range.min_value`, `Range.max_value`.
- **texture_progress_offset**: The offset of `texture_progress`. Useful for `texture_over` and `texture_under` with fancy borders, to avoid transparent margins in your progress texture.
- **texture_under**: Texture2D that draws under the progress bar. The bar's background.
- **tint_over**: Multiplies the color of the bar's `texture_over` texture. The effect is similar to `CanvasItem.modulate`, except it only affects this specific texture instead of the entire node.
- **tint_progress**: Multiplies the color of the bar's `texture_progress` texture.
- **tint_under**: Multiplies the color of the bar's `texture_under` texture.

**Methods:**
- get_stretch_margin(margin: int) -> int - Returns the stretch margin with the specified index. See `stretch_margin_bottom` and related properties.
- set_stretch_margin(margin: int, value: int) - Sets the stretch margin with the specified index. See `stretch_margin_bottom` and related properties.

**Enums:**
**FillMode:** FILL_LEFT_TO_RIGHT=0, FILL_RIGHT_TO_LEFT=1, FILL_TOP_TO_BOTTOM=2, FILL_BOTTOM_TO_TOP=3, FILL_CLOCKWISE=4, FILL_COUNTER_CLOCKWISE=5, FILL_BILINEAR_LEFT_AND_RIGHT=6, FILL_BILINEAR_TOP_AND_BOTTOM=7, FILL_CLOCKWISE_AND_COUNTER_CLOCKWISE=8
  - FILL_LEFT_TO_RIGHT: The `texture_progress` fills from left to right.
  - FILL_RIGHT_TO_LEFT: The `texture_progress` fills from right to left.
  - FILL_TOP_TO_BOTTOM: The `texture_progress` fills from top to bottom.
  - FILL_BOTTOM_TO_TOP: The `texture_progress` fills from bottom to top.
  - FILL_CLOCKWISE: Turns the node into a radial bar. The `texture_progress` fills clockwise. See `radial_center_offset`, `radial_initial_angle` and `radial_fill_degrees` to control the way the bar fills up.
  - FILL_COUNTER_CLOCKWISE: Turns the node into a radial bar. The `texture_progress` fills counterclockwise. See `radial_center_offset`, `radial_initial_angle` and `radial_fill_degrees` to control the way the bar fills up.
  - FILL_BILINEAR_LEFT_AND_RIGHT: The `texture_progress` fills from the center, expanding both towards the left and the right.
  - FILL_BILINEAR_TOP_AND_BOTTOM: The `texture_progress` fills from the center, expanding both towards the top and the bottom.
  - FILL_CLOCKWISE_AND_COUNTER_CLOCKWISE: Turns the node into a radial bar. The `texture_progress` fills radially from the center, expanding both clockwise and counterclockwise. See `radial_center_offset`, `radial_initial_angle` and `radial_fill_degrees` to control the way the bar fills up.

