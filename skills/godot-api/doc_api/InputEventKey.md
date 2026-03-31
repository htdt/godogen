## InputEventKey <- InputEventWithModifiers

An input event for keys on a keyboard. Supports key presses, key releases and `echo` events. It can also be received in `Node._unhandled_key_input`. **Note:** Events received from the keyboard usually have all properties set. Event mappings should have only one of the `keycode`, `physical_keycode` or `unicode` set. When events are compared, properties are checked in the following priority - `keycode`, `physical_keycode` and `unicode`. Events with the first matching value will be considered equal.

**Props:**
- echo: bool = false
- key_label: int (Key) = 0
- keycode: int (Key) = 0
- location: int (KeyLocation) = 0
- physical_keycode: int (Key) = 0
- pressed: bool = false
- unicode: int = 0

- **echo**: If `true`, the key was already pressed before this event. An echo event is a repeated key event sent when the user is holding down the key. **Note:** The rate at which echo events are sent is typically around 20 events per second (after holding down the key for roughly half a second). However, the key repeat delay/speed can be changed by the user or disabled entirely in the operating system settings. To ensure your project works correctly on all configurations, do not assume the user has a specific key repeat configuration in your project's behavior.
- **key_label**: Represents the localized label printed on the key in the current keyboard layout, which corresponds to one of the `Key` constants or any valid Unicode character. Key labels are meant for key prompts. For keyboard layouts with a single label on the key, it is equivalent to `keycode`. To get a human-readable representation of the InputEventKey, use `OS.get_keycode_string(event.key_label)` where `event` is the InputEventKey. [codeblock lang=text] +-----+ +-----+ | Q | | Q | - "Q" - keycode | Й | | ض | - "Й" and "ض" - key_label +-----+ +-----+ [/codeblock]
- **keycode**: Latin label printed on the key in the current keyboard layout, which corresponds to one of the `Key` constants. Key codes are meant for shortcuts expressed with a standard Latin keyboard, such as [kbd]Ctrl + S[/kbd] for a "Save" shortcut. To get a human-readable representation of the InputEventKey, use `OS.get_keycode_string(event.keycode)` where `event` is the InputEventKey. [codeblock lang=text] +-----+ +-----+ | Q | | Q | - "Q" - keycode | Й | | ض | - "Й" and "ض" - key_label +-----+ +-----+ [/codeblock]
- **location**: Represents the location of a key which has both left and right versions, such as [kbd]Shift[/kbd] or [kbd]Alt[/kbd].
- **physical_keycode**: Represents the physical location of a key on the 101/102-key US QWERTY keyboard, which corresponds to one of the `Key` constants. Physical key codes meant for game input, such as WASD movement, where only the location of the keys is important. To get a human-readable representation of the InputEventKey, use `OS.get_keycode_string` in combination with `DisplayServer.keyboard_get_keycode_from_physical` or `DisplayServer.keyboard_get_label_from_physical`:
- **pressed**: If `true`, the key's state is pressed. If `false`, the key's state is released.
- **unicode**: The key Unicode character code (when relevant), shifted by modifier keys. Unicode character codes for composite characters and complex scripts may not be available unless IME input mode is active. See `Window.set_ime_active` for more information. Unicode character codes are meant for text input. **Note:** This property is set by the engine only for a pressed event. If the event is sent by an IME or a virtual keyboard, no corresponding key released event is sent.

**Methods:**
- as_text_key_label() -> String - Returns a String representation of the event's `key_label` and modifiers.
- as_text_keycode() -> String - Returns a String representation of the event's `keycode` and modifiers.
- as_text_location() -> String - Returns a String representation of the event's `location`. This will be a blank string if the event is not specific to a location.
- as_text_physical_keycode() -> String - Returns a String representation of the event's `physical_keycode` and modifiers.
- get_key_label_with_modifiers() -> int - Returns the localized key label combined with modifier keys such as [kbd]Shift[/kbd] or [kbd]Alt[/kbd]. See also InputEventWithModifiers. To get a human-readable representation of the InputEventKey with modifiers, use `OS.get_keycode_string(event.get_key_label_with_modifiers())` where `event` is the InputEventKey.
- get_keycode_with_modifiers() -> int - Returns the Latin keycode combined with modifier keys such as [kbd]Shift[/kbd] or [kbd]Alt[/kbd]. See also InputEventWithModifiers. To get a human-readable representation of the InputEventKey with modifiers, use `OS.get_keycode_string(event.get_keycode_with_modifiers())` where `event` is the InputEventKey.
- get_physical_keycode_with_modifiers() -> int - Returns the physical keycode combined with modifier keys such as [kbd]Shift[/kbd] or [kbd]Alt[/kbd]. See also InputEventWithModifiers. To get a human-readable representation of the InputEventKey with modifiers, use `OS.get_keycode_string(event.get_physical_keycode_with_modifiers())` where `event` is the InputEventKey.

