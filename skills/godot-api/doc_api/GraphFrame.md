## GraphFrame <- GraphElement

GraphFrame is a special GraphElement to which other GraphElements can be attached. It can be configured to automatically resize to enclose all attached GraphElements. If the frame is moved, all the attached GraphElements inside it will be moved as well. A GraphFrame is always kept behind the connection layer and other GraphElements inside a GraphEdit.

**Props:**
- autoshrink_enabled: bool = true
- autoshrink_margin: int = 40
- drag_margin: int = 16
- mouse_filter: int (Control.MouseFilter) = 0
- tint_color: Color = Color(0.3, 0.3, 0.3, 0.75)
- tint_color_enabled: bool = false
- title: String = ""

- **autoshrink_enabled**: If `true`, the frame's rect will be adjusted automatically to enclose all attached GraphElements.
- **autoshrink_margin**: The margin around the attached nodes that is used to calculate the size of the frame when `autoshrink_enabled` is `true`.
- **drag_margin**: The margin inside the frame that can be used to drag the frame.
- **tint_color**: The color of the frame when `tint_color_enabled` is `true`.
- **tint_color_enabled**: If `true`, the tint color will be used to tint the frame.
- **title**: Title of the frame.

**Methods:**
- get_titlebar_hbox() -> HBoxContainer - Returns the HBoxContainer used for the title bar, only containing a Label for displaying the title by default. This can be used to add custom controls to the title bar such as option or close buttons.

**Signals:**
- autoshrink_changed - Emitted when `autoshrink_enabled` or `autoshrink_margin` changes.

