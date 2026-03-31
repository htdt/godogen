## InputEventShortcut <- InputEvent

InputEventShortcut is a special event that can be received in `Node._input`, `Node._shortcut_input`, and `Node._unhandled_input`. It is typically sent by the editor's Command Palette to trigger actions, but can also be sent manually using `Viewport.push_input`.

**Props:**
- shortcut: Shortcut

- **shortcut**: The Shortcut represented by this event. Its `Shortcut.matches_event` method will always return `true` for this event.

