## InputEventWithModifiers <- InputEventFromWindow

Stores information about mouse, keyboard, and touch gesture input events. This includes information about which modifier keys are pressed, such as [kbd]Shift[/kbd] or [kbd]Alt[/kbd]. See `Node._input`. **Note:** Modifier keys are considered modifiers only when used in combination with another key. As a result, their corresponding member variables, such as `ctrl_pressed`, will return `false` if the key is pressed on its own.

**Props:**
- alt_pressed: bool = false
- command_or_control_autoremap: bool = false
- ctrl_pressed: bool = false
- device: int = 16
- meta_pressed: bool = false
- shift_pressed: bool = false

- **alt_pressed**: State of the [kbd]Alt[/kbd] modifier.
- **command_or_control_autoremap**: Automatically use [kbd]Meta[/kbd] ([kbd]Cmd[/kbd]) on macOS and [kbd]Ctrl[/kbd] on other platforms. If `true`, `ctrl_pressed` and `meta_pressed` cannot be set.
- **ctrl_pressed**: State of the [kbd]Ctrl[/kbd] modifier.
- **meta_pressed**: State of the [kbd]Meta[/kbd] modifier. On Windows and Linux, this represents the Windows key (sometimes called "meta" or "super" on Linux). On macOS, this represents the Command key.
- **shift_pressed**: State of the [kbd]Shift[/kbd] modifier.

**Methods:**
- get_modifiers_mask() -> int - Returns the keycode combination of modifier keys.
- is_command_or_control_pressed() -> bool - On macOS, returns `true` if [kbd]Meta[/kbd] ([kbd]Cmd[/kbd]) is pressed. On other platforms, returns `true` if [kbd]Ctrl[/kbd] is pressed.

