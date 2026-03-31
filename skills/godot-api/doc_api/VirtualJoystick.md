## VirtualJoystick <- Control

A customizable on-screen joystick control designed for touchscreen devices. It allows users to provide directional input by dragging a virtual tip within a defined circular area. This control can simulate directional actions (see `action_up`, `action_down`, `action_left`, and `action_right`), which are triggered when the joystick is moved in the corresponding directions.

**Props:**
- action_down: StringName = &"ui_down"
- action_left: StringName = &"ui_left"
- action_right: StringName = &"ui_right"
- action_up: StringName = &"ui_up"
- clampzone_ratio: float = 1.0
- deadzone_ratio: float = 0.0
- initial_offset_ratio: Vector2 = Vector2(0.5, 0.5)
- joystick_mode: int (VirtualJoystick.JoystickMode) = 0
- joystick_size: float = 100.0
- tip_size: float = 50.0
- visibility_mode: int (VirtualJoystick.VisibilityMode) = 0

- **action_down**: The action to trigger when the joystick is moved down.
- **action_left**: The action to trigger when the joystick is moved left.
- **action_right**: The action to trigger when the joystick is moved right.
- **action_up**: The action to trigger when the joystick is moved up.
- **clampzone_ratio**: The multiplier applied to the joystick's radius that defines the clamp zone. This zone limits how far the joystick tip can move from its center before being clamped. A value of `1.0` means the tip can move up to the edge of the joystick's visual size. In `JOYSTICK_FOLLOWING` mode, this radius also determines how far the finger can move before the joystick base starts following the touch input.
- **deadzone_ratio**: The ratio of the joystick size that defines the joystick deadzone. The joystick tip must move beyond this ratio before being considered active. This deadzone is applied before triggering input actions and affects the joystick's input vector and all related signals. Note that input actions may also define their own deadzones in the InputMap. If both are set, the joystick deadzone is applied first, followed by the action's deadzone. By default, this value is `0.0`, meaning the joystick does not apply its own deadzone and relies entirely on the InputMap action deadzones.
- **initial_offset_ratio**: The initial position of the joystick as a ratio of the control's size. `(0, 0)` is top-left and `(1, 1)` is bottom-right.
- **joystick_mode**: The joystick mode to use.
- **joystick_size**: The size of the joystick in pixels.
- **tip_size**: The size of the joystick tip in pixels.
- **visibility_mode**: The visibility mode to use.

**Signals:**
- flick_canceled - Emitted when the tip enters the deadzone after being outside of it.
- flicked(input_vector: Vector2) - Emitted when the tip moved outside the deadzone and the joystick is released. The `input_vector` contains the last input direction and strength before release. Its length is between `0.0` and `1.0`.
- pressed - Emitted when the joystick is pressed.
- released(input_vector: Vector2) - Emitted when the joystick is released. The `input_vector` is the final input direction and strength, with a length between `0.0` and `1.0`.
- tapped - Emitted when the joystick is released without moving the tip.

**Enums:**
**JoystickMode:** JOYSTICK_FIXED=0, JOYSTICK_DYNAMIC=1, JOYSTICK_FOLLOWING=2
  - JOYSTICK_FIXED: The joystick doesn't move.
  - JOYSTICK_DYNAMIC: The joystick is moved to the initial touch position as long as it's within the joystick's bounds. It moves back to its original position when released.
  - JOYSTICK_FOLLOWING: The joystick is moved to the initial touch position as long as it's within the joystick's bounds. It will follow the touch input if it goes outside the joystick's range. It moves back to its original position when released.
**VisibilityMode:** VISIBILITY_ALWAYS=0, VISIBILITY_WHEN_TOUCHED=1
  - VISIBILITY_ALWAYS: The joystick is always visible.
  - VISIBILITY_WHEN_TOUCHED: The joystick is only visible when being touched.

