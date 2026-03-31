## ConfirmationDialog <- AcceptDialog

A dialog used for confirmation of actions. This window is similar to AcceptDialog, but pressing its Cancel button can have a different outcome from pressing the OK button. The order of the two buttons varies depending on the host OS. To get cancel action, you can use: **Note:** AcceptDialog is invisible by default. To make it visible, call one of the `popup_*` methods from Window on the node, such as `Window.popup_centered_clamped`.

**Props:**
- cancel_button_text: String = "Cancel"
- min_size: Vector2i = Vector2i(200, 70)
- size: Vector2i = Vector2i(200, 100)
- title: String = "Please Confirm..."

- **cancel_button_text**: The text displayed by the cancel button (see `get_cancel_button`).

**Methods:**
- get_cancel_button() -> Button - Returns the cancel button. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `CanvasItem.visible` property.

