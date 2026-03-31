## InputEventJoypadButton <- InputEvent

Input event type for gamepad buttons. For gamepad analog sticks and joysticks, see InputEventJoypadMotion.

**Props:**
- button_index: int (JoyButton) = 0
- pressed: bool = false
- pressure: float = 0.0

- **button_index**: Button identifier. One of the `JoyButton` button constants.
- **pressed**: If `true`, the button's state is pressed. If `false`, the button's state is released.

