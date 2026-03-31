## ReferenceRect <- Control

A rectangular box that displays only a colored border around its rectangle (see `Control.get_rect`). It can be used to visualize the extents of a Control node, for testing purposes.

**Props:**
- border_color: Color = Color(1, 0, 0, 1)
- border_width: float = 1.0
- editor_only: bool = true

- **border_color**: Sets the border color of the ReferenceRect.
- **border_width**: Sets the border width of the ReferenceRect. The border grows both inwards and outwards with respect to the rectangle box.
- **editor_only**: If `true`, the ReferenceRect will only be visible while in editor. Otherwise, ReferenceRect will be visible in the running project.

