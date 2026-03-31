## TextLine <- RefCounted

Abstraction over TextServer for handling a single line of text.

**Props:**
- alignment: int (HorizontalAlignment) = 0
- direction: int (TextServer.Direction) = 0
- ellipsis_char: String = "…"
- flags: int (TextServer.JustificationFlag) = 3
- orientation: int (TextServer.Orientation) = 0
- preserve_control: bool = false
- preserve_invalid: bool = true
- text_overrun_behavior: int (TextServer.OverrunBehavior) = 3
- width: float = -1.0

- **alignment**: Sets text alignment within the line as if the line was horizontal.
- **direction**: Text writing direction.
- **ellipsis_char**: Ellipsis character used for text clipping.
- **flags**: Line alignment rules. For more info see TextServer.
- **orientation**: Text orientation.
- **preserve_control**: If set to `true` text will display control characters.
- **preserve_invalid**: If set to `true` text will display invalid characters.
- **text_overrun_behavior**: The clipping behavior when the text exceeds the text line's set width.
- **width**: Text line width.

**Methods:**
- add_object(key: Variant, size: Vector2, inline_align: int = 5, length: int = 1, baseline: float = 0.0) -> bool - Adds inline object to the text buffer, `key` must be unique. In the text, object is represented as `length` object replacement characters.
- add_string(text: String, font: Font, font_size: int, language: String = "", meta: Variant = null) -> bool - Adds text span and font to draw it.
- clear() - Clears text line (removes text and inline objects).
- draw(canvas: RID, pos: Vector2, color: Color = Color(1, 1, 1, 1), oversampling: float = 0.0) - Draw text into a canvas item at a given position, with `color`. `pos` specifies the top left corner of the bounding box. If `oversampling` is greater than zero, it is used as font oversampling factor, otherwise viewport oversampling settings are used.
- draw_outline(canvas: RID, pos: Vector2, outline_size: int = 1, color: Color = Color(1, 1, 1, 1), oversampling: float = 0.0) - Draw text into a canvas item at a given position, with `color`. `pos` specifies the top left corner of the bounding box. If `oversampling` is greater than zero, it is used as font oversampling factor, otherwise viewport oversampling settings are used.
- duplicate() -> TextLine - Duplicates this TextLine.
- get_inferred_direction() -> int - Returns the text writing direction inferred by the BiDi algorithm.
- get_line_ascent() -> float - Returns the text ascent (number of pixels above the baseline for horizontal layout or to the left of baseline for vertical).
- get_line_descent() -> float - Returns the text descent (number of pixels below the baseline for horizontal layout or to the right of baseline for vertical).
- get_line_underline_position() -> float - Returns pixel offset of the underline below the baseline.
- get_line_underline_thickness() -> float - Returns thickness of the underline.
- get_line_width() -> float - Returns width (for horizontal layout) or height (for vertical) of the text.
- get_object_rect(key: Variant) -> Rect2 - Returns bounding rectangle of the inline object.
- get_objects() -> Array - Returns array of inline objects.
- get_rid() -> RID - Returns TextServer buffer RID.
- get_size() -> Vector2 - Returns size of the bounding box of the text.
- has_object(key: Variant) -> bool - Returns `true` if an object with `key` is embedded in this line.
- hit_test(coords: float) -> int - Returns caret character offset at the specified pixel offset at the baseline. This function always returns a valid position.
- resize_object(key: Variant, size: Vector2, inline_align: int = 5, baseline: float = 0.0) -> bool - Sets new size and alignment of embedded object.
- set_bidi_override(override: Array) - Overrides BiDi for the structured text. Override ranges should cover full source text without overlaps. BiDi algorithm will be used on each range separately.
- tab_align(tab_stops: PackedFloat32Array) - Aligns text to the given tab-stops.

