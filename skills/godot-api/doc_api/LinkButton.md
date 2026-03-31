## LinkButton <- BaseButton

A button that represents a link. This type of button is primarily used for interactions that cause a context change (like linking to a web page). See also BaseButton which contains common properties and methods associated with this node.

**Props:**
- ellipsis_char: String = "…"
- focus_mode: int (Control.FocusMode) = 3
- language: String = ""
- mouse_default_cursor_shape: int (Control.CursorShape) = 2
- structured_text_bidi_override: int (TextServer.StructuredTextParser) = 0
- structured_text_bidi_override_options: Array = []
- text: String = ""
- text_direction: int (Control.TextDirection) = 0
- text_overrun_behavior: int (TextServer.OverrunBehavior) = 0
- underline: int (LinkButton.UnderlineMode) = 0
- uri: String = ""

- **ellipsis_char**: Ellipsis character used for text clipping.
- **language**: Language code used for line-breaking and text shaping algorithms. If left empty, the current locale is used instead.
- **structured_text_bidi_override**: Set BiDi algorithm override for the structured text.
- **structured_text_bidi_override_options**: Set additional options for BiDi override.
- **text**: The button's text that will be displayed inside the button's area.
- **text_direction**: Base text writing direction.
- **text_overrun_behavior**: Sets the clipping behavior when the text exceeds the node's bounding rectangle.
- **underline**: The underline mode to use for the text.
- **uri**: The for this LinkButton. If set to a valid URI, pressing the button opens the URI using the operating system's default program for the protocol (via `OS.shell_open`). HTTP and HTTPS URLs open the default web browser.

**Enums:**
**UnderlineMode:** UNDERLINE_MODE_ALWAYS=0, UNDERLINE_MODE_ON_HOVER=1, UNDERLINE_MODE_NEVER=2
  - UNDERLINE_MODE_ALWAYS: The LinkButton will always show an underline at the bottom of its text.
  - UNDERLINE_MODE_ON_HOVER: The LinkButton will show an underline at the bottom of its text when the mouse cursor is over it.
  - UNDERLINE_MODE_NEVER: The LinkButton will never show an underline at the bottom of its text.

