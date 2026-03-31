## Popup <- Window

Popup is a base class for contextual windows and panels with fixed position. It's a modal by default (see `Window.popup_window`) and provides methods for implementing custom popup behavior. **Note:** Popup is invisible by default. To make it visible, call one of the `popup_*` methods from Window on the node, such as `Window.popup_centered_clamped`.

**Props:**
- borderless: bool = true
- maximize_disabled: bool = true
- minimize_disabled: bool = true
- popup_window: bool = true
- popup_wm_hint: bool = true
- transient: bool = true
- unresizable: bool = true
- visible: bool = false
- wrap_controls: bool = true


**Signals:**
- popup_hide - Emitted when the popup is hidden.

