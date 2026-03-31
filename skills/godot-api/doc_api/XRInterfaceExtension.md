## XRInterfaceExtension <- XRInterface

External XR interface plugins should inherit from this class.

**Methods:**
- _end_frame() - Called if interface is active and queues have been submitted.
- _get_anchor_detection_is_enabled() -> bool - Return `true` if anchor detection is enabled for this interface.
- _get_camera_feed_id() -> int - Returns the camera feed ID for the CameraFeed registered with the CameraServer that should be presented as the background on an AR capable device (if applicable).
- _get_camera_transform() -> Transform3D - Returns the Transform3D that positions the XRCamera3D in the world.
- _get_capabilities() -> int - Returns the capabilities of this interface.
- _get_color_texture() -> RID - Return color texture into which to render (if applicable).
- _get_depth_texture() -> RID - Return depth texture into which to render (if applicable).
- _get_name() -> StringName - Returns the name of this interface.
- _get_play_area() -> PackedVector3Array - Returns a PackedVector3Array that represents the play areas boundaries (if applicable).
- _get_play_area_mode() -> int - Returns the play area mode that sets up our play area.
- _get_projection_for_view(view: int, aspect: float, z_near: float, z_far: float) -> PackedFloat64Array - Returns the projection matrix for the given view as a PackedFloat64Array.
- _get_render_target_size() -> Vector2 - Returns the size of our render target for this interface, this overrides the size of the Viewport marked as the xr viewport.
- _get_suggested_pose_names(tracker_name: StringName) -> PackedStringArray - Returns a PackedStringArray with pose names configured by this interface. Note that user configuration can override this list.
- _get_suggested_tracker_names() -> PackedStringArray - Returns a PackedStringArray with tracker names configured by this interface. Note that user configuration can override this list.
- _get_system_info() -> Dictionary - Returns a Dictionary with system information related to this interface.
- _get_tracking_status() -> int - Returns the current status of our tracking.
- _get_transform_for_view(view: int, cam_transform: Transform3D) -> Transform3D - Returns a Transform3D for a given view.
- _get_velocity_texture() -> RID - Return velocity texture into which to render (if applicable).
- _get_view_count() -> int - Returns the number of views this interface requires, 1 for mono, 2 for stereoscopic.
- _get_vrs_texture() -> RID
- _get_vrs_texture_format() -> int - Returns the format of the texture returned by `_get_vrs_texture`.
- _initialize() -> bool - Initializes the interface, returns `true` on success.
- _is_initialized() -> bool - Returns `true` if this interface has been initialized.
- _post_draw_viewport(render_target: RID, screen_rect: Rect2) - Called after the XR Viewport draw logic has completed.
- _pre_draw_viewport(render_target: RID) -> bool - Called if this is our primary XRInterfaceExtension before we start processing a Viewport for every active XR Viewport, returns `true` if that viewport should be rendered. An XR interface may return `false` if the user has taken off their headset and we can pause rendering.
- _pre_render() - Called if this XRInterfaceExtension is active before rendering starts. Most XR interfaces will sync tracking at this point in time.
- _process() - Called if this XRInterfaceExtension is active before our physics and game process is called. Most XR interfaces will update its XRPositionalTrackers at this point in time.
- _set_anchor_detection_is_enabled(enabled: bool) - Enables anchor detection on this interface if supported.
- _set_play_area_mode(mode: int) -> bool - Set the play area mode for this interface.
- _supports_play_area_mode(mode: int) -> bool - Returns `true` if this interface supports this play area mode.
- _trigger_haptic_pulse(action_name: String, tracker_name: StringName, frequency: float, amplitude: float, duration_sec: float, delay_sec: float) - Triggers a haptic pulse to be emitted on the specified tracker.
- _uninitialize() - Uninitialize the interface.
- add_blit(render_target: RID, src_rect: Rect2, dst_rect: Rect2i, use_layer: bool, layer: int, apply_lens_distortion: bool, eye_center: Vector2, k1: float, k2: float, upscale: float, aspect_ratio: float) - Blits our render results to screen optionally applying lens distortion. This can only be called while processing `_commit_views`.
- get_color_texture() -> RID
- get_depth_texture() -> RID
- get_render_target_texture(render_target: RID) -> RID - Returns a valid RID for a texture to which we should render the current frame if supported by the interface.
- get_velocity_texture() -> RID

