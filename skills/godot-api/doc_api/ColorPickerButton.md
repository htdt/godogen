## ColorPickerButton <- Button

Encapsulates a ColorPicker, making it accessible by pressing a button. Pressing the button will toggle the ColorPicker's visibility. See also BaseButton which contains common properties and methods associated with this node. **Note:** By default, the button may not be wide enough for the color preview swatch to be visible. Make sure to set `Control.custom_minimum_size` to a big enough value to give the button enough space.

**Props:**
- color: Color = Color(0, 0, 0, 1)
- edit_alpha: bool = true
- edit_intensity: bool = true
- toggle_mode: bool = true

- **color**: The currently selected color.
- **edit_alpha**: If `true`, the alpha channel in the displayed ColorPicker will be visible.
- **edit_intensity**: If `true`, the intensity slider in the displayed ColorPicker will be visible.

**Methods:**
- get_picker() -> ColorPicker - Returns the ColorPicker that this node toggles. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `CanvasItem.visible` property.
- get_popup() -> PopupPanel - Returns the control's PopupPanel which allows you to connect to popup signals. This allows you to handle events when the ColorPicker is shown or hidden. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `Window.visible` property.

**Signals:**
- color_changed(color: Color) - Emitted when the color changes.
- picker_created - Emitted when the ColorPicker is created (the button is pressed for the first time).
- popup_closed - Emitted when the ColorPicker is closed.

