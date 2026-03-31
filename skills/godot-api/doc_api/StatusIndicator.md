## StatusIndicator <- Node

**Props:**
- icon: Texture2D
- menu: NodePath = NodePath("")
- tooltip: String = ""
- visible: bool = true

- **icon**: Status indicator icon.
- **menu**: Status indicator native popup menu. If this is set, the `pressed` signal is not emitted. **Note:** Native popup is only supported if NativeMenu supports `NativeMenu.FEATURE_POPUP_MENU` feature.
- **tooltip**: Status indicator tooltip.
- **visible**: If `true`, the status indicator is visible.

**Methods:**
- get_rect() -> Rect2 - Returns the status indicator rectangle in screen coordinates. If this status indicator is not visible, returns an empty Rect2.

**Signals:**
- pressed(mouse_button: int, mouse_position: Vector2i) - Emitted when the status indicator is pressed.

