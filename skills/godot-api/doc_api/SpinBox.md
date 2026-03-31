## SpinBox <- Range

SpinBox is a numerical input text field. It allows entering integers and floating-point numbers. The SpinBox also has up and down buttons that can be clicked to increase or decrease the value. The value can also be changed by dragging the mouse up or down over the SpinBox's arrows. Additionally, mathematical expressions can be entered. These are evaluated when the user presses [kbd]Enter[/kbd] while editing the SpinBox's text field. This uses the Expression class to parse and evaluate the expression. The result of the expression is then set as the value of the SpinBox. Some examples of valid expressions are `5 + 2 * 3`, `pow(2, 4)`, and `PI + sin(0.5)`. Expressions are case-sensitive. **Example:** Create a SpinBox, disable its context menu and set its text alignment to right. See Range class for more options over the SpinBox. **Note:** With the SpinBox's context menu disabled, you can right-click the bottom half of the spinbox to set the value to its minimum, while right-clicking the top half sets the value to its maximum. **Note:** SpinBox relies on an underlying LineEdit node. To theme a SpinBox's background, add theme items for LineEdit and customize them. The LineEdit has the `SpinBoxInnerLineEdit` theme variation, so that you can give it a distinct appearance from regular LineEdits. **Note:** If you want to implement drag and drop for the underlying LineEdit, you can use `Control.set_drag_forwarding` on the node returned by `get_line_edit`.

**Props:**
- alignment: int (HorizontalAlignment) = 0
- custom_arrow_round: bool = false
- custom_arrow_step: float = 0.0
- editable: bool = true
- prefix: String = ""
- select_all_on_focus: bool = false
- size_flags_vertical: int (Control.SizeFlags) = 1
- step: float = 1.0
- suffix: String = ""
- update_on_text_changed: bool = false

- **alignment**: Changes the alignment of the underlying LineEdit.
- **custom_arrow_round**: If `true`, the value will be rounded to a multiple of `custom_arrow_step` when interacting with the arrow buttons. Otherwise, increments the value by `custom_arrow_step` and then rounds it according to `Range.step`.
- **custom_arrow_step**: If not `0`, sets the step when interacting with the arrow buttons of the SpinBox. **Note:** `Range.value` will still be rounded to a multiple of `Range.step`.
- **editable**: If `true`, the SpinBox will be editable. Otherwise, it will be read only.
- **prefix**: Adds the specified prefix string before the numerical value of the SpinBox.
- **select_all_on_focus**: If `true`, the SpinBox will select the whole text when the LineEdit gains focus. Clicking the up and down arrows won't trigger this behavior.
- **suffix**: Adds the specified suffix string after the numerical value of the SpinBox.
- **update_on_text_changed**: Sets the value of the Range for this SpinBox when the LineEdit text is *changed* instead of *submitted*. See `LineEdit.text_changed` and `LineEdit.text_submitted`. **Note:** If set to `true`, this will interfere with entering mathematical expressions in the SpinBox. The SpinBox will try to evaluate the expression as you type, which means symbols like a trailing `+` are removed immediately by the expression being evaluated.

**Methods:**
- apply() - Applies the current value of this SpinBox. This is equivalent to pressing [kbd]Enter[/kbd] while editing the LineEdit used by the SpinBox. This will cause `LineEdit.text_submitted` to be emitted and its currently contained expression to be evaluated.
- get_line_edit() -> LineEdit - Returns the LineEdit instance from this SpinBox. You can use it to access properties and methods of LineEdit. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `CanvasItem.visible` property.

