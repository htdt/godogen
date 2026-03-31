## Label <- Control

A control for displaying plain text. It gives you control over the horizontal and vertical alignment and can wrap the text inside the node's bounding rectangle. It doesn't support bold, italics, or other rich text formatting. For that, use RichTextLabel instead. **Note:** A single Label node is not designed to display huge amounts of text. To display large amounts of text in a single node, consider using RichTextLabel instead as it supports features like an integrated scroll bar and threading. RichTextLabel generally performs better when displaying large amounts of text (several pages or more).

**Props:**
- autowrap_mode: int (TextServer.AutowrapMode) = 0
- autowrap_trim_flags: int (TextServer.LineBreakFlag) = 192
- clip_text: bool = false
- ellipsis_char: String = "…"
- horizontal_alignment: int (HorizontalAlignment) = 0
- justification_flags: int (TextServer.JustificationFlag) = 163
- label_settings: LabelSettings
- language: String = ""
- lines_skipped: int = 0
- max_lines_visible: int = -1
- mouse_filter: int (Control.MouseFilter) = 2
- paragraph_separator: String = "\\n"
- size_flags_vertical: int (Control.SizeFlags) = 4
- structured_text_bidi_override: int (TextServer.StructuredTextParser) = 0
- structured_text_bidi_override_options: Array = []
- tab_stops: PackedFloat32Array = PackedFloat32Array()
- text: String = ""
- text_direction: int (Control.TextDirection) = 0
- text_overrun_behavior: int (TextServer.OverrunBehavior) = 0
- uppercase: bool = false
- vertical_alignment: int (VerticalAlignment) = 0
- visible_characters: int = -1
- visible_characters_behavior: int (TextServer.VisibleCharactersBehavior) = 0
- visible_ratio: float = 1.0

- **autowrap_mode**: If set to something other than `TextServer.AUTOWRAP_OFF`, the text gets wrapped inside the node's bounding rectangle. If you resize the node, it will change its height automatically to show all the text.
- **autowrap_trim_flags**: Autowrap space trimming flags. See `TextServer.BREAK_TRIM_START_EDGE_SPACES` and `TextServer.BREAK_TRIM_END_EDGE_SPACES` for more info.
- **clip_text**: If `true`, the Label only shows the text that fits inside its bounding rectangle and will clip text horizontally.
- **ellipsis_char**: Ellipsis character used for text clipping.
- **horizontal_alignment**: Controls the text's horizontal alignment. Supports left, center, right, and fill (also known as justify).
- **justification_flags**: Line fill alignment rules.
- **label_settings**: A LabelSettings resource that can be shared between multiple Label nodes. Takes priority over theme properties.
- **language**: Language code used for line-breaking and text shaping algorithms. If left empty, the current locale is used instead.
- **lines_skipped**: The number of the lines ignored and not displayed from the start of the `text` value.
- **max_lines_visible**: Limits the lines of text the node shows on screen.
- **paragraph_separator**: String used as a paragraph separator. Each paragraph is processed independently, in its own BiDi context.
- **structured_text_bidi_override**: Set BiDi algorithm override for the structured text.
- **structured_text_bidi_override_options**: Set additional options for BiDi override.
- **tab_stops**: Aligns text to the given tab-stops.
- **text**: The text to display on screen.
- **text_direction**: Base text writing direction.
- **text_overrun_behavior**: The clipping behavior when the text exceeds the node's bounding rectangle.
- **uppercase**: If `true`, all the text displays as UPPERCASE.
- **vertical_alignment**: Controls the text's vertical alignment. Supports top, center, bottom, and fill.
- **visible_characters**: The number of characters to display. If set to `-1`, all characters are displayed. This can be useful when animating the text appearing in a dialog box. **Note:** Setting this property updates `visible_ratio` accordingly. **Note:** Characters are counted as Unicode codepoints. A single visible grapheme may contain multiple codepoints (e.g. certain emoji use three codepoints). A single codepoint may contain two UTF-16 characters, which are used in C# strings.
- **visible_characters_behavior**: The clipping behavior when `visible_characters` or `visible_ratio` is set.
- **visible_ratio**: The fraction of characters to display, relative to the total number of characters (see `get_total_character_count`). If set to `1.0`, all characters are displayed. If set to `0.5`, only half of the characters will be displayed. This can be useful when animating the text appearing in a dialog box. **Note:** Setting this property updates `visible_characters` accordingly.

**Methods:**
- get_character_bounds(pos: int) -> Rect2 - Returns the bounding rectangle of the character at position `pos` in the label's local coordinate system. If the character is a non-visual character or `pos` is outside the valid range, an empty Rect2 is returned. If the character is a part of a composite grapheme, the bounding rectangle of the whole grapheme is returned.
- get_line_count() -> int - Returns the number of lines of text the Label has.
- get_line_height(line: int = -1) -> int - Returns the height of the line `line`. If `line` is set to `-1`, returns the biggest line height. If there are no lines, returns font size in pixels.
- get_total_character_count() -> int - Returns the total number of printable characters in the text (excluding spaces and newlines).
- get_visible_line_count() -> int - Returns the number of lines shown. Useful if the Label's height cannot currently display all lines.

