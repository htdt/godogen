## ButtonGroup <- Resource

A group of BaseButton-derived buttons. The buttons in a ButtonGroup are treated like radio buttons: No more than one button can be pressed at a time. Some types of buttons (such as CheckBox) may have a special appearance in this state. Every member of a ButtonGroup should have `BaseButton.toggle_mode` set to `true`.

**Props:**
- allow_unpress: bool = false
- resource_local_to_scene: bool = true

- **allow_unpress**: If `true`, it is possible to unpress all buttons in this ButtonGroup.

**Methods:**
- get_buttons() -> BaseButton[] - Returns an Array of Buttons who have this as their ButtonGroup (see `BaseButton.button_group`).
- get_pressed_button() -> BaseButton - Returns the current pressed button.

**Signals:**
- pressed(button: BaseButton) - Emitted when one of the buttons of the group is pressed.

