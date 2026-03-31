## AudioListener3D <- Node3D

Once added to the scene tree and enabled using `make_current`, this node will override the location sounds are heard from. This can be used to listen from a location different from the Camera3D.

**Props:**
- doppler_tracking: int (AudioListener3D.DopplerTracking) = 0

- **doppler_tracking**: If not `DOPPLER_TRACKING_DISABLED`, this listener will simulate the for objects changed in particular `_process` methods. **Note:** The Doppler effect will only be heard on AudioStreamPlayer3Ds if `AudioStreamPlayer3D.doppler_tracking` is not set to `AudioStreamPlayer3D.DOPPLER_TRACKING_DISABLED`.

**Methods:**
- clear_current() - Disables the listener to use the current camera's listener instead.
- get_listener_transform() -> Transform3D - Returns the listener's global orthonormalized Transform3D.
- is_current() -> bool - Returns `true` if the listener was made current using `make_current`, `false` otherwise. **Note:** There may be more than one AudioListener3D marked as "current" in the scene tree, but only the one that was made current last will be used.
- make_current() - Enables the listener. This will override the current camera's listener.

**Enums:**
**DopplerTracking:** DOPPLER_TRACKING_DISABLED=0, DOPPLER_TRACKING_IDLE_STEP=1, DOPPLER_TRACKING_PHYSICS_STEP=2
  - DOPPLER_TRACKING_DISABLED: Disables simulation (default).
  - DOPPLER_TRACKING_IDLE_STEP: Simulate by tracking positions of objects that are changed in `_process`. Changes in the relative velocity of this listener compared to those objects affect how audio is perceived (changing the audio's `AudioStreamPlayer3D.pitch_scale`).
  - DOPPLER_TRACKING_PHYSICS_STEP: Simulate by tracking positions of objects that are changed in `_physics_process`. Changes in the relative velocity of this listener compared to those objects affect how audio is perceived (changing the audio's `AudioStreamPlayer3D.pitch_scale`).

