## Shortcut <- Resource

Shortcuts (also known as hotkeys) are containers of InputEvent resources. They are commonly used to interact with a Control element from an InputEvent. One shortcut can contain multiple InputEvent resources, making it possible to trigger one action with multiple different inputs. **Example:** Capture the [kbd]Ctrl + S[/kbd] shortcut using a Shortcut resource:

**Props:**
- events: Array = []

- **events**: The shortcut's InputEvent array. Generally the InputEvent used is an InputEventKey, though it can be any InputEvent, including an InputEventAction.

**Methods:**
- get_as_text() -> String - Returns the shortcut's first valid InputEvent as a String.
- has_valid_event() -> bool - Returns whether `events` contains an InputEvent which is valid.
- matches_event(event: InputEvent) -> bool - Returns whether any InputEvent in `events` equals `event`. This uses `InputEvent.is_match` to compare events.

