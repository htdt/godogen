## InputEventJoypadMotion <- InputEvent

Stores information about joystick motions. One InputEventJoypadMotion represents one axis at a time. For gamepad buttons, see InputEventJoypadButton.

**Props:**
- axis: int (JoyAxis) = 0
- axis_value: float = 0.0

- **axis**: Axis identifier.
- **axis_value**: Current position of the joystick on the given axis. The value ranges from `-1.0` to `1.0`. A value of `0` means the axis is in its resting position.

