## InputEventPanGesture <- InputEventGesture

Stores information about pan gestures. A pan gesture is performed when the user swipes the touch screen with two fingers. It's typically used for panning/scrolling. **Note:** On Android, this requires the `ProjectSettings.input_devices/pointing/android/enable_pan_and_scale_gestures` project setting to be enabled.

**Props:**
- delta: Vector2 = Vector2(0, 0)

- **delta**: Panning amount since last pan event.

