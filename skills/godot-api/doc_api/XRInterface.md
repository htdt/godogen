## XRInterface <- RefCounted

This class needs to be implemented to make an AR or VR platform available to Godot and these should be implemented as C++ modules or GDExtension modules. Part of the interface is exposed to GDScript so you can detect, enable and configure an AR or VR platform. Interfaces should be written in such a way that simply enabling them will give us a working setup. You can query the available interfaces through XRServer.

**Props:**
- ar_is_anchor_detection_enabled: bool = false
- environment_blend_mode: int (XRInterface.EnvironmentBlendMode) = 0
- interface_is_primary: bool = false
- xr_play_area_mode: int (XRInterface.PlayAreaMode) = 0

- **ar_is_anchor_detection_enabled**: On an AR interface, `true` if anchor detection is enabled.
- **environment_blend_mode**: Specify how XR should blend in the environment. This is specific to certain AR and passthrough devices where camera images are blended in by the XR compositor.
- **interface_is_primary**: `true` if this is the primary interface.
- **xr_play_area_mode**: The play area mode for this interface.

**Methods:**
- get_camera_feed_id() -> int - If this is an AR interface that requires displaying a camera feed as the background, this method returns the feed ID in the CameraServer for this interface.
- get_capabilities() -> int - Returns a combination of `Capabilities` flags providing information about the capabilities of this interface.
- get_name() -> StringName - Returns the name of this interface (`"OpenXR"`, `"OpenVR"`, `"OpenHMD"`, `"ARKit"`, etc.).
- get_play_area() -> PackedVector3Array - Returns an array of vectors that represent the physical play area mapped to the virtual space around the XROrigin3D point. The points form a convex polygon that can be used to react to or visualize the play area. This returns an empty array if this feature is not supported or if the information is not yet available.
- get_projection_for_view(view: int, aspect: float, near: float, far: float) -> Projection - Returns the projection matrix for a view/eye.
- get_render_target_size() -> Vector2 - Returns the resolution at which we should render our intermediate results before things like lens distortion are applied by the VR platform.
- get_supported_environment_blend_modes() -> Array - Returns the an array of supported environment blend modes, see `XRInterface.EnvironmentBlendMode`.
- get_system_info() -> Dictionary - Returns a Dictionary with extra system info. Interfaces are expected to return `XRRuntimeName` and `XRRuntimeVersion` providing info about the used XR runtime. Additional entries may be provided specific to an interface. **Note:**This information may only be available after `initialize` was successfully called.
- get_tracking_status() -> int - If supported, returns the status of our tracking. This will allow you to provide feedback to the user whether there are issues with positional tracking.
- get_transform_for_view(view: int, cam_transform: Transform3D) -> Transform3D - Returns the transform for a view/eye. `view` is the view/eye index. `cam_transform` is the transform that maps device coordinates to scene coordinates, typically the `Node3D.global_transform` of the current XROrigin3D.
- get_view_count() -> int - Returns the number of views that need to be rendered for this device. 1 for Monoscopic, 2 for Stereoscopic.
- initialize() -> bool - Call this to initialize this interface. The first interface that is initialized is identified as the primary interface and it will be used for rendering output. After initializing the interface you want to use you then need to enable the AR/VR mode of a viewport and rendering should commence. **Note:** You must enable the XR mode on the main viewport for any device that uses the main output of Godot, such as for mobile VR. If you do this for a platform that handles its own output (such as OpenVR) Godot will show just one eye without distortion on screen. Alternatively, you can add a separate viewport node to your scene and enable AR/VR on that viewport. It will be used to output to the HMD, leaving you free to do anything you like in the main window, such as using a separate camera as a spectator camera or rendering something completely different. While currently not used, you can activate additional interfaces. You may wish to do this if you want to track controllers from other platforms. However, at this point in time only one interface can render to an HMD.
- is_initialized() -> bool - Returns `true` if this interface has been initialized.
- is_passthrough_enabled() -> bool - Returns `true` if passthrough is enabled.
- is_passthrough_supported() -> bool - Returns `true` if this interface supports passthrough.
- set_environment_blend_mode(mode: int) -> bool - Sets the active environment blend mode. `mode` is the environment blend mode starting with the next frame. **Note:** Not all runtimes support all environment blend modes, so it is important to check this at startup. For example:
- set_play_area_mode(mode: int) -> bool - Sets the active play area mode, will return `false` if the mode can't be used with this interface. **Note:** Changing this after the interface has already been initialized can be jarring for the player, so it's recommended to recenter on the HMD with `XRServer.center_on_hmd` (if switching to `XRInterface.XR_PLAY_AREA_STAGE`) or make the switch during a scene change.
- start_passthrough() -> bool - Starts passthrough, will return `false` if passthrough couldn't be started. **Note:** The viewport used for XR must have a transparent background, otherwise passthrough may not properly render.
- stop_passthrough() - Stops passthrough.
- supports_play_area_mode(mode: int) -> bool - Call this to find out if a given play area mode is supported by this interface.
- trigger_haptic_pulse(action_name: String, tracker_name: StringName, frequency: float, amplitude: float, duration_sec: float, delay_sec: float) - Triggers a haptic pulse on a device associated with this interface. `action_name` is the name of the action for this pulse. `tracker_name` is optional and can be used to direct the pulse to a specific device provided that device is bound to this haptic. `frequency` is the frequency of the pulse, set to `0.0` to have the system use a default frequency. `amplitude` is the amplitude of the pulse between `0.0` and `1.0`. `duration_sec` is the duration of the pulse in seconds. `delay_sec` is a delay in seconds before the pulse is given.
- uninitialize() - Turns the interface off.

