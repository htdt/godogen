## InputEventMagnifyGesture <- InputEventGesture

Stores the factor of a magnifying touch gesture. This is usually performed when the user pinches the touch screen and used for zooming in/out. **Note:** On Android, this requires the `ProjectSettings.input_devices/pointing/android/enable_pan_and_scale_gestures` project setting to be enabled.

**Props:**
- factor: float = 1.0

- **factor**: The amount (or delta) of the event. This value is closer to `1.0` the slower the gesture is performed.

