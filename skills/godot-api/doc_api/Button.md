## Button <- BaseButton

Button is the standard themed button. It can contain text and an icon, and it will display them according to the current Theme. **Example:** Create a button and connect a method that will be called when the button is pressed: See also BaseButton which contains common properties and methods associated with this node. **Note:** Buttons do not detect touch input and therefore don't support multitouch, since mouse emulation can only press one button at a given time. Use TouchScreenButton for buttons that trigger gameplay movement or actions.

**Props:**
- alignment: int (HorizontalAlignment) = 1
- autowrap_mode: int (TextServer.AutowrapMode) = 0
- autowrap_trim_flags: int (TextServer.LineBreakFlag) = 128
- clip_text: bool = false
- expand_icon: bool = false
- flat: bool = false
- icon: Texture2D
- icon_alignment: int (HorizontalAlignment) = 0
- language: String = ""
- text: String = ""
- text_direction: int (Control.TextDirection) = 0
- text_overrun_behavior: int (TextServer.OverrunBehavior) = 0
- vertical_icon_alignment: int (VerticalAlignment) = 1

- **alignment**: Text alignment policy for the button's text.
- **autowrap_mode**: If set to something other than `TextServer.AUTOWRAP_OFF`, the text gets wrapped inside the node's bounding rectangle.
- **autowrap_trim_flags**: Autowrap space trimming flags. See `TextServer.BREAK_TRIM_START_EDGE_SPACES` and `TextServer.BREAK_TRIM_END_EDGE_SPACES` for more info.
- **clip_text**: If `true`, text that is too large to fit the button is clipped horizontally. If `false`, the button will always be wide enough to hold the text. The text is not vertically clipped, and the button's height is not affected by this property.
- **expand_icon**: When enabled, the button's icon will expand/shrink to fit the button's size while keeping its aspect. See also [theme_item icon_max_width].
- **flat**: Flat buttons don't display decoration.
- **icon**: Button's icon, if text is present the icon will be placed before the text. To edit margin and spacing of the icon, use [theme_item h_separation] theme property and `content_margin_*` properties of the used StyleBoxes.
- **icon_alignment**: Specifies if the icon should be aligned horizontally to the left, right, or center of a button. Uses the same `HorizontalAlignment` constants as the text alignment. If centered horizontally and vertically, text will draw on top of the icon.
- **language**: Language code used for line-breaking and text shaping algorithms. If left empty, the current locale is used instead.
- **text**: The button's text that will be displayed inside the button's area.
- **text_direction**: Base text writing direction.
- **text_overrun_behavior**: Sets the clipping behavior when the text exceeds the node's bounding rectangle.
- **vertical_icon_alignment**: Specifies if the icon should be aligned vertically to the top, bottom, or center of a button. Uses the same `VerticalAlignment` constants as the text alignment. If centered horizontally and vertically, text will draw on top of the icon.

