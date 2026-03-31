## TouchScreenButton <- Node2D

TouchScreenButton allows you to create on-screen buttons for touch devices. It's intended for gameplay use, such as a unit you have to touch to move. Unlike Button, TouchScreenButton supports multitouch out of the box. Several TouchScreenButtons can be pressed at the same time with touch input. This node inherits from Node2D. Unlike with Control nodes, you cannot set anchors on it. If you want to create menus or user interfaces, you may want to use Button nodes instead. To make button nodes react to touch events, you can enable `ProjectSettings.input_devices/pointing/emulate_mouse_from_touch` in the Project Settings. You can configure TouchScreenButton to be visible only on touch devices, helping you develop your game both for desktop and mobile devices.

**Props:**
- action: String = ""
- bitmask: BitMap
- passby_press: bool = false
- shape: Shape2D
- shape_centered: bool = true
- shape_visible: bool = true
- texture_normal: Texture2D
- texture_pressed: Texture2D
- visibility_mode: int (TouchScreenButton.VisibilityMode) = 0

- **action**: The button's action. Actions can be handled with InputEventAction.
- **bitmask**: The button's bitmask.
- **passby_press**: If `true`, the `pressed` and `released` signals are emitted whenever a pressed finger goes in and out of the button, even if the pressure started outside the active area of the button. **Note:** This is a "pass-by" (not "bypass") press mode.
- **shape**: The button's shape.
- **shape_centered**: If `true`, the button's shape is centered in the provided texture. If no texture is used, this property has no effect.
- **shape_visible**: If `true`, the button's shape is visible in the editor.
- **texture_normal**: The button's texture for the normal state.
- **texture_pressed**: The button's texture for the pressed state.
- **visibility_mode**: The button's visibility mode.

**Methods:**
- is_pressed() -> bool - Returns `true` if this button is currently pressed.

**Signals:**
- pressed - Emitted when the button is pressed (down).
- released - Emitted when the button is released (up).

**Enums:**
**VisibilityMode:** VISIBILITY_ALWAYS=0, VISIBILITY_TOUCHSCREEN_ONLY=1
  - VISIBILITY_ALWAYS: Always visible.
  - VISIBILITY_TOUCHSCREEN_ONLY: Visible on touch screens only.

