## LabelSettings <- Resource

LabelSettings is a resource that provides common settings to customize the text in a Label. It will take priority over the properties defined in `Control.theme`. The resource can be shared between multiple labels and changed on the fly, so it's convenient and flexible way to setup text style.

**Props:**
- font: Font
- font_color: Color = Color(1, 1, 1, 1)
- font_size: int = 16
- line_spacing: float = 3.0
- outline_color: Color = Color(1, 1, 1, 1)
- outline_size: int = 0
- paragraph_spacing: float = 0.0
- shadow_color: Color = Color(0, 0, 0, 0)
- shadow_offset: Vector2 = Vector2(1, 1)
- shadow_size: int = 1
- stacked_outline_count: int = 0
- stacked_outline_{index}/color: Color = Color(0, 0, 0, 1)
- stacked_outline_{index}/size: int = 0
- stacked_shadow_count: int = 0
- stacked_shadow_{index}/color: Color = Color(0, 0, 0, 1)
- stacked_shadow_{index}/offset: Vector2 = Vector2i(1, 1)
- stacked_shadow_{index}/outline_size: int = 0

- **font**: Font used for the text.
- **font_color**: Color of the text.
- **font_size**: Size of the text.
- **line_spacing**: Additional vertical spacing between lines (in pixels), spacing is added to line descent. This value can be negative.
- **outline_color**: The color of the outline.
- **outline_size**: Text outline size.
- **paragraph_spacing**: Vertical space between paragraphs. Added on top of `line_spacing`.
- **shadow_color**: Color of the shadow effect. If alpha is `0`, no shadow will be drawn.
- **shadow_offset**: Offset of the shadow effect, in pixels.
- **shadow_size**: Size of the shadow effect.
- **stacked_outline_count**: The number of stacked outlines.
- **stacked_outline_{index}/color**: The color of the outline at `index`. **Note:** `index` is a value in the `0 .. stacked_outline_count - 1` range.
- **stacked_outline_{index}/size**: The size of the outline at `index`. **Note:** `index` is a value in the `0 .. stacked_outline_count - 1` range.
- **stacked_shadow_count**: The number of stacked shadows.
- **stacked_shadow_{index}/color**: The color of the shadow at `index`. **Note:** `index` is a value in the `0 .. stacked_shadow_count - 1` range.
- **stacked_shadow_{index}/offset**: The offset of the shadow at `index`. **Note:** `index` is a value in the `0 .. stacked_shadow_count - 1` range.
- **stacked_shadow_{index}/outline_size**: The size of the shadow outline at `index`. **Note:** `index` is a value in the `0 .. stacked_shadow_count - 1` range.

**Methods:**
- add_stacked_outline(index: int = -1) - Adds a new stacked outline to the label at the given `index`. If `index` is `-1`, the new stacked outline will be added at the end of the list.
- add_stacked_shadow(index: int = -1) - Adds a new stacked shadow to the label at the given `index`. If `index` is `-1`, the new stacked shadow will be added at the end of the list.
- get_stacked_outline_color(index: int) -> Color - Returns the color of the stacked outline at `index`.
- get_stacked_outline_size(index: int) -> int - Returns the size of the stacked outline at `index`.
- get_stacked_shadow_color(index: int) -> Color - Returns the color of the stacked shadow at `index`.
- get_stacked_shadow_offset(index: int) -> Vector2 - Returns the offset of the stacked shadow at `index`.
- get_stacked_shadow_outline_size(index: int) -> int - Returns the outline size of the stacked shadow at `index`.
- move_stacked_outline(from_index: int, to_position: int) - Moves the stacked outline at index `from_index` to the given position `to_position` in the array.
- move_stacked_shadow(from_index: int, to_position: int) - Moves the stacked shadow at index `from_index` to the given position `to_position` in the array.
- remove_stacked_outline(index: int) - Removes the stacked outline at index `index`.
- remove_stacked_shadow(index: int) - Removes the stacked shadow at index `index`.
- set_stacked_outline_color(index: int, color: Color) - Sets the color of the stacked outline identified by the given `index` to `color`.
- set_stacked_outline_size(index: int, size: int) - Sets the size of the stacked outline identified by the given `index` to `size`.
- set_stacked_shadow_color(index: int, color: Color) - Sets the color of the stacked shadow identified by the given `index` to `color`.
- set_stacked_shadow_offset(index: int, offset: Vector2) - Sets the offset of the stacked shadow identified by the given `index` to `offset`.
- set_stacked_shadow_outline_size(index: int, size: int) - Sets the outline size of the stacked shadow identified by the given `index` to `size`.