**Signals:**
- play_area_changed(mode: int) - Emitted when the play area is changed. This can be a result of the player resetting the boundary or entering a new play area, the player changing the play area mode, the world scale changing or the player resetting their headset orientation.

**Enums:**
**Capabilities:** XR_NONE=0, XR_MONO=1, XR_STEREO=2, XR_QUAD=4, XR_VR=8, XR_AR=16, XR_EXTERNAL=32
  - XR_NONE: No XR capabilities.
  - XR_MONO: This interface can work with normal rendering output (non-HMD based AR).
  - XR_STEREO: This interface supports stereoscopic rendering.
  - XR_QUAD: This interface supports quad rendering (not yet supported by Godot).
  - XR_VR: This interface supports VR.
  - XR_AR: This interface supports AR (video background and real world tracking).
  - XR_EXTERNAL: This interface outputs to an external device. If the main viewport is used, the on screen output is an unmodified buffer of either the left or right eye (stretched if the viewport size is not changed to the same aspect ratio of `get_render_target_size`). Using a separate viewport node frees up the main viewport for other purposes.
**TrackingStatus:** XR_NORMAL_TRACKING=0, XR_EXCESSIVE_MOTION=1, XR_INSUFFICIENT_FEATURES=2, XR_UNKNOWN_TRACKING=3, XR_NOT_TRACKING=4
  - XR_NORMAL_TRACKING: Tracking is behaving as expected.
  - XR_EXCESSIVE_MOTION: Tracking is hindered by excessive motion (the player is moving faster than tracking can keep up).
  - XR_INSUFFICIENT_FEATURES: Tracking is hindered by insufficient features, it's too dark (for camera-based tracking), player is blocked, etc.
  - XR_UNKNOWN_TRACKING: We don't know the status of the tracking or this interface does not provide feedback.
  - XR_NOT_TRACKING: Tracking is not functional (camera not plugged in or obscured, lighthouses turned off, etc.).
**PlayAreaMode:** XR_PLAY_AREA_UNKNOWN=0, XR_PLAY_AREA_3DOF=1, XR_PLAY_AREA_SITTING=2, XR_PLAY_AREA_ROOMSCALE=3, XR_PLAY_AREA_STAGE=4, XR_PLAY_AREA_CUSTOM=2147483647
  - XR_PLAY_AREA_UNKNOWN: Play area mode not set or not available.
  - XR_PLAY_AREA_3DOF: Play area only supports orientation tracking, no positional tracking, area will center around player.
  - XR_PLAY_AREA_SITTING: Player is in seated position, limited positional tracking, fixed guardian around player.
  - XR_PLAY_AREA_ROOMSCALE: Player is free to move around, full positional tracking.
  - XR_PLAY_AREA_STAGE: Same as `XR_PLAY_AREA_ROOMSCALE` but origin point is fixed to the center of the physical space. In this mode, system-level recentering may be disabled, requiring the use of `XRServer.center_on_hmd`.
  - XR_PLAY_AREA_CUSTOM: Custom play area set by a GDExtension.
**EnvironmentBlendMode:** XR_ENV_BLEND_MODE_OPAQUE=0, XR_ENV_BLEND_MODE_ADDITIVE=1, XR_ENV_BLEND_MODE_ALPHA_BLEND=2
  - XR_ENV_BLEND_MODE_OPAQUE: Opaque blend mode. This is typically used for VR devices.
  - XR_ENV_BLEND_MODE_ADDITIVE: Additive blend mode. This is typically used for AR devices or VR devices with passthrough.
  - XR_ENV_BLEND_MODE_ALPHA_BLEND: Alpha blend mode. This is typically used for AR or VR devices with passthrough capabilities. The alpha channel controls how much of the passthrough is visible. Alpha of 0.0 means the passthrough is visible and this pixel works in ADDITIVE mode. Alpha of 1.0 means that the passthrough is not visible and this pixel works in OPAQUE mode.
**VRSTextureFormat:** XR_VRS_TEXTURE_FORMAT_UNIFIED=0, XR_VRS_TEXTURE_FORMAT_FRAGMENT_SHADING_RATE=1, XR_VRS_TEXTURE_FORMAT_FRAGMENT_DENSITY_MAP=2
  - XR_VRS_TEXTURE_FORMAT_UNIFIED: The texture format is the same as returned by `XRVRS.make_vrs_texture`.
  - XR_VRS_TEXTURE_FORMAT_FRAGMENT_SHADING_RATE: The texture format is the same as expected by the Vulkan `VK_KHR_fragment_shading_rate` extension.
  - XR_VRS_TEXTURE_FORMAT_FRAGMENT_DENSITY_MAP: The texture format is the same as expected by the Vulkan `VK_EXT_fragment_density_map` extension.

