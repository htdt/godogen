## BaseButton <- Control

BaseButton is an abstract base class for GUI buttons. It doesn't display anything by itself.

**Props:**
- action_mode: int (BaseButton.ActionMode) = 1
- button_group: ButtonGroup
- button_mask: int (MouseButtonMask) = 1
- button_pressed: bool = false
- disabled: bool = false
- focus_mode: int (Control.FocusMode) = 2
- keep_pressed_outside: bool = false
- shortcut: Shortcut
- shortcut_feedback: bool = true
- shortcut_in_tooltip: bool = true
- toggle_mode: bool = false

- **action_mode**: Determines when the button is considered clicked.
- **button_group**: The ButtonGroup associated with the button. Not to be confused with node groups. **Note:** The button will be configured as a radio button if a ButtonGroup is assigned to it.
- **button_mask**: Binary mask to choose which mouse buttons this button will respond to. To allow both left-click and right-click, use `MOUSE_BUTTON_MASK_LEFT | MOUSE_BUTTON_MASK_RIGHT`.
- **button_pressed**: If `true`, the button's state is pressed. Means the button is pressed down or toggled (if `toggle_mode` is active). Only works if `toggle_mode` is `true`. **Note:** Changing the value of `button_pressed` will result in `toggled` to be emitted. If you want to change the pressed state without emitting that signal, use `set_pressed_no_signal`.
- **disabled**: If `true`, the button is in disabled state and can't be clicked or toggled. **Note:** If the button is disabled while held down, `button_up` will be emitted.
- **keep_pressed_outside**: If `true`, the button stays pressed when moving the cursor outside the button while pressing it. **Note:** This property only affects the button's visual appearance. Signals will be emitted at the same moment regardless of this property's value.
- **shortcut**: Shortcut associated to the button.
- **shortcut_feedback**: If `true`, the button will highlight for a short amount of time when its shortcut is activated. If `false` and `toggle_mode` is `false`, the shortcut will activate without any visual feedback.
- **shortcut_in_tooltip**: If `true`, the button will add information about its shortcut in the tooltip. This includes the shortcut's events and its `Resource.resource_name`. If both events and name are empty, the shortcut will not be included. **Note:** This property does nothing when the tooltip control is customized using `Control._make_custom_tooltip`.
- **toggle_mode**: If `true`, the button is in toggle mode. Makes the button flip state between pressed and unpressed each time its area is clicked.

**Methods:**
- _pressed() - Called when the button is pressed. If you need to know the button's pressed state (and `toggle_mode` is active), use `_toggled` instead.
- _toggled(toggled_on: bool) - Called when the button is toggled (only if `toggle_mode` is active).
- get_draw_mode() -> int - Returns the visual state used to draw the button. This is useful mainly when implementing your own draw code by either overriding _draw() or connecting to "draw" signal. The visual state of the button is defined by the `DrawMode` enum.
- is_hovered() -> bool - Returns `true` if the mouse has entered the button and has not left it yet.
- set_pressed_no_signal(pressed: bool) - Changes the `button_pressed` state of the button, without emitting `toggled`. Use when you just want to change the state of the button without sending the pressed event (e.g. when initializing scene). Only works if `toggle_mode` is `true`. **Note:** This method doesn't unpress other buttons in `button_group`.

**Signals:**
- button_down - Emitted when the button starts being held down.
- button_up - Emitted when the button stops being held down.
- pressed - Emitted when the button is toggled or pressed. This is on `button_down` if `action_mode` is `ACTION_MODE_BUTTON_PRESS` and on `button_up` otherwise. If you need to know the button's pressed state (and `toggle_mode` is active), use `toggled` instead.
- toggled(toggled_on: bool) - Emitted when the button was just toggled between pressed and normal states (only if `toggle_mode` is active). The new state is contained in the `toggled_on` argument.

**Enums:**
**DrawMode:** DRAW_NORMAL=0, DRAW_PRESSED=1, DRAW_HOVER=2, DRAW_DISABLED=3, DRAW_HOVER_PRESSED=4
  - DRAW_NORMAL: The normal state (i.e. not pressed, not hovered, not toggled and enabled) of buttons.
  - DRAW_PRESSED: The state of buttons are pressed.
  - DRAW_HOVER: The state of buttons are hovered.
  - DRAW_DISABLED: The state of buttons are disabled.
  - DRAW_HOVER_PRESSED: The state of buttons are both hovered and pressed.
**ActionMode:** ACTION_MODE_BUTTON_PRESS=0, ACTION_MODE_BUTTON_RELEASE=1
  - ACTION_MODE_BUTTON_PRESS: Require just a press to consider the button clicked.
  - ACTION_MODE_BUTTON_RELEASE: Require a press and a subsequent release before considering the button clicked.

