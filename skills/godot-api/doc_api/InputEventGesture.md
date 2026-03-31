## InputEventGesture <- InputEventWithModifiers

InputEventGestures are sent when a user performs a supported gesture on a touch screen. Gestures can't be emulated using mouse, because they typically require multi-touch.

**Props:**
- device: int = 0
- position: Vector2 = Vector2(0, 0)

- **position**: The local gesture position relative to the Viewport. If used in `Control._gui_input`, the position is relative to the current Control that received this gesture.

