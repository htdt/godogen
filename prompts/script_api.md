# Godot API Reference

## AABB

A 3D axis-aligned bounding box.

**Props:**
- end: Vector3 = Vector3(0, 0, 0)
- position: Vector3 = Vector3(0, 0, 0)
- size: Vector3 = Vector3(0, 0, 0)

**Methods:**
- abs() -> AABB
- encloses(with: AABB) -> bool
- expand(to_point: Vector3) -> AABB
- get_center() -> Vector3
- get_endpoint(idx: int) -> Vector3
- get_longest_axis() -> Vector3
- get_longest_axis_index() -> int
- get_longest_axis_size() -> float
- get_shortest_axis() -> Vector3
- get_shortest_axis_index() -> int
- get_shortest_axis_size() -> float
- get_support(direction: Vector3) -> Vector3
- get_volume() -> float
- grow(by: float) -> AABB
- has_point(point: Vector3) -> bool
- has_surface() -> bool
- has_volume() -> bool
- intersection(with: AABB) -> AABB
- intersects(with: AABB) -> bool
- intersects_plane(plane: Plane) -> bool
- intersects_ray(from: Vector3, dir: Vector3) -> Variant
- intersects_segment(from: Vector3, to: Vector3) -> Variant
- is_equal_approx(aabb: AABB) -> bool
- is_finite() -> bool
- merge(with: AABB) -> AABB


## AnimatableBody2D <- StaticBody2D

A 2D physics body that can't be moved by external forces. When moved manually, it affects other bodies in its path.

**Props:**
- sync_to_physics: bool = true


## AnimatableBody3D <- StaticBody3D

A 3D physics body that can't be moved by external forces. When moved manually, it affects other bodies in its path.

**Props:**
- sync_to_physics: bool = true


## AnimatedSprite2D <- Node2D

Sprite node that contains multiple textures as frames to play for animation.

**Props:**
- animation: StringName = &"default"
- autoplay: String = ""
- centered: bool = true
- flip_h: bool = false
- flip_v: bool = false
- frame: int = 0
- frame_progress: float = 0.0
- offset: Vector2 = Vector2(0, 0)
- speed_scale: float = 1.0
- sprite_frames: SpriteFrames

**Methods:**
- get_playing_speed() -> float
- is_playing() -> bool
- pause()
- play(name: StringName = &"", custom_speed: float = 1.0, from_end: bool = false)
- play_backwards(name: StringName = &"")
- set_frame_and_progress(frame: int, progress: float)
- stop()

**Signals:**
- animation_changed
- animation_finished
- animation_looped
- frame_changed
- sprite_frames_changed


## AnimatedSprite3D <- SpriteBase3D

2D sprite node in 3D world, that can use multiple 2D textures for animation.

**Props:**
- animation: StringName = &"default"
- autoplay: String = ""
- frame: int = 0
- frame_progress: float = 0.0
- speed_scale: float = 1.0
- sprite_frames: SpriteFrames

**Methods:**
- get_playing_speed() -> float
- is_playing() -> bool
- pause()
- play(name: StringName = &"", custom_speed: float = 1.0, from_end: bool = false)
- play_backwards(name: StringName = &"")
- set_frame_and_progress(frame: int, progress: float)
- stop()

**Signals:**
- animation_changed
- animation_finished
- animation_looped
- frame_changed
- sprite_frames_changed


## AnimationMixer <- Node

Base class for AnimationPlayer and AnimationTree.

**Props:**
- active: bool = true
- audio_max_polyphony: int = 32
- callback_mode_discrete: int (AnimationMixer.AnimationCallbackModeDiscrete) = 1
- callback_mode_method: int (AnimationMixer.AnimationCallbackModeMethod) = 0
- callback_mode_process: int (AnimationMixer.AnimationCallbackModeProcess) = 1
- deterministic: bool = false
- reset_on_save: bool = true
- root_motion_local: bool = false
- root_motion_track: NodePath = NodePath("")
- root_node: NodePath = NodePath("..")

**Methods:**
- add_animation_library(name: StringName, library: AnimationLibrary) -> int
- advance(delta: float)
- capture(name: StringName, duration: float, trans_type: int = 0, ease_type: int = 0)
- clear_caches()
- find_animation(animation: Animation) -> StringName
- find_animation_library(animation: Animation) -> StringName
- get_animation(name: StringName) -> Animation
- get_animation_library(name: StringName) -> AnimationLibrary
- get_animation_library_list() -> StringName[]
- get_animation_list() -> PackedStringArray
- get_root_motion_position() -> Vector3
- get_root_motion_position_accumulator() -> Vector3
- get_root_motion_rotation() -> Quaternion
- get_root_motion_rotation_accumulator() -> Quaternion
- get_root_motion_scale() -> Vector3
- get_root_motion_scale_accumulator() -> Vector3
- has_animation(name: StringName) -> bool
- has_animation_library(name: StringName) -> bool
- remove_animation_library(name: StringName)
- rename_animation_library(name: StringName, newname: StringName)

**Signals:**
- animation_finished(anim_name: StringName)
- animation_libraries_updated
- animation_list_changed
- animation_started(anim_name: StringName)
- caches_cleared
- mixer_applied
- mixer_updated

**Enums:**
**AnimationCallbackModeProcess:** ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS=0, ANIMATION_CALLBACK_MODE_PROCESS_IDLE=1, ANIMATION_CALLBACK_MODE_PROCESS_MANUAL=2
**AnimationCallbackModeMethod:** ANIMATION_CALLBACK_MODE_METHOD_DEFERRED=0, ANIMATION_CALLBACK_MODE_METHOD_IMMEDIATE=1
**AnimationCallbackModeDiscrete:** ANIMATION_CALLBACK_MODE_DISCRETE_DOMINANT=0, ANIMATION_CALLBACK_MODE_DISCRETE_RECESSIVE=1, ANIMATION_CALLBACK_MODE_DISCRETE_FORCE_CONTINUOUS=2


## AnimationPlayer <- AnimationMixer

A node used for animation playback.

**Props:**
- assigned_animation: StringName
- autoplay: StringName = &""
- current_animation: StringName = &""
- current_animation_length: float
- current_animation_position: float
- movie_quit_on_finish: bool = false
- playback_auto_capture: bool = true
- playback_auto_capture_duration: float = -1.0
- playback_auto_capture_ease_type: int (Tween.EaseType) = 0
- playback_auto_capture_transition_type: int (Tween.TransitionType) = 0
- playback_default_blend_time: float = 0.0
- speed_scale: float = 1.0

**Methods:**
- animation_get_next(animation_from: StringName) -> StringName
- animation_set_next(animation_from: StringName, animation_to: StringName)
- clear_queue()
- get_blend_time(animation_from: StringName, animation_to: StringName) -> float
- get_method_call_mode() -> int
- get_playing_speed() -> float
- get_process_callback() -> int
- get_queue() -> StringName[]
- get_root() -> NodePath
- get_section_end_time() -> float
- get_section_start_time() -> float
- has_section() -> bool
- is_animation_active() -> bool
- is_playing() -> bool
- pause()
- play(name: StringName = &"", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false)
- play_backwards(name: StringName = &"", custom_blend: float = -1)
- play_section(name: StringName = &"", start_time: float = -1, end_time: float = -1, custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false)
- play_section_backwards(name: StringName = &"", start_time: float = -1, end_time: float = -1, custom_blend: float = -1)
- play_section_with_markers(name: StringName = &"", start_marker: StringName = &"", end_marker: StringName = &"", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false)
- play_section_with_markers_backwards(name: StringName = &"", start_marker: StringName = &"", end_marker: StringName = &"", custom_blend: float = -1)
- play_with_capture(name: StringName = &"", duration: float = -1.0, custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false, trans_type: int = 0, ease_type: int = 0)
- queue(name: StringName)
- reset_section()
- seek(seconds: float, update: bool = false, update_only: bool = false)
- set_blend_time(animation_from: StringName, animation_to: StringName, sec: float)
- set_method_call_mode(mode: int)
- set_process_callback(mode: int)
- set_root(path: NodePath)
- set_section(start_time: float = -1, end_time: float = -1)
- set_section_with_markers(start_marker: StringName = &"", end_marker: StringName = &"")
- stop(keep_state: bool = false)

**Signals:**
- animation_changed(old_name: StringName, new_name: StringName)
- current_animation_changed(name: StringName)

**Enums:**
**AnimationProcessCallback:** ANIMATION_PROCESS_PHYSICS=0, ANIMATION_PROCESS_IDLE=1, ANIMATION_PROCESS_MANUAL=2
**AnimationMethodCallMode:** ANIMATION_METHOD_CALL_DEFERRED=0, ANIMATION_METHOD_CALL_IMMEDIATE=1


## AnimationTree <- AnimationMixer

A node used for advanced animation transitions in an AnimationPlayer.

**Props:**
- advance_expression_base_node: NodePath = NodePath(".")
- anim_player: NodePath = NodePath("")
- callback_mode_discrete: int (AnimationMixer.AnimationCallbackModeDiscrete) = 2
- deterministic: bool = true
- tree_root: AnimationRootNode

**Methods:**
- get_process_callback() -> int
- set_process_callback(mode: int)

**Signals:**
- animation_player_changed

**Enums:**
**AnimationProcessCallback:** ANIMATION_PROCESS_PHYSICS=0, ANIMATION_PROCESS_IDLE=1, ANIMATION_PROCESS_MANUAL=2


## Area2D <- CollisionObject2D

A region of 2D space that detects other CollisionObject2Ds entering or exiting it.

**Props:**
- angular_damp: float = 1.0
- angular_damp_space_override: int (Area2D.SpaceOverride) = 0
- audio_bus_name: StringName = &"Master"
- audio_bus_override: bool = false
- gravity: float = 980.0
- gravity_direction: Vector2 = Vector2(0, 1)
- gravity_point: bool = false
- gravity_point_center: Vector2 = Vector2(0, 1)
- gravity_point_unit_distance: float = 0.0
- gravity_space_override: int (Area2D.SpaceOverride) = 0
- linear_damp: float = 0.1
- linear_damp_space_override: int (Area2D.SpaceOverride) = 0
- monitorable: bool = true
- monitoring: bool = true
- priority: int = 0

**Methods:**
- get_overlapping_areas() -> Area2D[]
- get_overlapping_bodies() -> Node2D[]
- has_overlapping_areas() -> bool
- has_overlapping_bodies() -> bool
- overlaps_area(area: Node) -> bool
- overlaps_body(body: Node) -> bool

**Signals:**
- area_entered(area: Area2D)
- area_exited(area: Area2D)
- area_shape_entered(area_rid: RID, area: Area2D, area_shape_index: int, local_shape_index: int)
- area_shape_exited(area_rid: RID, area: Area2D, area_shape_index: int, local_shape_index: int)
- body_entered(body: Node2D)
- body_exited(body: Node2D)
- body_shape_entered(body_rid: RID, body: Node2D, body_shape_index: int, local_shape_index: int)
- body_shape_exited(body_rid: RID, body: Node2D, body_shape_index: int, local_shape_index: int)

**Enums:**
**SpaceOverride:** SPACE_OVERRIDE_DISABLED=0, SPACE_OVERRIDE_COMBINE=1, SPACE_OVERRIDE_COMBINE_REPLACE=2, SPACE_OVERRIDE_REPLACE=3, SPACE_OVERRIDE_REPLACE_COMBINE=4


## Area3D <- CollisionObject3D

A region of 3D space that detects other CollisionObject3Ds entering or exiting it.

**Props:**
- angular_damp: float = 0.1
- angular_damp_space_override: int (Area3D.SpaceOverride) = 0
- audio_bus_name: StringName = &"Master"
- audio_bus_override: bool = false
- gravity: float = 9.8
- gravity_direction: Vector3 = Vector3(0, -1, 0)
- gravity_point: bool = false
- gravity_point_center: Vector3 = Vector3(0, -1, 0)
- gravity_point_unit_distance: float = 0.0
- gravity_space_override: int (Area3D.SpaceOverride) = 0
- linear_damp: float = 0.1
- linear_damp_space_override: int (Area3D.SpaceOverride) = 0
- monitorable: bool = true
- monitoring: bool = true
- priority: int = 0
- reverb_bus_amount: float = 0.0
- reverb_bus_enabled: bool = false
- reverb_bus_name: StringName = &"Master"
- reverb_bus_uniformity: float = 0.0
- wind_attenuation_factor: float = 0.0
- wind_force_magnitude: float = 0.0
- wind_source_path: NodePath = NodePath("")

**Methods:**
- get_overlapping_areas() -> Area3D[]
- get_overlapping_bodies() -> Node3D[]
- has_overlapping_areas() -> bool
- has_overlapping_bodies() -> bool
- overlaps_area(area: Node) -> bool
- overlaps_body(body: Node) -> bool

**Signals:**
- area_entered(area: Area3D)
- area_exited(area: Area3D)
- area_shape_entered(area_rid: RID, area: Area3D, area_shape_index: int, local_shape_index: int)
- area_shape_exited(area_rid: RID, area: Area3D, area_shape_index: int, local_shape_index: int)
- body_entered(body: Node3D)
- body_exited(body: Node3D)
- body_shape_entered(body_rid: RID, body: Node3D, body_shape_index: int, local_shape_index: int)
- body_shape_exited(body_rid: RID, body: Node3D, body_shape_index: int, local_shape_index: int)

**Enums:**
**SpaceOverride:** SPACE_OVERRIDE_DISABLED=0, SPACE_OVERRIDE_COMBINE=1, SPACE_OVERRIDE_COMBINE_REPLACE=2, SPACE_OVERRIDE_REPLACE=3, SPACE_OVERRIDE_REPLACE_COMBINE=4


## ArrayMesh <- Mesh

Mesh type that provides utility for constructing a surface from arrays.

**Props:**
- blend_shape_mode: int (Mesh.BlendShapeMode) = 1
- custom_aabb: AABB = AABB(0, 0, 0, 0, 0, 0)
- shadow_mesh: ArrayMesh

**Methods:**
- add_blend_shape(name: StringName)
- add_surface_from_arrays(primitive: int, arrays: Array, blend_shapes: Array[] = [], lods: Dictionary = {}, flags: int = 0)
- clear_blend_shapes()
- clear_surfaces()
- get_blend_shape_count() -> int
- get_blend_shape_name(index: int) -> StringName
- lightmap_unwrap(transform: Transform3D, texel_size: float) -> int
- regen_normal_maps()
- set_blend_shape_name(index: int, name: StringName)
- surface_find_by_name(name: String) -> int
- surface_get_array_index_len(surf_idx: int) -> int
- surface_get_array_len(surf_idx: int) -> int
- surface_get_format(surf_idx: int) -> int
- surface_get_name(surf_idx: int) -> String
- surface_get_primitive_type(surf_idx: int) -> int
- surface_remove(surf_idx: int)
- surface_set_name(surf_idx: int, name: String)
- surface_update_attribute_region(surf_idx: int, offset: int, data: PackedByteArray)
- surface_update_skin_region(surf_idx: int, offset: int, data: PackedByteArray)
- surface_update_vertex_region(surf_idx: int, offset: int, data: PackedByteArray)


## AspectRatioContainer <- Container

A container that preserves the proportions of its child controls.

**Props:**
- alignment_horizontal: int (AspectRatioContainer.AlignmentMode) = 1
- alignment_vertical: int (AspectRatioContainer.AlignmentMode) = 1
- ratio: float = 1.0
- stretch_mode: int (AspectRatioContainer.StretchMode) = 2

**Enums:**
**StretchMode:** STRETCH_WIDTH_CONTROLS_HEIGHT=0, STRETCH_HEIGHT_CONTROLS_WIDTH=1, STRETCH_FIT=2, STRETCH_COVER=3
**AlignmentMode:** ALIGNMENT_BEGIN=0, ALIGNMENT_CENTER=1, ALIGNMENT_END=2


## AtlasTexture <- Texture2D

A texture that crops out part of another Texture2D.

**Props:**
- atlas: Texture2D
- filter_clip: bool = false
- margin: Rect2 = Rect2(0, 0, 0, 0)
- region: Rect2 = Rect2(0, 0, 0, 0)
- resource_local_to_scene: bool = false


## AudioStream <- Resource

Base class for audio streams.

**Methods:**
- can_be_sampled() -> bool
- generate_sample() -> AudioSample
- get_length() -> float
- instantiate_playback() -> AudioStreamPlayback
- is_meta_stream() -> bool
- is_monophonic() -> bool

**Signals:**
- parameter_list_changed


## AudioStreamPlayer <- Node

A node for audio playback.

**Props:**
- autoplay: bool = false
- bus: StringName = &"Master"
- max_polyphony: int = 1
- mix_target: int (AudioStreamPlayer.MixTarget) = 0
- pitch_scale: float = 1.0
- playback_type: int (AudioServer.PlaybackType) = 0
- playing: bool = false
- stream: AudioStream
- stream_paused: bool = false
- volume_db: float = 0.0
- volume_linear: float

**Methods:**
- get_playback_position() -> float
- get_stream_playback() -> AudioStreamPlayback
- has_stream_playback() -> bool
- play(from_position: float = 0.0)
- seek(to_position: float)
- stop()

**Signals:**
- finished

**Enums:**
**MixTarget:** MIX_TARGET_STEREO=0, MIX_TARGET_SURROUND=1, MIX_TARGET_CENTER=2


## AudioStreamPlayer2D <- Node2D

Plays positional sound in 2D space.

**Props:**
- area_mask: int = 1
- attenuation: float = 1.0
- autoplay: bool = false
- bus: StringName = &"Master"
- max_distance: float = 2000.0
- max_polyphony: int = 1
- panning_strength: float = 1.0
- pitch_scale: float = 1.0
- playback_type: int (AudioServer.PlaybackType) = 0
- playing: bool = false
- stream: AudioStream
- stream_paused: bool = false
- volume_db: float = 0.0
- volume_linear: float

**Methods:**
- get_playback_position() -> float
- get_stream_playback() -> AudioStreamPlayback
- has_stream_playback() -> bool
- play(from_position: float = 0.0)
- seek(to_position: float)
- stop()

**Signals:**
- finished


## AudioStreamPlayer3D <- Node3D

Plays positional sound in 3D space.

**Props:**
- area_mask: int = 1
- attenuation_filter_cutoff_hz: float = 5000.0
- attenuation_filter_db: float = -24.0
- attenuation_model: int (AudioStreamPlayer3D.AttenuationModel) = 0
- autoplay: bool = false
- bus: StringName = &"Master"
- doppler_tracking: int (AudioStreamPlayer3D.DopplerTracking) = 0
- emission_angle_degrees: float = 45.0
- emission_angle_enabled: bool = false
- emission_angle_filter_attenuation_db: float = -12.0
- max_db: float = 3.0
- max_distance: float = 0.0
- max_polyphony: int = 1
- panning_strength: float = 1.0
- pitch_scale: float = 1.0
- playback_type: int (AudioServer.PlaybackType) = 0
- playing: bool = false
- stream: AudioStream
- stream_paused: bool = false
- unit_size: float = 10.0
- volume_db: float = 0.0
- volume_linear: float

**Methods:**
- get_playback_position() -> float
- get_stream_playback() -> AudioStreamPlayback
- has_stream_playback() -> bool
- play(from_position: float = 0.0)
- seek(to_position: float)
- stop()

**Signals:**
- finished

**Enums:**
**AttenuationModel:** ATTENUATION_INVERSE_DISTANCE=0, ATTENUATION_INVERSE_SQUARE_DISTANCE=1, ATTENUATION_LOGARITHMIC=2, ATTENUATION_DISABLED=3
**DopplerTracking:** DOPPLER_TRACKING_DISABLED=0, DOPPLER_TRACKING_IDLE_STEP=1, DOPPLER_TRACKING_PHYSICS_STEP=2


## AudioStreamWAV <- AudioStream

Stores audio data loaded from WAV files.

**Props:**
- data: PackedByteArray = PackedByteArray()
- format: int (AudioStreamWAV.Format) = 0
- loop_begin: int = 0
- loop_end: int = 0
- loop_mode: int (AudioStreamWAV.LoopMode) = 0
- mix_rate: int = 44100
- stereo: bool = false
- tags: Dictionary = {}

**Methods:**
- load_from_buffer(stream_data: PackedByteArray, options: Dictionary = {}) -> AudioStreamWAV
- load_from_file(path: String, options: Dictionary = {}) -> AudioStreamWAV
- save_to_wav(path: String) -> int

**Enums:**
**Format:** FORMAT_8_BITS=0, FORMAT_16_BITS=1, FORMAT_IMA_ADPCM=2, FORMAT_QOA=3
**LoopMode:** LOOP_DISABLED=0, LOOP_FORWARD=1, LOOP_PINGPONG=2, LOOP_BACKWARD=3


## Basis

A 3×3 matrix for representing 3D rotation and scale.

**Props:**
- x: Vector3 = Vector3(1, 0, 0)
- y: Vector3 = Vector3(0, 1, 0)
- z: Vector3 = Vector3(0, 0, 1)

**Methods:**
- determinant() -> float
- from_euler(euler: Vector3, order: int = 2) -> Basis
- from_scale(scale: Vector3) -> Basis
- get_euler(order: int = 2) -> Vector3
- get_rotation_quaternion() -> Quaternion
- get_scale() -> Vector3
- inverse() -> Basis
- is_conformal() -> bool
- is_equal_approx(b: Basis) -> bool
- is_finite() -> bool
- looking_at(target: Vector3, up: Vector3 = Vector3(0, 1, 0), use_model_front: bool = false) -> Basis
- orthonormalized() -> Basis
- rotated(axis: Vector3, angle: float) -> Basis
- scaled(scale: Vector3) -> Basis
- scaled_local(scale: Vector3) -> Basis
- slerp(to: Basis, weight: float) -> Basis
- tdotx(with: Vector3) -> float
- tdoty(with: Vector3) -> float
- tdotz(with: Vector3) -> float
- transposed() -> Basis

**Enums:**
**Constants:** IDENTITY=Basis(1, 0, 0, 0, 1, 0, 0, 0, 1), FLIP_X=Basis(-1, 0, 0, 0, 1, 0, 0, 0, 1), FLIP_Y=Basis(1, 0, 0, 0, -1, 0, 0, 0, 1), FLIP_Z=Basis(1, 0, 0, 0, 1, 0, 0, 0, -1)


## BoxMesh <- PrimitiveMesh

Generate an axis-aligned box PrimitiveMesh.

**Props:**
- size: Vector3 = Vector3(1, 1, 1)
- subdivide_depth: int = 0
- subdivide_height: int = 0
- subdivide_width: int = 0


## BoxShape3D <- Shape3D

A 3D box shape used for physics collision.

**Props:**
- size: Vector3 = Vector3(1, 1, 1)


## Button <- BaseButton

A themed button that can contain text and an icon.

**Props:**
- alignment: int (HorizontalAlignment) = 1
- autowrap_mode: int (TextServer.AutowrapMode) = 0
- autowrap_trim_flags: int (TextServer.LineBreakFlag) = 128
- clip_text: bool = false
- expand_icon: bool = false
- flat: bool = false
- icon: Texture2D
- icon_alignment: int (HorizontalAlignment) = 0
- language: String = ""
- text: String = ""
- text_direction: int (Control.TextDirection) = 0
- text_overrun_behavior: int (TextServer.OverrunBehavior) = 0
- vertical_icon_alignment: int (VerticalAlignment) = 1


## CPUParticles2D <- Node2D

A CPU-based 2D particle emitter.

**Props:**
- amount: int = 8
- angle_curve: Curve
- angle_max: float = 0.0
- angle_min: float = 0.0
- angular_velocity_curve: Curve
- angular_velocity_max: float = 0.0
- angular_velocity_min: float = 0.0
- anim_offset_curve: Curve
- anim_offset_max: float = 0.0
- anim_offset_min: float = 0.0
- anim_speed_curve: Curve
- anim_speed_max: float = 0.0
- anim_speed_min: float = 0.0
- color: Color = Color(1, 1, 1, 1)
- color_initial_ramp: Gradient
- color_ramp: Gradient
- damping_curve: Curve
- damping_max: float = 0.0
- damping_min: float = 0.0
- direction: Vector2 = Vector2(1, 0)
- draw_order: int (CPUParticles2D.DrawOrder) = 0
- emission_colors: PackedColorArray
- emission_normals: PackedVector2Array
- emission_points: PackedVector2Array
- emission_rect_extents: Vector2
- emission_ring_inner_radius: float
- emission_ring_radius: float
- emission_shape: int (CPUParticles2D.EmissionShape) = 0
- emission_sphere_radius: float
- emitting: bool = true
- explosiveness: float = 0.0
- fixed_fps: int = 0
- fract_delta: bool = true
- gravity: Vector2 = Vector2(0, 980)
- hue_variation_curve: Curve
- hue_variation_max: float = 0.0
- hue_variation_min: float = 0.0
- initial_velocity_max: float = 0.0
- initial_velocity_min: float = 0.0
- lifetime: float = 1.0
- lifetime_randomness: float = 0.0
- linear_accel_curve: Curve
- linear_accel_max: float = 0.0
- linear_accel_min: float = 0.0
- local_coords: bool = false
- one_shot: bool = false
- orbit_velocity_curve: Curve
- orbit_velocity_max: float = 0.0
- orbit_velocity_min: float = 0.0
- particle_flag_align_y: bool = false
- physics_interpolation_mode: int (Node.PhysicsInterpolationMode) = 2
- preprocess: float = 0.0
- radial_accel_curve: Curve
- radial_accel_max: float = 0.0
- radial_accel_min: float = 0.0
- randomness: float = 0.0
- scale_amount_curve: Curve
- scale_amount_max: float = 1.0
- scale_amount_min: float = 1.0
- scale_curve_x: Curve
- scale_curve_y: Curve
- seed: int = 0
- speed_scale: float = 1.0
- split_scale: bool = false
- spread: float = 45.0
- tangential_accel_curve: Curve
- tangential_accel_max: float = 0.0
- tangential_accel_min: float = 0.0
- texture: Texture2D
- use_fixed_seed: bool = false

**Methods:**
- convert_from_particles(particles: Node)
- get_param_curve(param: int) -> Curve
- get_param_max(param: int) -> float
- get_param_min(param: int) -> float
- get_particle_flag(particle_flag: int) -> bool
- request_particles_process(process_time: float)
- restart(keep_seed: bool = false)
- set_param_curve(param: int, curve: Curve)
- set_param_max(param: int, value: float)
- set_param_min(param: int, value: float)
- set_particle_flag(particle_flag: int, enable: bool)

**Signals:**
- finished

**Enums:**
**DrawOrder:** DRAW_ORDER_INDEX=0, DRAW_ORDER_LIFETIME=1
**Parameter:** PARAM_INITIAL_LINEAR_VELOCITY=0, PARAM_ANGULAR_VELOCITY=1, PARAM_ORBIT_VELOCITY=2, PARAM_LINEAR_ACCEL=3, PARAM_RADIAL_ACCEL=4, PARAM_TANGENTIAL_ACCEL=5, PARAM_DAMPING=6, PARAM_ANGLE=7, PARAM_SCALE=8, PARAM_HUE_VARIATION=9, ...
**ParticleFlags:** PARTICLE_FLAG_ALIGN_Y_TO_VELOCITY=0, PARTICLE_FLAG_ROTATE_Y=1, PARTICLE_FLAG_DISABLE_Z=2, PARTICLE_FLAG_MAX=3
**EmissionShape:** EMISSION_SHAPE_POINT=0, EMISSION_SHAPE_SPHERE=1, EMISSION_SHAPE_SPHERE_SURFACE=2, EMISSION_SHAPE_RECTANGLE=3, EMISSION_SHAPE_POINTS=4, EMISSION_SHAPE_DIRECTED_POINTS=5, EMISSION_SHAPE_RING=6, EMISSION_SHAPE_MAX=7


## CPUParticles3D <- GeometryInstance3D

A CPU-based 3D particle emitter.

**Props:**
- amount: int = 8
- angle_curve: Curve
- angle_max: float = 0.0
- angle_min: float = 0.0
- angular_velocity_curve: Curve
- angular_velocity_max: float = 0.0
- angular_velocity_min: float = 0.0
- anim_offset_curve: Curve
- anim_offset_max: float = 0.0
- anim_offset_min: float = 0.0
- anim_speed_curve: Curve
- anim_speed_max: float = 0.0
- anim_speed_min: float = 0.0
- color: Color = Color(1, 1, 1, 1)
- color_initial_ramp: Gradient
- color_ramp: Gradient
- damping_curve: Curve
- damping_max: float = 0.0
- damping_min: float = 0.0
- direction: Vector3 = Vector3(1, 0, 0)
- draw_order: int (CPUParticles3D.DrawOrder) = 0
- emission_box_extents: Vector3
- emission_colors: PackedColorArray = PackedColorArray()
- emission_normals: PackedVector3Array
- emission_points: PackedVector3Array
- emission_ring_axis: Vector3
- emission_ring_cone_angle: float
- emission_ring_height: float
- emission_ring_inner_radius: float
- emission_ring_radius: float
- emission_shape: int (CPUParticles3D.EmissionShape) = 0
- emission_sphere_radius: float
- emitting: bool = true
- explosiveness: float = 0.0
- fixed_fps: int = 0
- flatness: float = 0.0
- fract_delta: bool = true
- gravity: Vector3 = Vector3(0, -9.8, 0)
- hue_variation_curve: Curve
- hue_variation_max: float = 0.0
- hue_variation_min: float = 0.0
- initial_velocity_max: float = 0.0
- initial_velocity_min: float = 0.0
- lifetime: float = 1.0
- lifetime_randomness: float = 0.0
- linear_accel_curve: Curve
- linear_accel_max: float = 0.0
- linear_accel_min: float = 0.0
- local_coords: bool = false
- mesh: Mesh
- one_shot: bool = false
- orbit_velocity_curve: Curve
- orbit_velocity_max: float
- orbit_velocity_min: float
- particle_flag_align_y: bool = false
- particle_flag_disable_z: bool = false
- particle_flag_rotate_y: bool = false
- preprocess: float = 0.0
- radial_accel_curve: Curve
- radial_accel_max: float = 0.0
- radial_accel_min: float = 0.0
- randomness: float = 0.0
- scale_amount_curve: Curve
- scale_amount_max: float = 1.0
- scale_amount_min: float = 1.0
- scale_curve_x: Curve
- scale_curve_y: Curve
- scale_curve_z: Curve
- seed: int = 0
- speed_scale: float = 1.0
- split_scale: bool = false
- spread: float = 45.0
- tangential_accel_curve: Curve
- tangential_accel_max: float = 0.0
- tangential_accel_min: float = 0.0
- use_fixed_seed: bool = false
- visibility_aabb: AABB = AABB(0, 0, 0, 0, 0, 0)

**Methods:**
- capture_aabb() -> AABB
- convert_from_particles(particles: Node)
- get_param_curve(param: int) -> Curve
- get_param_max(param: int) -> float
- get_param_min(param: int) -> float
- get_particle_flag(particle_flag: int) -> bool
- request_particles_process(process_time: float)
- restart(keep_seed: bool = false)
- set_param_curve(param: int, curve: Curve)
- set_param_max(param: int, value: float)
- set_param_min(param: int, value: float)
- set_particle_flag(particle_flag: int, enable: bool)

**Signals:**
- finished

**Enums:**
**DrawOrder:** DRAW_ORDER_INDEX=0, DRAW_ORDER_LIFETIME=1, DRAW_ORDER_VIEW_DEPTH=2
**Parameter:** PARAM_INITIAL_LINEAR_VELOCITY=0, PARAM_ANGULAR_VELOCITY=1, PARAM_ORBIT_VELOCITY=2, PARAM_LINEAR_ACCEL=3, PARAM_RADIAL_ACCEL=4, PARAM_TANGENTIAL_ACCEL=5, PARAM_DAMPING=6, PARAM_ANGLE=7, PARAM_SCALE=8, PARAM_HUE_VARIATION=9, ...
**ParticleFlags:** PARTICLE_FLAG_ALIGN_Y_TO_VELOCITY=0, PARTICLE_FLAG_ROTATE_Y=1, PARTICLE_FLAG_DISABLE_Z=2, PARTICLE_FLAG_MAX=3
**EmissionShape:** EMISSION_SHAPE_POINT=0, EMISSION_SHAPE_SPHERE=1, EMISSION_SHAPE_SPHERE_SURFACE=2, EMISSION_SHAPE_BOX=3, EMISSION_SHAPE_POINTS=4, EMISSION_SHAPE_DIRECTED_POINTS=5, EMISSION_SHAPE_RING=6, EMISSION_SHAPE_MAX=7


## Callable

A built-in type representing a method or a standalone function.

**Methods:**
- bind() -> Callable
- bindv(arguments: Array) -> Callable
- call() -> Variant
- call_deferred()
- callv(arguments: Array) -> Variant
- create(variant: Variant, method: StringName) -> Callable
- get_argument_count() -> int
- get_bound_arguments() -> Array
- get_bound_arguments_count() -> int
- get_method() -> StringName
- get_object() -> Object
- get_object_id() -> int
- get_unbound_arguments_count() -> int
- hash() -> int
- is_custom() -> bool
- is_null() -> bool
- is_standard() -> bool
- is_valid() -> bool
- rpc()
- rpc_id(peer_id: int)
- unbind(argcount: int) -> Callable


## Camera2D <- Node2D

Camera node for 2D scenes.

**Props:**
- anchor_mode: int (Camera2D.AnchorMode) = 1
- custom_viewport: Node
- drag_bottom_margin: float = 0.2
- drag_horizontal_enabled: bool = false
- drag_horizontal_offset: float = 0.0
- drag_left_margin: float = 0.2
- drag_right_margin: float = 0.2
- drag_top_margin: float = 0.2
- drag_vertical_enabled: bool = false
- drag_vertical_offset: float = 0.0
- editor_draw_drag_margin: bool = false
- editor_draw_limits: bool = false
- editor_draw_screen: bool = true
- enabled: bool = true
- ignore_rotation: bool = true
- limit_bottom: int = 10000000
- limit_enabled: bool = true
- limit_left: int = -10000000
- limit_right: int = 10000000
- limit_smoothed: bool = false
- limit_top: int = -10000000
- offset: Vector2 = Vector2(0, 0)
- position_smoothing_enabled: bool = false
- position_smoothing_speed: float = 5.0
- process_callback: int (Camera2D.Camera2DProcessCallback) = 1
- rotation_smoothing_enabled: bool = false
- rotation_smoothing_speed: float = 5.0
- zoom: Vector2 = Vector2(1, 1)

**Methods:**
- align()
- force_update_scroll()
- get_drag_margin(margin: int) -> float
- get_limit(margin: int) -> int
- get_screen_center_position() -> Vector2
- get_screen_rotation() -> float
- get_target_position() -> Vector2
- is_current() -> bool
- make_current()
- reset_smoothing()
- set_drag_margin(margin: int, drag_margin: float)
- set_limit(margin: int, limit: int)

**Enums:**
**AnchorMode:** ANCHOR_MODE_FIXED_TOP_LEFT=0, ANCHOR_MODE_DRAG_CENTER=1
**Camera2DProcessCallback:** CAMERA2D_PROCESS_PHYSICS=0, CAMERA2D_PROCESS_IDLE=1


## Camera3D <- Node3D

Camera node, displays from a point of view.

**Props:**
- attributes: CameraAttributes
- compositor: Compositor
- cull_mask: int = 1048575
- current: bool = false
- doppler_tracking: int (Camera3D.DopplerTracking) = 0
- environment: Environment
- far: float = 4000.0
- fov: float = 75.0
- frustum_offset: Vector2 = Vector2(0, 0)
- h_offset: float = 0.0
- keep_aspect: int (Camera3D.KeepAspect) = 1
- near: float = 0.05
- projection: int (Camera3D.ProjectionType) = 0
- size: float = 1.0
- v_offset: float = 0.0

**Methods:**
- clear_current(enable_next: bool = true)
- get_camera_projection() -> Projection
- get_camera_rid() -> RID
- get_camera_transform() -> Transform3D
- get_cull_mask_value(layer_number: int) -> bool
- get_frustum() -> Plane[]
- get_pyramid_shape_rid() -> RID
- is_position_behind(world_point: Vector3) -> bool
- is_position_in_frustum(world_point: Vector3) -> bool
- make_current()
- project_local_ray_normal(screen_point: Vector2) -> Vector3
- project_position(screen_point: Vector2, z_depth: float) -> Vector3
- project_ray_normal(screen_point: Vector2) -> Vector3
- project_ray_origin(screen_point: Vector2) -> Vector3
- set_cull_mask_value(layer_number: int, value: bool)
- set_frustum(size: float, offset: Vector2, z_near: float, z_far: float)
- set_orthogonal(size: float, z_near: float, z_far: float)
- set_perspective(fov: float, z_near: float, z_far: float)
- unproject_position(world_point: Vector3) -> Vector2

**Enums:**
**ProjectionType:** PROJECTION_PERSPECTIVE=0, PROJECTION_ORTHOGONAL=1, PROJECTION_FRUSTUM=2
**KeepAspect:** KEEP_WIDTH=0, KEEP_HEIGHT=1
**DopplerTracking:** DOPPLER_TRACKING_DISABLED=0, DOPPLER_TRACKING_IDLE_STEP=1, DOPPLER_TRACKING_PHYSICS_STEP=2


## CanvasItem <- Node

Abstract base class for everything in 2D space.

**Props:**
- clip_children: int (CanvasItem.ClipChildrenMode) = 0
- light_mask: int = 1
- material: Material
- modulate: Color = Color(1, 1, 1, 1)
- self_modulate: Color = Color(1, 1, 1, 1)
- show_behind_parent: bool = false
- texture_filter: int (CanvasItem.TextureFilter) = 0
- texture_repeat: int (CanvasItem.TextureRepeat) = 0
- top_level: bool = false
- use_parent_material: bool = false
- visibility_layer: int = 1
- visible: bool = true
- y_sort_enabled: bool = false
- z_as_relative: bool = true
- z_index: int = 0

**Methods:**
- draw_animation_slice(animation_length: float, slice_begin: float, slice_end: float, offset: float = 0.0)
- draw_arc(center: Vector2, radius: float, start_angle: float, end_angle: float, point_count: int, color: Color, width: float = -1.0, antialiased: bool = false)
- draw_char(font: Font, pos: Vector2, char: String, font_size: int = 16, modulate: Color = Color(1, 1, 1, 1), oversampling: float = 0.0)
- draw_char_outline(font: Font, pos: Vector2, char: String, font_size: int = 16, size: int = -1, modulate: Color = Color(1, 1, 1, 1), oversampling: float = 0.0)
- draw_circle(position: Vector2, radius: float, color: Color, filled: bool = true, width: float = -1.0, antialiased: bool = false)
- draw_colored_polygon(points: PackedVector2Array, color: Color, uvs: PackedVector2Array = PackedVector2Array(), texture: Texture2D = null)
- draw_dashed_line(from: Vector2, to: Vector2, color: Color, width: float = -1.0, dash: float = 2.0, aligned: bool = true, antialiased: bool = false)
- draw_ellipse(position: Vector2, major: float, minor: float, color: Color, filled: bool = true, width: float = -1.0, antialiased: bool = false)
- draw_ellipse_arc(center: Vector2, major: float, minor: float, start_angle: float, end_angle: float, point_count: int, color: Color, width: float = -1.0, antialiased: bool = false)
- draw_end_animation()
- draw_lcd_texture_rect_region(texture: Texture2D, rect: Rect2, src_rect: Rect2, modulate: Color = Color(1, 1, 1, 1))
- draw_line(from: Vector2, to: Vector2, color: Color, width: float = -1.0, antialiased: bool = false)
- draw_mesh(mesh: Mesh, texture: Texture2D, transform: Transform2D = Transform2D(1, 0, 0, 1, 0, 0), modulate: Color = Color(1, 1, 1, 1))
- draw_msdf_texture_rect_region(texture: Texture2D, rect: Rect2, src_rect: Rect2, modulate: Color = Color(1, 1, 1, 1), outline: float = 0.0, pixel_range: float = 4.0, scale: float = 1.0)
- draw_multiline(points: PackedVector2Array, color: Color, width: float = -1.0, antialiased: bool = false)
- draw_multiline_colors(points: PackedVector2Array, colors: PackedColorArray, width: float = -1.0, antialiased: bool = false)
- draw_multiline_string(font: Font, pos: Vector2, text: String, alignment: int = 0, width: float = -1, font_size: int = 16, max_lines: int = -1, modulate: Color = Color(1, 1, 1, 1), brk_flags: int = 3, justification_flags: int = 3, direction: int = 0, orientation: int = 0, oversampling: float = 0.0)
- draw_multiline_string_outline(font: Font, pos: Vector2, text: String, alignment: int = 0, width: float = -1, font_size: int = 16, max_lines: int = -1, size: int = 1, modulate: Color = Color(1, 1, 1, 1), brk_flags: int = 3, justification_flags: int = 3, direction: int = 0, orientation: int = 0, oversampling: float = 0.0)
- draw_multimesh(multimesh: MultiMesh, texture: Texture2D)
- draw_polygon(points: PackedVector2Array, colors: PackedColorArray, uvs: PackedVector2Array = PackedVector2Array(), texture: Texture2D = null)
- draw_polyline(points: PackedVector2Array, color: Color, width: float = -1.0, antialiased: bool = false)
- draw_polyline_colors(points: PackedVector2Array, colors: PackedColorArray, width: float = -1.0, antialiased: bool = false)
- draw_primitive(points: PackedVector2Array, colors: PackedColorArray, uvs: PackedVector2Array, texture: Texture2D = null)
- draw_rect(rect: Rect2, color: Color, filled: bool = true, width: float = -1.0, antialiased: bool = false)
- draw_set_transform(position: Vector2, rotation: float = 0.0, scale: Vector2 = Vector2(1, 1))
- draw_set_transform_matrix(xform: Transform2D)
- draw_string(font: Font, pos: Vector2, text: String, alignment: int = 0, width: float = -1, font_size: int = 16, modulate: Color = Color(1, 1, 1, 1), justification_flags: int = 3, direction: int = 0, orientation: int = 0, oversampling: float = 0.0)
- draw_string_outline(font: Font, pos: Vector2, text: String, alignment: int = 0, width: float = -1, font_size: int = 16, size: int = 1, modulate: Color = Color(1, 1, 1, 1), justification_flags: int = 3, direction: int = 0, orientation: int = 0, oversampling: float = 0.0)
- draw_style_box(style_box: StyleBox, rect: Rect2)
- draw_texture(texture: Texture2D, position: Vector2, modulate: Color = Color(1, 1, 1, 1))
- draw_texture_rect(texture: Texture2D, rect: Rect2, tile: bool, modulate: Color = Color(1, 1, 1, 1), transpose: bool = false)
- draw_texture_rect_region(texture: Texture2D, rect: Rect2, src_rect: Rect2, modulate: Color = Color(1, 1, 1, 1), transpose: bool = false, clip_uv: bool = true)
- force_update_transform()
- get_canvas() -> RID
- get_canvas_item() -> RID
- get_canvas_layer_node() -> CanvasLayer
- get_canvas_transform() -> Transform2D
- get_global_mouse_position() -> Vector2
- get_global_transform() -> Transform2D
- get_global_transform_with_canvas() -> Transform2D
- get_instance_shader_parameter(name: StringName) -> Variant
- get_local_mouse_position() -> Vector2
- get_screen_transform() -> Transform2D
- get_transform() -> Transform2D
- get_viewport_rect() -> Rect2
- get_viewport_transform() -> Transform2D
- get_visibility_layer_bit(layer: int) -> bool
- get_world_2d() -> World2D
- hide()
- is_local_transform_notification_enabled() -> bool
- is_transform_notification_enabled() -> bool
- is_visible_in_tree() -> bool
- make_canvas_position_local(viewport_point: Vector2) -> Vector2
- make_input_local(event: InputEvent) -> InputEvent
- move_to_front()
- queue_redraw()
- set_instance_shader_parameter(name: StringName, value: Variant)
- set_notify_local_transform(enable: bool)
- set_notify_transform(enable: bool)
- set_visibility_layer_bit(layer: int, enabled: bool)
- show()

**Signals:**
- draw
- hidden
- item_rect_changed
- visibility_changed

**Enums:**
**Constants:** NOTIFICATION_TRANSFORM_CHANGED=2000, NOTIFICATION_LOCAL_TRANSFORM_CHANGED=35, NOTIFICATION_DRAW=30, NOTIFICATION_VISIBILITY_CHANGED=31, NOTIFICATION_ENTER_CANVAS=32, NOTIFICATION_EXIT_CANVAS=33, NOTIFICATION_WORLD_2D_CHANGED=36
**TextureFilter:** TEXTURE_FILTER_PARENT_NODE=0, TEXTURE_FILTER_NEAREST=1, TEXTURE_FILTER_LINEAR=2, TEXTURE_FILTER_NEAREST_WITH_MIPMAPS=3, TEXTURE_FILTER_LINEAR_WITH_MIPMAPS=4, TEXTURE_FILTER_NEAREST_WITH_MIPMAPS_ANISOTROPIC=5, TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC=6, TEXTURE_FILTER_MAX=7
**TextureRepeat:** TEXTURE_REPEAT_PARENT_NODE=0, TEXTURE_REPEAT_DISABLED=1, TEXTURE_REPEAT_ENABLED=2, TEXTURE_REPEAT_MIRROR=3, TEXTURE_REPEAT_MAX=4
**ClipChildrenMode:** CLIP_CHILDREN_DISABLED=0, CLIP_CHILDREN_ONLY=1, CLIP_CHILDREN_AND_DRAW=2, CLIP_CHILDREN_MAX=3


## CanvasItemMaterial <- Material

A material for CanvasItems.

**Props:**
- blend_mode: int (CanvasItemMaterial.BlendMode) = 0
- light_mode: int (CanvasItemMaterial.LightMode) = 0
- particles_anim_h_frames: int
- particles_anim_loop: bool
- particles_anim_v_frames: int
- particles_animation: bool = false

**Enums:**
**BlendMode:** BLEND_MODE_MIX=0, BLEND_MODE_ADD=1, BLEND_MODE_SUB=2, BLEND_MODE_MUL=3, BLEND_MODE_PREMULT_ALPHA=4
**LightMode:** LIGHT_MODE_NORMAL=0, LIGHT_MODE_UNSHADED=1, LIGHT_MODE_LIGHT_ONLY=2


## CanvasLayer <- Node

A node used for independent rendering of objects within a 2D scene.

**Props:**
- custom_viewport: Node
- follow_viewport_enabled: bool = false
- follow_viewport_scale: float = 1.0
- layer: int = 1
- offset: Vector2 = Vector2(0, 0)
- rotation: float = 0.0
- scale: Vector2 = Vector2(1, 1)
- transform: Transform2D = Transform2D(1, 0, 0, 1, 0, 0)
- visible: bool = true

**Methods:**
- get_canvas() -> RID
- get_final_transform() -> Transform2D
- hide()
- show()

**Signals:**
- visibility_changed


## CapsuleShape2D <- Shape2D

A 2D capsule shape used for physics collision.

**Props:**
- height: float = 30.0
- mid_height: float
- radius: float = 10.0


## CapsuleShape3D <- Shape3D

A 3D capsule shape used for physics collision.

**Props:**
- height: float = 2.0
- mid_height: float
- radius: float = 0.5


## CenterContainer <- Container

A container that keeps child controls in its center.

**Props:**
- use_top_left: bool = false


## CharacterBody2D <- PhysicsBody2D

A 2D physics body specialized for characters moved by script.

**Props:**
- floor_block_on_wall: bool = true
- floor_constant_speed: bool = false
- floor_max_angle: float = 0.7853982
- floor_snap_length: float = 1.0
- floor_stop_on_slope: bool = true
- max_slides: int = 4
- motion_mode: int (CharacterBody2D.MotionMode) = 0
- platform_floor_layers: int = 4294967295
- platform_on_leave: int (CharacterBody2D.PlatformOnLeave) = 0
- platform_wall_layers: int = 0
- safe_margin: float = 0.08
- slide_on_ceiling: bool = true
- up_direction: Vector2 = Vector2(0, -1)
- velocity: Vector2 = Vector2(0, 0)
- wall_min_slide_angle: float = 0.2617994

**Methods:**
- apply_floor_snap()
- get_floor_angle(up_direction: Vector2 = Vector2(0, -1)) -> float
- get_floor_normal() -> Vector2
- get_last_motion() -> Vector2
- get_last_slide_collision() -> KinematicCollision2D
- get_platform_velocity() -> Vector2
- get_position_delta() -> Vector2
- get_real_velocity() -> Vector2
- get_slide_collision(slide_idx: int) -> KinematicCollision2D
- get_slide_collision_count() -> int
- get_wall_normal() -> Vector2
- is_on_ceiling() -> bool
- is_on_ceiling_only() -> bool
- is_on_floor() -> bool
- is_on_floor_only() -> bool
- is_on_wall() -> bool
- is_on_wall_only() -> bool
- move_and_slide() -> bool

**Enums:**
**MotionMode:** MOTION_MODE_GROUNDED=0, MOTION_MODE_FLOATING=1
**PlatformOnLeave:** PLATFORM_ON_LEAVE_ADD_VELOCITY=0, PLATFORM_ON_LEAVE_ADD_UPWARD_VELOCITY=1, PLATFORM_ON_LEAVE_DO_NOTHING=2


## CharacterBody3D <- PhysicsBody3D

A 3D physics body specialized for characters moved by script.

**Props:**
- floor_block_on_wall: bool = true
- floor_constant_speed: bool = false
- floor_max_angle: float = 0.7853982
- floor_snap_length: float = 0.1
- floor_stop_on_slope: bool = true
- max_slides: int = 6
- motion_mode: int (CharacterBody3D.MotionMode) = 0
- platform_floor_layers: int = 4294967295
- platform_on_leave: int (CharacterBody3D.PlatformOnLeave) = 0
- platform_wall_layers: int = 0
- safe_margin: float = 0.001
- slide_on_ceiling: bool = true
- up_direction: Vector3 = Vector3(0, 1, 0)
- velocity: Vector3 = Vector3(0, 0, 0)
- wall_min_slide_angle: float = 0.2617994

**Methods:**
- apply_floor_snap()
- get_floor_angle(up_direction: Vector3 = Vector3(0, 1, 0)) -> float
- get_floor_normal() -> Vector3
- get_last_motion() -> Vector3
- get_last_slide_collision() -> KinematicCollision3D
- get_platform_angular_velocity() -> Vector3
- get_platform_velocity() -> Vector3
- get_position_delta() -> Vector3
- get_real_velocity() -> Vector3
- get_slide_collision(slide_idx: int) -> KinematicCollision3D
- get_slide_collision_count() -> int
- get_wall_normal() -> Vector3
- is_on_ceiling() -> bool
- is_on_ceiling_only() -> bool
- is_on_floor() -> bool
- is_on_floor_only() -> bool
- is_on_wall() -> bool
- is_on_wall_only() -> bool
- move_and_slide() -> bool

**Enums:**
**MotionMode:** MOTION_MODE_GROUNDED=0, MOTION_MODE_FLOATING=1
**PlatformOnLeave:** PLATFORM_ON_LEAVE_ADD_VELOCITY=0, PLATFORM_ON_LEAVE_ADD_UPWARD_VELOCITY=1, PLATFORM_ON_LEAVE_DO_NOTHING=2


## CheckBox <- Button

A button that represents a binary choice.

**Props:**
- alignment: int (HorizontalAlignment) = 0
- toggle_mode: bool = true


## CheckButton <- Button

A button that represents a binary choice.

**Props:**
- alignment: int (HorizontalAlignment) = 0
- toggle_mode: bool = true


## CircleShape2D <- Shape2D

A 2D circle shape used for physics collision.

**Props:**
- radius: float = 10.0


## CollisionPolygon2D <- Node2D

A node that provides a polygon shape to a CollisionObject2D parent.

**Props:**
- build_mode: int (CollisionPolygon2D.BuildMode) = 0
- disabled: bool = false
- one_way_collision: bool = false
- one_way_collision_margin: float = 1.0
- polygon: PackedVector2Array = PackedVector2Array()

**Enums:**
**BuildMode:** BUILD_SOLIDS=0, BUILD_SEGMENTS=1


## CollisionPolygon3D <- Node3D

A node that provides a thickened polygon shape (a prism) to a CollisionObject3D parent.

**Props:**
- debug_color: Color = Color(0, 0, 0, 0)
- debug_fill: bool = true
- depth: float = 1.0
- disabled: bool = false
- margin: float = 0.04
- polygon: PackedVector2Array = PackedVector2Array()


## CollisionShape2D <- Node2D

A node that provides a Shape2D to a CollisionObject2D parent.

**Props:**
- debug_color: Color = Color(0, 0, 0, 0)
- disabled: bool = false
- one_way_collision: bool = false
- one_way_collision_margin: float = 1.0
- shape: Shape2D


## CollisionShape3D <- Node3D

A node that provides a Shape3D to a CollisionObject3D parent.

**Props:**
- debug_color: Color = Color(0, 0, 0, 0)
- debug_fill: bool = true
- disabled: bool = false
- shape: Shape3D

**Methods:**
- make_convex_from_siblings()
- resource_changed(resource: Resource)


## Color

A color represented in RGBA format.

**Props:**
- a: float = 1.0
- a8: int = 255
- b: float = 0.0
- b8: int = 0
- g: float = 0.0
- g8: int = 0
- h: float = 0.0
- ok_hsl_h: float = 0.0
- ok_hsl_l: float = 0.0
- ok_hsl_s: float = 0.0
- r: float = 0.0
- r8: int = 0
- s: float = 0.0
- v: float = 0.0

**Methods:**
- blend(over: Color) -> Color
- clamp(min: Color = Color(0, 0, 0, 0), max: Color = Color(1, 1, 1, 1)) -> Color
- darkened(amount: float) -> Color
- from_hsv(h: float, s: float, v: float, alpha: float = 1.0) -> Color
- from_ok_hsl(h: float, s: float, l: float, alpha: float = 1.0) -> Color
- from_rgba8(r8: int, g8: int, b8: int, a8: int = 255) -> Color
- from_rgbe9995(rgbe: int) -> Color
- from_string(str: String, default: Color) -> Color
- get_luminance() -> float
- hex(hex: int) -> Color
- hex64(hex: int) -> Color
- html(rgba: String) -> Color
- html_is_valid(color: String) -> bool
- inverted() -> Color
- is_equal_approx(to: Color) -> bool
- lerp(to: Color, weight: float) -> Color
- lightened(amount: float) -> Color
- linear_to_srgb() -> Color
- srgb_to_linear() -> Color
- to_abgr32() -> int
- to_abgr64() -> int
- to_argb32() -> int
- to_argb64() -> int
- to_html(with_alpha: bool = true) -> String
- to_rgba32() -> int
- to_rgba64() -> int

**Enums:**
**Constants:** ALICE_BLUE=Color(0.9411765, 0.972549, 1, 1), ANTIQUE_WHITE=Color(0.98039216, 0.92156863, 0.84313726, 1), AQUA=Color(0, 1, 1, 1), AQUAMARINE=Color(0.49803922, 1, 0.83137256, 1), AZURE=Color(0.9411765, 1, 1, 1), BEIGE=Color(0.9607843, 0.9607843, 0.8627451, 1), BISQUE=Color(1, 0.89411765, 0.76862746, 1), BLACK=Color(0, 0, 0, 1), BLANCHED_ALMOND=Color(1, 0.92156863, 0.8039216, 1), BLUE=Color(0, 0, 1, 1), ...


## ColorRect <- Control

A control that displays a solid color rectangle.

**Props:**
- color: Color = Color(1, 1, 1, 1)


## Container <- Control

Base class for all GUI containers.

**Props:**
- accessibility_region: bool = false
- mouse_filter: int (Control.MouseFilter) = 1

**Methods:**
- fit_child_in_rect(child: Control, rect: Rect2)
- queue_sort()

**Signals:**
- pre_sort_children
- sort_children

**Enums:**
**Constants:** NOTIFICATION_PRE_SORT_CHILDREN=50, NOTIFICATION_SORT_CHILDREN=51


## Control <- CanvasItem

Base class for all GUI controls. Adapts its position and size based on its parent control.

**Props:**
- accessibility_controls_nodes: NodePath[] = []
- accessibility_described_by_nodes: NodePath[] = []
- accessibility_description: String = ""
- accessibility_flow_to_nodes: NodePath[] = []
- accessibility_labeled_by_nodes: NodePath[] = []
- accessibility_live: int (DisplayServer.AccessibilityLiveMode) = 0
- accessibility_name: String = ""
- anchor_bottom: float = 0.0
- anchor_left: float = 0.0
- anchor_right: float = 0.0
- anchor_top: float = 0.0
- auto_translate: bool
- clip_contents: bool = false
- custom_minimum_size: Vector2 = Vector2(0, 0)
- focus_behavior_recursive: int (Control.FocusBehaviorRecursive) = 0
- focus_mode: int (Control.FocusMode) = 0
- focus_neighbor_bottom: NodePath = NodePath("")
- focus_neighbor_left: NodePath = NodePath("")
- focus_neighbor_right: NodePath = NodePath("")
- focus_neighbor_top: NodePath = NodePath("")
- focus_next: NodePath = NodePath("")
- focus_previous: NodePath = NodePath("")
- global_position: Vector2
- grow_horizontal: int (Control.GrowDirection) = 1
- grow_vertical: int (Control.GrowDirection) = 1
- layout_direction: int (Control.LayoutDirection) = 0
- localize_numeral_system: bool = true
- mouse_behavior_recursive: int (Control.MouseBehaviorRecursive) = 0
- mouse_default_cursor_shape: int (Control.CursorShape) = 0
- mouse_filter: int (Control.MouseFilter) = 0
- mouse_force_pass_scroll_events: bool = true
- offset_bottom: float = 0.0
- offset_left: float = 0.0
- offset_right: float = 0.0
- offset_top: float = 0.0
- physics_interpolation_mode: int (Node.PhysicsInterpolationMode) = 2
- pivot_offset: Vector2 = Vector2(0, 0)
- pivot_offset_ratio: Vector2 = Vector2(0, 0)
- position: Vector2 = Vector2(0, 0)
- rotation: float = 0.0
- rotation_degrees: float
- scale: Vector2 = Vector2(1, 1)
- shortcut_context: Node
- size: Vector2 = Vector2(0, 0)
- size_flags_horizontal: int (Control.SizeFlags) = 1
- size_flags_stretch_ratio: float = 1.0
- size_flags_vertical: int (Control.SizeFlags) = 1
- theme: Theme
- theme_type_variation: StringName = &""
- tooltip_auto_translate_mode: int (Node.AutoTranslateMode) = 0
- tooltip_text: String = ""

**Methods:**
- accept_event()
- accessibility_drag()
- accessibility_drop()
- add_theme_color_override(name: StringName, color: Color)
- add_theme_constant_override(name: StringName, constant: int)
- add_theme_font_override(name: StringName, font: Font)
- add_theme_font_size_override(name: StringName, font_size: int)
- add_theme_icon_override(name: StringName, texture: Texture2D)
- add_theme_stylebox_override(name: StringName, stylebox: StyleBox)
- begin_bulk_theme_override()
- end_bulk_theme_override()
- find_next_valid_focus() -> Control
- find_prev_valid_focus() -> Control
- find_valid_focus_neighbor(side: int) -> Control
- force_drag(data: Variant, preview: Control)
- get_anchor(side: int) -> float
- get_begin() -> Vector2
- get_combined_minimum_size() -> Vector2
- get_combined_pivot_offset() -> Vector2
- get_cursor_shape(position: Vector2 = Vector2(0, 0)) -> int
- get_end() -> Vector2
- get_focus_mode_with_override() -> int
- get_focus_neighbor(side: int) -> NodePath
- get_global_rect() -> Rect2
- get_minimum_size() -> Vector2
- get_mouse_filter_with_override() -> int
- get_offset(offset: int) -> float
- get_parent_area_size() -> Vector2
- get_parent_control() -> Control
- get_rect() -> Rect2
- get_screen_position() -> Vector2
- get_theme_color(name: StringName, theme_type: StringName = &"") -> Color
- get_theme_constant(name: StringName, theme_type: StringName = &"") -> int
- get_theme_default_base_scale() -> float
- get_theme_default_font() -> Font
- get_theme_default_font_size() -> int
- get_theme_font(name: StringName, theme_type: StringName = &"") -> Font
- get_theme_font_size(name: StringName, theme_type: StringName = &"") -> int
- get_theme_icon(name: StringName, theme_type: StringName = &"") -> Texture2D
- get_theme_stylebox(name: StringName, theme_type: StringName = &"") -> StyleBox
- get_tooltip(at_position: Vector2 = Vector2(0, 0)) -> String
- grab_click_focus()
- grab_focus(hide_focus: bool = false)
- has_focus(ignore_hidden_focus: bool = false) -> bool
- has_theme_color(name: StringName, theme_type: StringName = &"") -> bool
- has_theme_color_override(name: StringName) -> bool
- has_theme_constant(name: StringName, theme_type: StringName = &"") -> bool
- has_theme_constant_override(name: StringName) -> bool
- has_theme_font(name: StringName, theme_type: StringName = &"") -> bool
- has_theme_font_override(name: StringName) -> bool
- has_theme_font_size(name: StringName, theme_type: StringName = &"") -> bool
- has_theme_font_size_override(name: StringName) -> bool
- has_theme_icon(name: StringName, theme_type: StringName = &"") -> bool
- has_theme_icon_override(name: StringName) -> bool
- has_theme_stylebox(name: StringName, theme_type: StringName = &"") -> bool
- has_theme_stylebox_override(name: StringName) -> bool
- is_drag_successful() -> bool
- is_layout_rtl() -> bool
- release_focus()
- remove_theme_color_override(name: StringName)
- remove_theme_constant_override(name: StringName)
- remove_theme_font_override(name: StringName)
- remove_theme_font_size_override(name: StringName)
- remove_theme_icon_override(name: StringName)
- remove_theme_stylebox_override(name: StringName)
- reset_size()
- set_anchor(side: int, anchor: float, keep_offset: bool = false, push_opposite_anchor: bool = true)
- set_anchor_and_offset(side: int, anchor: float, offset: float, push_opposite_anchor: bool = false)
- set_anchors_and_offsets_preset(preset: int, resize_mode: int = 0, margin: int = 0)
- set_anchors_preset(preset: int, keep_offsets: bool = false)
- set_begin(position: Vector2)
- set_drag_forwarding(drag_func: Callable, can_drop_func: Callable, drop_func: Callable)
- set_drag_preview(control: Control)
- set_end(position: Vector2)
- set_focus_neighbor(side: int, neighbor: NodePath)
- set_global_position(position: Vector2, keep_offsets: bool = false)
- set_offset(side: int, offset: float)
- set_offsets_preset(preset: int, resize_mode: int = 0, margin: int = 0)
- set_position(position: Vector2, keep_offsets: bool = false)
- set_size(size: Vector2, keep_offsets: bool = false)
- update_minimum_size()
- warp_mouse(position: Vector2)

**Signals:**
- focus_entered
- focus_exited
- gui_input(event: InputEvent)
- minimum_size_changed
- mouse_entered
- mouse_exited
- resized
- size_flags_changed
- theme_changed

**Enums:**
**FocusMode:** FOCUS_NONE=0, FOCUS_CLICK=1, FOCUS_ALL=2, FOCUS_ACCESSIBILITY=3
**FocusBehaviorRecursive:** FOCUS_BEHAVIOR_INHERITED=0, FOCUS_BEHAVIOR_DISABLED=1, FOCUS_BEHAVIOR_ENABLED=2
**MouseBehaviorRecursive:** MOUSE_BEHAVIOR_INHERITED=0, MOUSE_BEHAVIOR_DISABLED=1, MOUSE_BEHAVIOR_ENABLED=2
**Constants:** NOTIFICATION_RESIZED=40, NOTIFICATION_MOUSE_ENTER=41, NOTIFICATION_MOUSE_EXIT=42, NOTIFICATION_MOUSE_ENTER_SELF=60, NOTIFICATION_MOUSE_EXIT_SELF=61, NOTIFICATION_FOCUS_ENTER=43, NOTIFICATION_FOCUS_EXIT=44, NOTIFICATION_THEME_CHANGED=45, NOTIFICATION_SCROLL_BEGIN=47, NOTIFICATION_SCROLL_END=48, ...
**CursorShape:** CURSOR_ARROW=0, CURSOR_IBEAM=1, CURSOR_POINTING_HAND=2, CURSOR_CROSS=3, CURSOR_WAIT=4, CURSOR_BUSY=5, CURSOR_DRAG=6, CURSOR_CAN_DROP=7, CURSOR_FORBIDDEN=8, CURSOR_VSIZE=9, ...
**LayoutPreset:** PRESET_TOP_LEFT=0, PRESET_TOP_RIGHT=1, PRESET_BOTTOM_LEFT=2, PRESET_BOTTOM_RIGHT=3, PRESET_CENTER_LEFT=4, PRESET_CENTER_TOP=5, PRESET_CENTER_RIGHT=6, PRESET_CENTER_BOTTOM=7, PRESET_CENTER=8, PRESET_LEFT_WIDE=9, ...
**LayoutPresetMode:** PRESET_MODE_MINSIZE=0, PRESET_MODE_KEEP_WIDTH=1, PRESET_MODE_KEEP_HEIGHT=2, PRESET_MODE_KEEP_SIZE=3
**SizeFlags:** SIZE_SHRINK_BEGIN=0, SIZE_FILL=1, SIZE_EXPAND=2, SIZE_EXPAND_FILL=3, SIZE_SHRINK_CENTER=4, SIZE_SHRINK_END=8
**MouseFilter:** MOUSE_FILTER_STOP=0, MOUSE_FILTER_PASS=1, MOUSE_FILTER_IGNORE=2
**GrowDirection:** GROW_DIRECTION_BEGIN=0, GROW_DIRECTION_END=1, GROW_DIRECTION_BOTH=2
**Anchor:** ANCHOR_BEGIN=0, ANCHOR_END=1
**LayoutDirection:** LAYOUT_DIRECTION_INHERITED=0, LAYOUT_DIRECTION_APPLICATION_LOCALE=1, LAYOUT_DIRECTION_LTR=2, LAYOUT_DIRECTION_RTL=3, LAYOUT_DIRECTION_SYSTEM_LOCALE=4, LAYOUT_DIRECTION_MAX=5, LAYOUT_DIRECTION_LOCALE=1
**TextDirection:** TEXT_DIRECTION_INHERITED=3, TEXT_DIRECTION_AUTO=0, TEXT_DIRECTION_LTR=1, TEXT_DIRECTION_RTL=2


## ConvexPolygonShape2D <- Shape2D

A 2D convex polygon shape used for physics collision.

**Props:**
- points: PackedVector2Array = PackedVector2Array()

**Methods:**
- set_point_cloud(point_cloud: PackedVector2Array)


## ConvexPolygonShape3D <- Shape3D

A 3D convex polyhedron shape used for physics collision.

**Props:**
- points: PackedVector3Array = PackedVector3Array()


## Curve <- Resource

A mathematical curve.

**Props:**
- bake_resolution: int = 100
- max_domain: float = 1.0
- max_value: float = 1.0
- min_domain: float = 0.0
- min_value: float = 0.0
- point_count: int = 0

**Methods:**
- add_point(position: Vector2, left_tangent: float = 0, right_tangent: float = 0, left_mode: int = 0, right_mode: int = 0) -> int
- bake()
- clean_dupes()
- clear_points()
- get_domain_range() -> float
- get_point_left_mode(index: int) -> int
- get_point_left_tangent(index: int) -> float
- get_point_position(index: int) -> Vector2
- get_point_right_mode(index: int) -> int
- get_point_right_tangent(index: int) -> float
- get_value_range() -> float
- remove_point(index: int)
- sample(offset: float) -> float
- sample_baked(offset: float) -> float
- set_point_left_mode(index: int, mode: int)
- set_point_left_tangent(index: int, tangent: float)
- set_point_offset(index: int, offset: float) -> int
- set_point_right_mode(index: int, mode: int)
- set_point_right_tangent(index: int, tangent: float)
- set_point_value(index: int, y: float)

**Signals:**
- domain_changed
- range_changed

**Enums:**
**TangentMode:** TANGENT_FREE=0, TANGENT_LINEAR=1, TANGENT_MODE_COUNT=2


## Curve2D <- Resource

Describes a Bézier curve in 2D space.

**Props:**
- bake_interval: float = 5.0
- point_count: int = 0

**Methods:**
- add_point(position: Vector2, in: Vector2 = Vector2(0, 0), out: Vector2 = Vector2(0, 0), index: int = -1)
- clear_points()
- get_baked_length() -> float
- get_baked_points() -> PackedVector2Array
- get_closest_offset(to_point: Vector2) -> float
- get_closest_point(to_point: Vector2) -> Vector2
- get_point_in(idx: int) -> Vector2
- get_point_out(idx: int) -> Vector2
- get_point_position(idx: int) -> Vector2
- remove_point(idx: int)
- sample(idx: int, t: float) -> Vector2
- sample_baked(offset: float = 0.0, cubic: bool = false) -> Vector2
- sample_baked_with_rotation(offset: float = 0.0, cubic: bool = false) -> Transform2D
- samplef(fofs: float) -> Vector2
- set_point_in(idx: int, position: Vector2)
- set_point_out(idx: int, position: Vector2)
- set_point_position(idx: int, position: Vector2)
- tessellate(max_stages: int = 5, tolerance_degrees: float = 4) -> PackedVector2Array
- tessellate_even_length(max_stages: int = 5, tolerance_length: float = 20.0) -> PackedVector2Array


## Curve3D <- Resource

Describes a Bézier curve in 3D space.

**Props:**
- bake_interval: float = 0.2
- closed: bool = false
- point_count: int = 0
- up_vector_enabled: bool = true

**Methods:**
- add_point(position: Vector3, in: Vector3 = Vector3(0, 0, 0), out: Vector3 = Vector3(0, 0, 0), index: int = -1)
- clear_points()
- get_baked_length() -> float
- get_baked_points() -> PackedVector3Array
- get_baked_tilts() -> PackedFloat32Array
- get_baked_up_vectors() -> PackedVector3Array
- get_closest_offset(to_point: Vector3) -> float
- get_closest_point(to_point: Vector3) -> Vector3
- get_point_in(idx: int) -> Vector3
- get_point_out(idx: int) -> Vector3
- get_point_position(idx: int) -> Vector3
- get_point_tilt(idx: int) -> float
- remove_point(idx: int)
- sample(idx: int, t: float) -> Vector3
- sample_baked(offset: float = 0.0, cubic: bool = false) -> Vector3
- sample_baked_up_vector(offset: float, apply_tilt: bool = false) -> Vector3
- sample_baked_with_rotation(offset: float = 0.0, cubic: bool = false, apply_tilt: bool = false) -> Transform3D
- samplef(fofs: float) -> Vector3
- set_point_in(idx: int, position: Vector3)
- set_point_out(idx: int, position: Vector3)
- set_point_position(idx: int, position: Vector3)
- set_point_tilt(idx: int, tilt: float)
- tessellate(max_stages: int = 5, tolerance_degrees: float = 4) -> PackedVector3Array
- tessellate_even_length(max_stages: int = 5, tolerance_length: float = 0.2) -> PackedVector3Array


## CylinderMesh <- PrimitiveMesh

Class representing a cylindrical PrimitiveMesh.

**Props:**
- bottom_radius: float = 0.5
- cap_bottom: bool = true
- cap_top: bool = true
- height: float = 2.0
- radial_segments: int = 64
- rings: int = 4
- top_radius: float = 0.5


## DirectionalLight2D <- Light2D

Directional 2D light from a distance.

**Props:**
- height: float = 0.0
- max_distance: float = 10000.0


## DirectionalLight3D <- Light3D

Directional light from a distance, as from the Sun.

**Props:**
- directional_shadow_blend_splits: bool = false
- directional_shadow_fade_start: float = 0.8
- directional_shadow_max_distance: float = 100.0
- directional_shadow_mode: int (DirectionalLight3D.ShadowMode) = 2
- directional_shadow_pancake_size: float = 20.0
- directional_shadow_split_1: float = 0.1
- directional_shadow_split_2: float = 0.2
- directional_shadow_split_3: float = 0.5
- sky_mode: int (DirectionalLight3D.SkyMode) = 0

**Enums:**
**ShadowMode:** SHADOW_ORTHOGONAL=0, SHADOW_PARALLEL_2_SPLITS=1, SHADOW_PARALLEL_4_SPLITS=2
**SkyMode:** SKY_MODE_LIGHT_AND_SKY=0, SKY_MODE_LIGHT_ONLY=1, SKY_MODE_SKY_ONLY=2


## Engine <- Object

Provides access to engine properties.

**Props:**
- max_fps: int = 0
- max_physics_steps_per_frame: int = 8
- physics_jitter_fix: float = 0.5
- physics_ticks_per_second: int = 60
- print_error_messages: bool = true
- print_to_stdout: bool = true
- time_scale: float = 1.0

**Methods:**
- capture_script_backtraces(include_variables: bool = false) -> ScriptBacktrace[]
- get_architecture_name() -> String
- get_author_info() -> Dictionary
- get_copyright_info() -> Dictionary[]
- get_donor_info() -> Dictionary
- get_frames_drawn() -> int
- get_frames_per_second() -> float
- get_license_info() -> Dictionary
- get_license_text() -> String
- get_main_loop() -> MainLoop
- get_physics_frames() -> int
- get_physics_interpolation_fraction() -> float
- get_process_frames() -> int
- get_script_language(index: int) -> ScriptLanguage
- get_script_language_count() -> int
- get_singleton(name: StringName) -> Object
- get_singleton_list() -> PackedStringArray
- get_version_info() -> Dictionary
- get_write_movie_path() -> String
- has_singleton(name: StringName) -> bool
- is_editor_hint() -> bool
- is_embedded_in_editor() -> bool
- is_in_physics_frame() -> bool
- register_script_language(language: ScriptLanguage) -> int
- register_singleton(name: StringName, instance: Object)
- unregister_script_language(language: ScriptLanguage) -> int
- unregister_singleton(name: StringName)


## Font <- Resource

Abstract base class for fonts and font variations.

**Props:**
- fallbacks: Font[] = []

**Methods:**
- draw_char(canvas_item: RID, pos: Vector2, char: int, font_size: int, modulate: Color = Color(1, 1, 1, 1), oversampling: float = 0.0) -> float
- draw_char_outline(canvas_item: RID, pos: Vector2, char: int, font_size: int, size: int = -1, modulate: Color = Color(1, 1, 1, 1), oversampling: float = 0.0) -> float
- draw_multiline_string(canvas_item: RID, pos: Vector2, text: String, alignment: int = 0, width: float = -1, font_size: int = 16, max_lines: int = -1, modulate: Color = Color(1, 1, 1, 1), brk_flags: int = 3, justification_flags: int = 3, direction: int = 0, orientation: int = 0, oversampling: float = 0.0)
- draw_multiline_string_outline(canvas_item: RID, pos: Vector2, text: String, alignment: int = 0, width: float = -1, font_size: int = 16, max_lines: int = -1, size: int = 1, modulate: Color = Color(1, 1, 1, 1), brk_flags: int = 3, justification_flags: int = 3, direction: int = 0, orientation: int = 0, oversampling: float = 0.0)
- draw_string(canvas_item: RID, pos: Vector2, text: String, alignment: int = 0, width: float = -1, font_size: int = 16, modulate: Color = Color(1, 1, 1, 1), justification_flags: int = 3, direction: int = 0, orientation: int = 0, oversampling: float = 0.0)
- draw_string_outline(canvas_item: RID, pos: Vector2, text: String, alignment: int = 0, width: float = -1, font_size: int = 16, size: int = 1, modulate: Color = Color(1, 1, 1, 1), justification_flags: int = 3, direction: int = 0, orientation: int = 0, oversampling: float = 0.0)
- find_variation(variation_coordinates: Dictionary, face_index: int = 0, strength: float = 0.0, transform: Transform2D = Transform2D(1, 0, 0, 1, 0, 0), spacing_top: int = 0, spacing_bottom: int = 0, spacing_space: int = 0, spacing_glyph: int = 0, baseline_offset: float = 0.0) -> RID
- get_ascent(font_size: int = 16) -> float
- get_char_size(char: int, font_size: int) -> Vector2
- get_descent(font_size: int = 16) -> float
- get_face_count() -> int
- get_font_name() -> String
- get_font_stretch() -> int
- get_font_style() -> int
- get_font_style_name() -> String
- get_font_weight() -> int
- get_height(font_size: int = 16) -> float
- get_multiline_string_size(text: String, alignment: int = 0, width: float = -1, font_size: int = 16, max_lines: int = -1, brk_flags: int = 3, justification_flags: int = 3, direction: int = 0, orientation: int = 0) -> Vector2
- get_opentype_features() -> Dictionary
- get_ot_name_strings() -> Dictionary
- get_rids() -> RID[]
- get_spacing(spacing: int) -> int
- get_string_size(text: String, alignment: int = 0, width: float = -1, font_size: int = 16, justification_flags: int = 3, direction: int = 0, orientation: int = 0) -> Vector2
- get_supported_chars() -> String
- get_supported_feature_list() -> Dictionary
- get_supported_variation_list() -> Dictionary
- get_underline_position(font_size: int = 16) -> float
- get_underline_thickness(font_size: int = 16) -> float
- has_char(char: int) -> bool
- is_language_supported(language: String) -> bool
- is_script_supported(script: String) -> bool
- set_cache_capacity(single_line: int, multi_line: int)


## FontFile <- Font

Holds font source data and prerendered glyph cache, imported from a dynamic or a bitmap font.

**Props:**
- allow_system_fallback: bool = true
- antialiasing: int (TextServer.FontAntialiasing) = 1
- data: PackedByteArray = PackedByteArray()
- disable_embedded_bitmaps: bool = true
- fixed_size: int = 0
- fixed_size_scale_mode: int (TextServer.FixedSizeScaleMode) = 0
- font_name: String = ""
- font_stretch: int = 100
- font_style: int (TextServer.FontStyle) = 0
- font_weight: int = 400
- force_autohinter: bool = false
- generate_mipmaps: bool = false
- hinting: int (TextServer.Hinting) = 1
- keep_rounding_remainders: bool = true
- modulate_color_glyphs: bool = false
- msdf_pixel_range: int = 16
- msdf_size: int = 48
- multichannel_signed_distance_field: bool = false
- opentype_feature_overrides: Dictionary = {}
- oversampling: float = 0.0
- style_name: String = ""
- subpixel_positioning: int (TextServer.SubpixelPositioning) = 1

**Methods:**
- clear_cache()
- clear_glyphs(cache_index: int, size: Vector2i)
- clear_kerning_map(cache_index: int, size: int)
- clear_size_cache(cache_index: int)
- clear_textures(cache_index: int, size: Vector2i)
- get_cache_ascent(cache_index: int, size: int) -> float
- get_cache_count() -> int
- get_cache_descent(cache_index: int, size: int) -> float
- get_cache_scale(cache_index: int, size: int) -> float
- get_cache_underline_position(cache_index: int, size: int) -> float
- get_cache_underline_thickness(cache_index: int, size: int) -> float
- get_char_from_glyph_index(size: int, glyph_index: int) -> int
- get_embolden(cache_index: int) -> float
- get_extra_baseline_offset(cache_index: int) -> float
- get_extra_spacing(cache_index: int, spacing: int) -> int
- get_face_index(cache_index: int) -> int
- get_glyph_advance(cache_index: int, size: int, glyph: int) -> Vector2
- get_glyph_index(size: int, char: int, variation_selector: int) -> int
- get_glyph_list(cache_index: int, size: Vector2i) -> PackedInt32Array
- get_glyph_offset(cache_index: int, size: Vector2i, glyph: int) -> Vector2
- get_glyph_size(cache_index: int, size: Vector2i, glyph: int) -> Vector2
- get_glyph_texture_idx(cache_index: int, size: Vector2i, glyph: int) -> int
- get_glyph_uv_rect(cache_index: int, size: Vector2i, glyph: int) -> Rect2
- get_kerning(cache_index: int, size: int, glyph_pair: Vector2i) -> Vector2
- get_kerning_list(cache_index: int, size: int) -> Vector2i[]
- get_language_support_override(language: String) -> bool
- get_language_support_overrides() -> PackedStringArray
- get_script_support_override(script: String) -> bool
- get_script_support_overrides() -> PackedStringArray
- get_size_cache_list(cache_index: int) -> Vector2i[]
- get_texture_count(cache_index: int, size: Vector2i) -> int
- get_texture_image(cache_index: int, size: Vector2i, texture_index: int) -> Image
- get_texture_offsets(cache_index: int, size: Vector2i, texture_index: int) -> PackedInt32Array
- get_transform(cache_index: int) -> Transform2D
- get_variation_coordinates(cache_index: int) -> Dictionary
- load_bitmap_font(path: String) -> int
- load_dynamic_font(path: String) -> int
- remove_cache(cache_index: int)
- remove_glyph(cache_index: int, size: Vector2i, glyph: int)
- remove_kerning(cache_index: int, size: int, glyph_pair: Vector2i)
- remove_language_support_override(language: String)
- remove_script_support_override(script: String)
- remove_size_cache(cache_index: int, size: Vector2i)
- remove_texture(cache_index: int, size: Vector2i, texture_index: int)
- render_glyph(cache_index: int, size: Vector2i, index: int)
- render_range(cache_index: int, size: Vector2i, start: int, end: int)
- set_cache_ascent(cache_index: int, size: int, ascent: float)
- set_cache_descent(cache_index: int, size: int, descent: float)
- set_cache_scale(cache_index: int, size: int, scale: float)
- set_cache_underline_position(cache_index: int, size: int, underline_position: float)
- set_cache_underline_thickness(cache_index: int, size: int, underline_thickness: float)
- set_embolden(cache_index: int, strength: float)
- set_extra_baseline_offset(cache_index: int, baseline_offset: float)
- set_extra_spacing(cache_index: int, spacing: int, value: int)
- set_face_index(cache_index: int, face_index: int)
- set_glyph_advance(cache_index: int, size: int, glyph: int, advance: Vector2)
- set_glyph_offset(cache_index: int, size: Vector2i, glyph: int, offset: Vector2)
- set_glyph_size(cache_index: int, size: Vector2i, glyph: int, gl_size: Vector2)
- set_glyph_texture_idx(cache_index: int, size: Vector2i, glyph: int, texture_idx: int)
- set_glyph_uv_rect(cache_index: int, size: Vector2i, glyph: int, uv_rect: Rect2)
- set_kerning(cache_index: int, size: int, glyph_pair: Vector2i, kerning: Vector2)
- set_language_support_override(language: String, supported: bool)
- set_script_support_override(script: String, supported: bool)
- set_texture_image(cache_index: int, size: Vector2i, texture_index: int, image: Image)
- set_texture_offsets(cache_index: int, size: Vector2i, texture_index: int, offset: PackedInt32Array)
- set_transform(cache_index: int, transform: Transform2D)
- set_variation_coordinates(cache_index: int, variation_coordinates: Dictionary)


## GPUParticles2D <- Node2D

A 2D particle emitter.

**Props:**
- amount: int = 8
- amount_ratio: float = 1.0
- collision_base_size: float = 1.0
- draw_order: int (GPUParticles2D.DrawOrder) = 1
- emitting: bool = true
- explosiveness: float = 0.0
- fixed_fps: int = 30
- fract_delta: bool = true
- interp_to_end: float = 0.0
- interpolate: bool = true
- lifetime: float = 1.0
- local_coords: bool = false
- one_shot: bool = false
- preprocess: float = 0.0
- process_material: Material
- randomness: float = 0.0
- seed: int = 0
- speed_scale: float = 1.0
- sub_emitter: NodePath = NodePath("")
- texture: Texture2D
- trail_enabled: bool = false
- trail_lifetime: float = 0.3
- trail_section_subdivisions: int = 4
- trail_sections: int = 8
- use_fixed_seed: bool = false
- visibility_rect: Rect2 = Rect2(-100, -100, 200, 200)

**Methods:**
- capture_rect() -> Rect2
- convert_from_particles(particles: Node)
- emit_particle(xform: Transform2D, velocity: Vector2, color: Color, custom: Color, flags: int)
- request_particles_process(process_time: float)
- restart(keep_seed: bool = false)

**Signals:**
- finished

**Enums:**
**DrawOrder:** DRAW_ORDER_INDEX=0, DRAW_ORDER_LIFETIME=1, DRAW_ORDER_REVERSE_LIFETIME=2
**EmitFlags:** EMIT_FLAG_POSITION=1, EMIT_FLAG_ROTATION_SCALE=2, EMIT_FLAG_VELOCITY=4, EMIT_FLAG_COLOR=8, EMIT_FLAG_CUSTOM=16


## GPUParticles3D <- GeometryInstance3D

A 3D particle emitter.

**Props:**
- amount: int = 8
- amount_ratio: float = 1.0
- collision_base_size: float = 0.01
- draw_order: int (GPUParticles3D.DrawOrder) = 0
- draw_pass_1: Mesh
- draw_pass_2: Mesh
- draw_pass_3: Mesh
- draw_pass_4: Mesh
- draw_passes: int = 1
- draw_skin: Skin
- emitting: bool = true
- explosiveness: float = 0.0
- fixed_fps: int = 30
- fract_delta: bool = true
- interp_to_end: float = 0.0
- interpolate: bool = true
- lifetime: float = 1.0
- local_coords: bool = false
- one_shot: bool = false
- preprocess: float = 0.0
- process_material: Material
- randomness: float = 0.0
- seed: int = 0
- speed_scale: float = 1.0
- sub_emitter: NodePath = NodePath("")
- trail_enabled: bool = false
- trail_lifetime: float = 0.3
- transform_align: int (GPUParticles3D.TransformAlign) = 0
- use_fixed_seed: bool = false
- visibility_aabb: AABB = AABB(-4, -4, -4, 8, 8, 8)

**Methods:**
- capture_aabb() -> AABB
- convert_from_particles(particles: Node)
- emit_particle(xform: Transform3D, velocity: Vector3, color: Color, custom: Color, flags: int)
- get_draw_pass_mesh(pass: int) -> Mesh
- request_particles_process(process_time: float)
- restart(keep_seed: bool = false)
- set_draw_pass_mesh(pass: int, mesh: Mesh)

**Signals:**
- finished

**Enums:**
**DrawOrder:** DRAW_ORDER_INDEX=0, DRAW_ORDER_LIFETIME=1, DRAW_ORDER_REVERSE_LIFETIME=2, DRAW_ORDER_VIEW_DEPTH=3
**EmitFlags:** EMIT_FLAG_POSITION=1, EMIT_FLAG_ROTATION_SCALE=2, EMIT_FLAG_VELOCITY=4, EMIT_FLAG_COLOR=8, EMIT_FLAG_CUSTOM=16
**Constants:** MAX_DRAW_PASSES=4
**TransformAlign:** TRANSFORM_ALIGN_DISABLED=0, TRANSFORM_ALIGN_Z_BILLBOARD=1, TRANSFORM_ALIGN_Y_TO_VELOCITY=2, TRANSFORM_ALIGN_Z_BILLBOARD_Y_TO_VELOCITY=3


## Gradient <- Resource

A color transition.

**Props:**
- colors: PackedColorArray = PackedColorArray(0, 0, 0, 1, 1, 1, 1, 1)
- interpolation_color_space: int (Gradient.ColorSpace) = 0
- interpolation_mode: int (Gradient.InterpolationMode) = 0
- offsets: PackedFloat32Array = PackedFloat32Array(0, 1)

**Methods:**
- add_point(offset: float, color: Color)
- get_color(point: int) -> Color
- get_offset(point: int) -> float
- get_point_count() -> int
- remove_point(point: int)
- reverse()
- sample(offset: float) -> Color
- set_color(point: int, color: Color)
- set_offset(point: int, offset: float)

**Enums:**
**InterpolationMode:** GRADIENT_INTERPOLATE_LINEAR=0, GRADIENT_INTERPOLATE_CONSTANT=1, GRADIENT_INTERPOLATE_CUBIC=2
**ColorSpace:** GRADIENT_COLOR_SPACE_SRGB=0, GRADIENT_COLOR_SPACE_LINEAR_SRGB=1, GRADIENT_COLOR_SPACE_OKLAB=2


## GridContainer <- Container

A container that arranges its child controls in a grid layout.

**Props:**
- columns: int = 1


## HBoxContainer <- BoxContainer

A container that arranges its child controls horizontally.


## HSlider <- Slider

A horizontal slider that goes from left (min) to right (max).


## ImageTexture <- Texture2D

A Texture2D based on an Image.

**Props:**
- resource_local_to_scene: bool = false

**Methods:**
- create_from_image(image: Image) -> ImageTexture
- get_format() -> int
- set_image(image: Image)
- set_size_override(size: Vector2i)
- update(image: Image)


## Input <- Object

A singleton for handling inputs.

**Props:**
- emulate_mouse_from_touch: bool
- emulate_touch_from_mouse: bool
- mouse_mode: int (Input.MouseMode)
- use_accumulated_input: bool

**Methods:**
- action_press(action: StringName, strength: float = 1.0)
- action_release(action: StringName)
- add_joy_mapping(mapping: String, update_existing: bool = false)
- clear_joy_motion_sensors_calibration(device: int)
- flush_buffered_events()
- get_accelerometer() -> Vector3
- get_action_raw_strength(action: StringName, exact_match: bool = false) -> float
- get_action_strength(action: StringName, exact_match: bool = false) -> float
- get_axis(negative_action: StringName, positive_action: StringName) -> float
- get_connected_joypads() -> int[]
- get_current_cursor_shape() -> int
- get_gravity() -> Vector3
- get_gyroscope() -> Vector3
- get_joy_accelerometer(device: int) -> Vector3
- get_joy_axis(device: int, axis: int) -> float
- get_joy_gravity(device: int) -> Vector3
- get_joy_guid(device: int) -> String
- get_joy_gyroscope(device: int) -> Vector3
- get_joy_info(device: int) -> Dictionary
- get_joy_motion_sensors_calibration(device: int) -> Dictionary
- get_joy_motion_sensors_rate(device: int) -> float
- get_joy_name(device: int) -> String
- get_joy_vibration_duration(device: int) -> float
- get_joy_vibration_strength(device: int) -> Vector2
- get_last_mouse_screen_velocity() -> Vector2
- get_last_mouse_velocity() -> Vector2
- get_magnetometer() -> Vector3
- get_mouse_button_mask() -> int
- get_vector(negative_x: StringName, positive_x: StringName, negative_y: StringName, positive_y: StringName, deadzone: float = -1.0) -> Vector2
- has_joy_light(device: int) -> bool
- has_joy_motion_sensors(device: int) -> bool
- is_action_just_pressed(action: StringName, exact_match: bool = false) -> bool
- is_action_just_pressed_by_event(action: StringName, event: InputEvent, exact_match: bool = false) -> bool
- is_action_just_released(action: StringName, exact_match: bool = false) -> bool
- is_action_just_released_by_event(action: StringName, event: InputEvent, exact_match: bool = false) -> bool
- is_action_pressed(action: StringName, exact_match: bool = false) -> bool
- is_anything_pressed() -> bool
- is_joy_button_pressed(device: int, button: int) -> bool
- is_joy_known(device: int) -> bool
- is_joy_motion_sensors_calibrated(device: int) -> bool
- is_joy_motion_sensors_calibrating(device: int) -> bool
- is_joy_motion_sensors_enabled(device: int) -> bool
- is_key_label_pressed(keycode: int) -> bool
- is_key_pressed(keycode: int) -> bool
- is_mouse_button_pressed(button: int) -> bool
- is_physical_key_pressed(keycode: int) -> bool
- parse_input_event(event: InputEvent)
- remove_joy_mapping(guid: String)
- set_accelerometer(value: Vector3)
- set_custom_mouse_cursor(image: Resource, shape: int = 0, hotspot: Vector2 = Vector2(0, 0))
- set_default_cursor_shape(shape: int = 0)
- set_gravity(value: Vector3)
- set_gyroscope(value: Vector3)
- set_joy_light(device: int, color: Color)
- set_joy_motion_sensors_calibration(device: int, calibration_info: Dictionary)
- set_joy_motion_sensors_enabled(device: int, enable: bool)
- set_magnetometer(value: Vector3)
- should_ignore_device(vendor_id: int, product_id: int) -> bool
- start_joy_motion_sensors_calibration(device: int)
- start_joy_vibration(device: int, weak_magnitude: float, strong_magnitude: float, duration: float = 0)
- stop_joy_motion_sensors_calibration(device: int)
- stop_joy_vibration(device: int)
- vibrate_handheld(duration_ms: int = 500, amplitude: float = -1.0)
- warp_mouse(position: Vector2)

**Signals:**
- joy_connection_changed(device: int, connected: bool)

**Enums:**
**MouseMode:** MOUSE_MODE_VISIBLE=0, MOUSE_MODE_HIDDEN=1, MOUSE_MODE_CAPTURED=2, MOUSE_MODE_CONFINED=3, MOUSE_MODE_CONFINED_HIDDEN=4, MOUSE_MODE_MAX=5
**CursorShape:** CURSOR_ARROW=0, CURSOR_IBEAM=1, CURSOR_POINTING_HAND=2, CURSOR_CROSS=3, CURSOR_WAIT=4, CURSOR_BUSY=5, CURSOR_DRAG=6, CURSOR_CAN_DROP=7, CURSOR_FORBIDDEN=8, CURSOR_VSIZE=9, ...


## InputEvent <- Resource

Abstract base class for input events.

**Props:**
- device: int = 0

**Methods:**
- accumulate(with_event: InputEvent) -> bool
- as_text() -> String
- get_action_strength(action: StringName, exact_match: bool = false) -> float
- is_action(action: StringName, exact_match: bool = false) -> bool
- is_action_pressed(action: StringName, allow_echo: bool = false, exact_match: bool = false) -> bool
- is_action_released(action: StringName, exact_match: bool = false) -> bool
- is_action_type() -> bool
- is_canceled() -> bool
- is_echo() -> bool
- is_match(event: InputEvent, exact_match: bool = true) -> bool
- is_pressed() -> bool
- is_released() -> bool
- xformed_by(xform: Transform2D, local_ofs: Vector2 = Vector2(0, 0)) -> InputEvent

**Enums:**
**Constants:** DEVICE_ID_EMULATION=-1


## InputEventAction <- InputEvent

An input event type for actions.

**Props:**
- action: StringName = &""
- event_index: int = -1
- pressed: bool = false
- strength: float = 1.0


## InputEventKey <- InputEventWithModifiers

Represents a key on a keyboard being pressed or released.

**Props:**
- echo: bool = false
- key_label: int (Key) = 0
- keycode: int (Key) = 0
- location: int (KeyLocation) = 0
- physical_keycode: int (Key) = 0
- pressed: bool = false
- unicode: int = 0

**Methods:**
- as_text_key_label() -> String
- as_text_keycode() -> String
- as_text_location() -> String
- as_text_physical_keycode() -> String
- get_key_label_with_modifiers() -> int
- get_keycode_with_modifiers() -> int
- get_physical_keycode_with_modifiers() -> int


## InputEventMouseButton <- InputEventMouse

Represents a mouse button being pressed or released.

**Props:**
- button_index: int (MouseButton) = 0
- canceled: bool = false
- double_click: bool = false
- factor: float = 1.0
- pressed: bool = false


## InputEventMouseMotion <- InputEventMouse

Represents a mouse or a pen movement.

**Props:**
- pen_inverted: bool = false
- pressure: float = 0.0
- relative: Vector2 = Vector2(0, 0)
- screen_relative: Vector2 = Vector2(0, 0)
- screen_velocity: Vector2 = Vector2(0, 0)
- tilt: Vector2 = Vector2(0, 0)
- velocity: Vector2 = Vector2(0, 0)


## ItemList <- Control

A vertical list of selectable items with one or multiple columns.

**Props:**
- allow_reselect: bool = false
- allow_rmb_select: bool = false
- allow_search: bool = true
- auto_height: bool = false
- auto_width: bool = false
- clip_contents: bool = true
- fixed_column_width: int = 0
- fixed_icon_size: Vector2i = Vector2i(0, 0)
- focus_mode: int (Control.FocusMode) = 2
- icon_mode: int (ItemList.IconMode) = 1
- icon_scale: float = 1.0
- item_count: int = 0
- max_columns: int = 1
- max_text_lines: int = 1
- same_column_width: bool = false
- scroll_hint_mode: int (ItemList.ScrollHintMode) = 0
- select_mode: int (ItemList.SelectMode) = 0
- text_overrun_behavior: int (TextServer.OverrunBehavior) = 3
- tile_scroll_hint: bool = false
- wraparound_items: bool = true

**Methods:**
- add_icon_item(icon: Texture2D, selectable: bool = true) -> int
- add_item(text: String, icon: Texture2D = null, selectable: bool = true) -> int
- center_on_current(center_verically: bool = true, center_horizontally: bool = true)
- clear()
- deselect(idx: int)
- deselect_all()
- ensure_current_is_visible()
- force_update_list_size()
- get_h_scroll_bar() -> HScrollBar
- get_item_at_position(position: Vector2, exact: bool = false) -> int
- get_item_auto_translate_mode(idx: int) -> int
- get_item_custom_bg_color(idx: int) -> Color
- get_item_custom_fg_color(idx: int) -> Color
- get_item_icon(idx: int) -> Texture2D
- get_item_icon_modulate(idx: int) -> Color
- get_item_icon_region(idx: int) -> Rect2
- get_item_language(idx: int) -> String
- get_item_metadata(idx: int) -> Variant
- get_item_rect(idx: int, expand: bool = true) -> Rect2
- get_item_text(idx: int) -> String
- get_item_text_direction(idx: int) -> int
- get_item_tooltip(idx: int) -> String
- get_selected_items() -> PackedInt32Array
- get_v_scroll_bar() -> VScrollBar
- is_anything_selected() -> bool
- is_item_disabled(idx: int) -> bool
- is_item_icon_transposed(idx: int) -> bool
- is_item_selectable(idx: int) -> bool
- is_item_tooltip_enabled(idx: int) -> bool
- is_selected(idx: int) -> bool
- move_item(from_idx: int, to_idx: int)
- remove_item(idx: int)
- select(idx: int, single: bool = true)
- set_item_auto_translate_mode(idx: int, mode: int)
- set_item_custom_bg_color(idx: int, custom_bg_color: Color)
- set_item_custom_fg_color(idx: int, custom_fg_color: Color)
- set_item_disabled(idx: int, disabled: bool)
- set_item_icon(idx: int, icon: Texture2D)
- set_item_icon_modulate(idx: int, modulate: Color)
- set_item_icon_region(idx: int, rect: Rect2)
- set_item_icon_transposed(idx: int, transposed: bool)
- set_item_language(idx: int, language: String)
- set_item_metadata(idx: int, metadata: Variant)
- set_item_selectable(idx: int, selectable: bool)
- set_item_text(idx: int, text: String)
- set_item_text_direction(idx: int, direction: int)
- set_item_tooltip(idx: int, tooltip: String)
- set_item_tooltip_enabled(idx: int, enable: bool)
- sort_items_by_text()

**Signals:**
- empty_clicked(at_position: Vector2, mouse_button_index: int)
- item_activated(index: int)
- item_clicked(index: int, at_position: Vector2, mouse_button_index: int)
- item_selected(index: int)
- multi_selected(index: int, selected: bool)

**Enums:**
**IconMode:** ICON_MODE_TOP=0, ICON_MODE_LEFT=1
**SelectMode:** SELECT_SINGLE=0, SELECT_MULTI=1, SELECT_TOGGLE=2
**ScrollHintMode:** SCROLL_HINT_MODE_DISABLED=0, SCROLL_HINT_MODE_BOTH=1, SCROLL_HINT_MODE_TOP=2, SCROLL_HINT_MODE_BOTTOM=3


## Label <- Control

A control for displaying plain text.

**Props:**
- autowrap_mode: int (TextServer.AutowrapMode) = 0
- autowrap_trim_flags: int (TextServer.LineBreakFlag) = 192
- clip_text: bool = false
- ellipsis_char: String = "…"
- horizontal_alignment: int (HorizontalAlignment) = 0
- justification_flags: int (TextServer.JustificationFlag) = 163
- label_settings: LabelSettings
- language: String = ""
- lines_skipped: int = 0
- max_lines_visible: int = -1
- mouse_filter: int (Control.MouseFilter) = 2
- paragraph_separator: String = "\\n"
- size_flags_vertical: int (Control.SizeFlags) = 4
- structured_text_bidi_override: int (TextServer.StructuredTextParser) = 0
- structured_text_bidi_override_options: Array = []
- tab_stops: PackedFloat32Array = PackedFloat32Array()
- text: String = ""
- text_direction: int (Control.TextDirection) = 0
- text_overrun_behavior: int (TextServer.OverrunBehavior) = 0
- uppercase: bool = false
- vertical_alignment: int (VerticalAlignment) = 0
- visible_characters: int = -1
- visible_characters_behavior: int (TextServer.VisibleCharactersBehavior) = 0
- visible_ratio: float = 1.0

**Methods:**
- get_character_bounds(pos: int) -> Rect2
- get_line_count() -> int
- get_line_height(line: int = -1) -> int
- get_total_character_count() -> int
- get_visible_line_count() -> int


## Light2D <- Node2D

Casts light in a 2D environment.

**Props:**
- blend_mode: int (Light2D.BlendMode) = 0
- color: Color = Color(1, 1, 1, 1)
- editor_only: bool = false
- enabled: bool = true
- energy: float = 1.0
- range_item_cull_mask: int = 1
- range_layer_max: int = 0
- range_layer_min: int = 0
- range_z_max: int = 1024
- range_z_min: int = -1024
- shadow_color: Color = Color(0, 0, 0, 0)
- shadow_enabled: bool = false
- shadow_filter: int (Light2D.ShadowFilter) = 0
- shadow_filter_smooth: float = 0.0
- shadow_item_cull_mask: int = 1

**Methods:**
- get_height() -> float
- set_height(height: float)

**Enums:**
**ShadowFilter:** SHADOW_FILTER_NONE=0, SHADOW_FILTER_PCF5=1, SHADOW_FILTER_PCF13=2
**BlendMode:** BLEND_MODE_ADD=0, BLEND_MODE_SUB=1, BLEND_MODE_MIX=2


## Light3D <- VisualInstance3D

Provides a base class for different kinds of light nodes.

**Props:**
- distance_fade_begin: float = 40.0
- distance_fade_enabled: bool = false
- distance_fade_length: float = 10.0
- distance_fade_shadow: float = 50.0
- editor_only: bool = false
- light_angular_distance: float = 0.0
- light_bake_mode: int (Light3D.BakeMode) = 2
- light_color: Color = Color(1, 1, 1, 1)
- light_cull_mask: int = 4294967295
- light_energy: float = 1.0
- light_indirect_energy: float = 1.0
- light_intensity_lumens: float
- light_intensity_lux: float
- light_negative: bool = false
- light_projector: Texture2D
- light_size: float = 0.0
- light_specular: float = 1.0
- light_temperature: float
- light_volumetric_fog_energy: float = 1.0
- shadow_bias: float = 0.1
- shadow_blur: float = 1.0
- shadow_caster_mask: int = 4294967295
- shadow_enabled: bool = false
- shadow_normal_bias: float = 2.0
- shadow_opacity: float = 1.0
- shadow_reverse_cull_face: bool = false
- shadow_transmittance_bias: float = 0.05

**Methods:**
- get_correlated_color() -> Color
- get_param(param: int) -> float
- set_param(param: int, value: float)

**Enums:**
**Param:** PARAM_ENERGY=0, PARAM_INDIRECT_ENERGY=1, PARAM_VOLUMETRIC_FOG_ENERGY=2, PARAM_SPECULAR=3, PARAM_RANGE=4, PARAM_SIZE=5, PARAM_ATTENUATION=6, PARAM_SPOT_ANGLE=7, PARAM_SPOT_ATTENUATION=8, PARAM_SHADOW_MAX_DISTANCE=9, ...
**BakeMode:** BAKE_DISABLED=0, BAKE_STATIC=1, BAKE_DYNAMIC=2


## LineEdit <- Control

An input field for single-line text.

**Props:**
- alignment: int (HorizontalAlignment) = 0
- backspace_deletes_composite_character_enabled: bool = false
- caret_blink: bool = false
- caret_blink_interval: float = 0.65
- caret_column: int = 0
- caret_force_displayed: bool = false
- caret_mid_grapheme: bool = false
- clear_button_enabled: bool = false
- context_menu_enabled: bool = true
- deselect_on_focus_loss_enabled: bool = true
- drag_and_drop_selection_enabled: bool = true
- draw_control_chars: bool = false
- editable: bool = true
- emoji_menu_enabled: bool = true
- expand_to_text_length: bool = false
- flat: bool = false
- focus_mode: int (Control.FocusMode) = 2
- icon_expand_mode: int (LineEdit.ExpandMode) = 0
- keep_editing_on_text_submit: bool = false
- language: String = ""
- max_length: int = 0
- middle_mouse_paste_enabled: bool = true
- mouse_default_cursor_shape: int (Control.CursorShape) = 1
- placeholder_text: String = ""
- right_icon: Texture2D
- right_icon_scale: float = 1.0
- secret: bool = false
- secret_character: String = "•"
- select_all_on_focus: bool = false
- selecting_enabled: bool = true
- shortcut_keys_enabled: bool = true
- structured_text_bidi_override: int (TextServer.StructuredTextParser) = 0
- structured_text_bidi_override_options: Array = []
- text: String = ""
- text_direction: int (Control.TextDirection) = 0
- virtual_keyboard_enabled: bool = true
- virtual_keyboard_show_on_focus: bool = true
- virtual_keyboard_type: int (LineEdit.VirtualKeyboardType) = 0

**Methods:**
- apply_ime()
- cancel_ime()
- clear()
- delete_char_at_caret()
- delete_text(from_column: int, to_column: int)
- deselect()
- edit(hide_focus: bool = false)
- get_menu() -> PopupMenu
- get_next_composite_character_column(column: int) -> int
- get_previous_composite_character_column(column: int) -> int
- get_scroll_offset() -> float
- get_selected_text() -> String
- get_selection_from_column() -> int
- get_selection_to_column() -> int
- has_ime_text() -> bool
- has_redo() -> bool
- has_selection() -> bool
- has_undo() -> bool
- insert_text_at_caret(text: String)
- is_editing() -> bool
- is_menu_visible() -> bool
- menu_option(option: int)
- select(from: int = 0, to: int = -1)
- select_all()
- unedit()

**Signals:**
- editing_toggled(toggled_on: bool)
- text_change_rejected(rejected_substring: String)
- text_changed(new_text: String)
- text_submitted(new_text: String)

**Enums:**
**MenuItems:** MENU_CUT=0, MENU_COPY=1, MENU_PASTE=2, MENU_CLEAR=3, MENU_SELECT_ALL=4, MENU_UNDO=5, MENU_REDO=6, MENU_SUBMENU_TEXT_DIR=7, MENU_DIR_INHERITED=8, MENU_DIR_AUTO=9, ...
**VirtualKeyboardType:** KEYBOARD_TYPE_DEFAULT=0, KEYBOARD_TYPE_MULTILINE=1, KEYBOARD_TYPE_NUMBER=2, KEYBOARD_TYPE_NUMBER_DECIMAL=3, KEYBOARD_TYPE_PHONE=4, KEYBOARD_TYPE_EMAIL_ADDRESS=5, KEYBOARD_TYPE_PASSWORD=6, KEYBOARD_TYPE_URL=7
**ExpandMode:** EXPAND_MODE_ORIGINAL_SIZE=0, EXPAND_MODE_FIT_TO_TEXT=1, EXPAND_MODE_FIT_TO_LINE_EDIT=2


## MarginContainer <- Container

A container that keeps a margin around its child controls.


## Material <- Resource

Virtual base class for applying visual properties to an object, such as color and roughness.

**Props:**
- next_pass: Material
- render_priority: int

**Methods:**
- create_placeholder() -> Resource
- inspect_native_shader_code()

**Enums:**
**Constants:** RENDER_PRIORITY_MAX=127, RENDER_PRIORITY_MIN=-128


## Mesh <- Resource

A Resource that contains vertex array-based geometry.

**Props:**
- lightmap_size_hint: Vector2i = Vector2i(0, 0)

**Methods:**
- create_convex_shape(clean: bool = true, simplify: bool = false) -> ConvexPolygonShape3D
- create_outline(margin: float) -> Mesh
- create_placeholder() -> Resource
- create_trimesh_shape() -> ConcavePolygonShape3D
- generate_triangle_mesh() -> TriangleMesh
- get_aabb() -> AABB
- get_faces() -> PackedVector3Array
- get_surface_count() -> int
- surface_get_arrays(surf_idx: int) -> Array
- surface_get_blend_shape_arrays(surf_idx: int) -> Array[]
- surface_get_material(surf_idx: int) -> Material
- surface_set_material(surf_idx: int, material: Material)

**Enums:**
**PrimitiveType:** PRIMITIVE_POINTS=0, PRIMITIVE_LINES=1, PRIMITIVE_LINE_STRIP=2, PRIMITIVE_TRIANGLES=3, PRIMITIVE_TRIANGLE_STRIP=4
**ArrayType:** ARRAY_VERTEX=0, ARRAY_NORMAL=1, ARRAY_TANGENT=2, ARRAY_COLOR=3, ARRAY_TEX_UV=4, ARRAY_TEX_UV2=5, ARRAY_CUSTOM0=6, ARRAY_CUSTOM1=7, ARRAY_CUSTOM2=8, ARRAY_CUSTOM3=9, ...
**ArrayCustomFormat:** ARRAY_CUSTOM_RGBA8_UNORM=0, ARRAY_CUSTOM_RGBA8_SNORM=1, ARRAY_CUSTOM_RG_HALF=2, ARRAY_CUSTOM_RGBA_HALF=3, ARRAY_CUSTOM_R_FLOAT=4, ARRAY_CUSTOM_RG_FLOAT=5, ARRAY_CUSTOM_RGB_FLOAT=6, ARRAY_CUSTOM_RGBA_FLOAT=7, ARRAY_CUSTOM_MAX=8
**ArrayFormat:** ARRAY_FORMAT_VERTEX=1, ARRAY_FORMAT_NORMAL=2, ARRAY_FORMAT_TANGENT=4, ARRAY_FORMAT_COLOR=8, ARRAY_FORMAT_TEX_UV=16, ARRAY_FORMAT_TEX_UV2=32, ARRAY_FORMAT_CUSTOM0=64, ARRAY_FORMAT_CUSTOM1=128, ARRAY_FORMAT_CUSTOM2=256, ARRAY_FORMAT_CUSTOM3=512, ...
**BlendShapeMode:** BLEND_SHAPE_MODE_NORMALIZED=0, BLEND_SHAPE_MODE_RELATIVE=1


## MeshInstance2D <- Node2D

Node used for displaying a Mesh in 2D.

**Props:**
- mesh: Mesh
- texture: Texture2D

**Signals:**
- texture_changed


## MeshInstance3D <- GeometryInstance3D

Node that instances meshes into a scenario.

**Props:**
- mesh: Mesh
- skeleton: NodePath = NodePath("")
- skin: Skin

**Methods:**
- bake_mesh_from_current_blend_shape_mix(existing: ArrayMesh = null) -> ArrayMesh
- bake_mesh_from_current_skeleton_pose(existing: ArrayMesh = null) -> ArrayMesh
- create_convex_collision(clean: bool = true, simplify: bool = false)
- create_debug_tangents()
- create_multiple_convex_collisions(settings: MeshConvexDecompositionSettings = null)
- create_trimesh_collision()
- find_blend_shape_by_name(name: StringName) -> int
- get_active_material(surface: int) -> Material
- get_blend_shape_count() -> int
- get_blend_shape_value(blend_shape_idx: int) -> float
- get_skin_reference() -> SkinReference
- get_surface_override_material(surface: int) -> Material
- get_surface_override_material_count() -> int
- set_blend_shape_value(blend_shape_idx: int, value: float)
- set_surface_override_material(surface: int, material: Material)


## MultiMeshInstance2D <- Node2D

Node that instances a MultiMesh in 2D.

**Props:**
- multimesh: MultiMesh
- texture: Texture2D

**Signals:**
- texture_changed


## MultiMeshInstance3D <- GeometryInstance3D

Node that instances a MultiMesh.

**Props:**
- multimesh: MultiMesh


## NavigationAgent2D <- Node

A 2D agent used to pathfind to a position while avoiding obstacles.

**Props:**
- avoidance_enabled: bool = false
- avoidance_layers: int = 1
- avoidance_mask: int = 1
- avoidance_priority: float = 1.0
- debug_enabled: bool = false
- debug_path_custom_color: Color = Color(1, 1, 1, 1)
- debug_path_custom_line_width: float = -1.0
- debug_path_custom_point_size: float = 4.0
- debug_use_custom: bool = false
- max_neighbors: int = 10
- max_speed: float = 100.0
- navigation_layers: int = 1
- neighbor_distance: float = 500.0
- path_desired_distance: float = 20.0
- path_max_distance: float = 100.0
- path_metadata_flags: int (NavigationPathQueryParameters2D.PathMetadataFlags) = 7
- path_postprocessing: int (NavigationPathQueryParameters2D.PathPostProcessing) = 0
- path_return_max_length: float = 0.0
- path_return_max_radius: float = 0.0
- path_search_max_distance: float = 0.0
- path_search_max_polygons: int = 4096
- pathfinding_algorithm: int (NavigationPathQueryParameters2D.PathfindingAlgorithm) = 0
- radius: float = 10.0
- simplify_epsilon: float = 0.0
- simplify_path: bool = false
- target_desired_distance: float = 10.0
- target_position: Vector2 = Vector2(0, 0)
- time_horizon_agents: float = 1.0
- time_horizon_obstacles: float = 0.0
- velocity: Vector2 = Vector2(0, 0)

**Methods:**
- distance_to_target() -> float
- get_avoidance_layer_value(layer_number: int) -> bool
- get_avoidance_mask_value(mask_number: int) -> bool
- get_current_navigation_path() -> PackedVector2Array
- get_current_navigation_path_index() -> int
- get_current_navigation_result() -> NavigationPathQueryResult2D
- get_final_position() -> Vector2
- get_navigation_layer_value(layer_number: int) -> bool
- get_navigation_map() -> RID
- get_next_path_position() -> Vector2
- get_path_length() -> float
- get_rid() -> RID
- is_navigation_finished() -> bool
- is_target_reachable() -> bool
- is_target_reached() -> bool
- set_avoidance_layer_value(layer_number: int, value: bool)
- set_avoidance_mask_value(mask_number: int, value: bool)
- set_navigation_layer_value(layer_number: int, value: bool)
- set_navigation_map(navigation_map: RID)
- set_velocity_forced(velocity: Vector2)

**Signals:**
- link_reached(details: Dictionary)
- navigation_finished
- path_changed
- target_reached
- velocity_computed(safe_velocity: Vector2)
- waypoint_reached(details: Dictionary)


## NavigationAgent3D <- Node

A 3D agent used to pathfind to a position while avoiding obstacles.

**Props:**
- avoidance_enabled: bool = false
- avoidance_layers: int = 1
- avoidance_mask: int = 1
- avoidance_priority: float = 1.0
- debug_enabled: bool = false
- debug_path_custom_color: Color = Color(1, 1, 1, 1)
- debug_path_custom_point_size: float = 4.0
- debug_use_custom: bool = false
- height: float = 1.0
- keep_y_velocity: bool = true
- max_neighbors: int = 10
- max_speed: float = 10.0
- navigation_layers: int = 1
- neighbor_distance: float = 50.0
- path_desired_distance: float = 1.0
- path_height_offset: float = 0.0
- path_max_distance: float = 5.0
- path_metadata_flags: int (NavigationPathQueryParameters3D.PathMetadataFlags) = 7
- path_postprocessing: int (NavigationPathQueryParameters3D.PathPostProcessing) = 0
- path_return_max_length: float = 0.0
- path_return_max_radius: float = 0.0
- path_search_max_distance: float = 0.0
- path_search_max_polygons: int = 4096
- pathfinding_algorithm: int (NavigationPathQueryParameters3D.PathfindingAlgorithm) = 0
- radius: float = 0.5
- simplify_epsilon: float = 0.0
- simplify_path: bool = false
- target_desired_distance: float = 1.0
- target_position: Vector3 = Vector3(0, 0, 0)
- time_horizon_agents: float = 1.0
- time_horizon_obstacles: float = 0.0
- use_3d_avoidance: bool = false
- velocity: Vector3 = Vector3(0, 0, 0)

**Methods:**
- distance_to_target() -> float
- get_avoidance_layer_value(layer_number: int) -> bool
- get_avoidance_mask_value(mask_number: int) -> bool
- get_current_navigation_path() -> PackedVector3Array
- get_current_navigation_path_index() -> int
- get_current_navigation_result() -> NavigationPathQueryResult3D
- get_final_position() -> Vector3
- get_navigation_layer_value(layer_number: int) -> bool
- get_navigation_map() -> RID
- get_next_path_position() -> Vector3
- get_path_length() -> float
- get_rid() -> RID
- is_navigation_finished() -> bool
- is_target_reachable() -> bool
- is_target_reached() -> bool
- set_avoidance_layer_value(layer_number: int, value: bool)
- set_avoidance_mask_value(mask_number: int, value: bool)
- set_navigation_layer_value(layer_number: int, value: bool)
- set_navigation_map(navigation_map: RID)
- set_velocity_forced(velocity: Vector3)

**Signals:**
- link_reached(details: Dictionary)
- navigation_finished
- path_changed
- target_reached
- velocity_computed(safe_velocity: Vector3)
- waypoint_reached(details: Dictionary)


## NavigationRegion2D <- Node2D

A traversable 2D region that NavigationAgent2Ds can use for pathfinding.

**Props:**
- enabled: bool = true
- enter_cost: float = 0.0
- navigation_layers: int = 1
- navigation_polygon: NavigationPolygon
- travel_cost: float = 1.0
- use_edge_connections: bool = true

**Methods:**
- bake_navigation_polygon(on_thread: bool = true)
- get_bounds() -> Rect2
- get_navigation_layer_value(layer_number: int) -> bool
- get_navigation_map() -> RID
- get_region_rid() -> RID
- get_rid() -> RID
- is_baking() -> bool
- set_navigation_layer_value(layer_number: int, value: bool)
- set_navigation_map(navigation_map: RID)

**Signals:**
- bake_finished
- navigation_polygon_changed


## NavigationRegion3D <- Node3D

A traversable 3D region that NavigationAgent3Ds can use for pathfinding.

**Props:**
- enabled: bool = true
- enter_cost: float = 0.0
- navigation_layers: int = 1
- navigation_mesh: NavigationMesh
- travel_cost: float = 1.0
- use_edge_connections: bool = true

**Methods:**
- bake_navigation_mesh(on_thread: bool = true)
- get_bounds() -> AABB
- get_navigation_layer_value(layer_number: int) -> bool
- get_navigation_map() -> RID
- get_region_rid() -> RID
- get_rid() -> RID
- is_baking() -> bool
- set_navigation_layer_value(layer_number: int, value: bool)
- set_navigation_map(navigation_map: RID)

**Signals:**
- bake_finished
- navigation_mesh_changed


## Node <- Object

Base class for all scene objects.

**Props:**
- auto_translate_mode: int (Node.AutoTranslateMode) = 0
- editor_description: String = ""
- multiplayer: MultiplayerAPI
- name: StringName
- owner: Node
- physics_interpolation_mode: int (Node.PhysicsInterpolationMode) = 0
- process_mode: int (Node.ProcessMode) = 0
- process_physics_priority: int = 0
- process_priority: int = 0
- process_thread_group: int (Node.ProcessThreadGroup) = 0
- process_thread_group_order: int
- process_thread_messages: int (Node.ProcessThreadMessages)
- scene_file_path: String
- unique_name_in_owner: bool = false

**Methods:**
- add_child(node: Node, force_readable_name: bool = false, internal: int = 0)
- add_sibling(sibling: Node, force_readable_name: bool = false)
- add_to_group(group: StringName, persistent: bool = false)
- atr(message: String, context: StringName = "") -> String
- atr_n(message: String, plural_message: StringName, n: int, context: StringName = "") -> String
- call_deferred_thread_group(method: StringName) -> Variant
- call_thread_safe(method: StringName) -> Variant
- can_auto_translate() -> bool
- can_process() -> bool
- create_tween() -> Tween
- duplicate(flags: int = 15) -> Node
- find_child(pattern: String, recursive: bool = true, owned: bool = true) -> Node
- find_children(pattern: String, type: String = "", recursive: bool = true, owned: bool = true) -> Node[]
- find_parent(pattern: String) -> Node
- get_accessibility_element() -> RID
- get_child(idx: int, include_internal: bool = false) -> Node
- get_child_count(include_internal: bool = false) -> int
- get_children(include_internal: bool = false) -> Node[]
- get_groups() -> StringName[]
- get_index(include_internal: bool = false) -> int
- get_last_exclusive_window() -> Window
- get_multiplayer_authority() -> int
- get_node(path: NodePath) -> Node
- get_node_and_resource(path: NodePath) -> Array
- get_node_or_null(path: NodePath) -> Node
- get_node_rpc_config() -> Variant
- get_orphan_node_ids() -> int[]
- get_parent() -> Node
- get_path() -> NodePath
- get_path_to(node: Node, use_unique_path: bool = false) -> NodePath
- get_physics_process_delta_time() -> float
- get_process_delta_time() -> float
- get_scene_instance_load_placeholder() -> bool
- get_tree() -> SceneTree
- get_tree_string() -> String
- get_tree_string_pretty() -> String
- get_viewport() -> Viewport
- get_window() -> Window
- has_node(path: NodePath) -> bool
- has_node_and_resource(path: NodePath) -> bool
- is_ancestor_of(node: Node) -> bool
- is_displayed_folded() -> bool
- is_editable_instance(node: Node) -> bool
- is_greater_than(node: Node) -> bool
- is_in_group(group: StringName) -> bool
- is_inside_tree() -> bool
- is_multiplayer_authority() -> bool
- is_node_ready() -> bool
- is_part_of_edited_scene() -> bool
- is_physics_interpolated() -> bool
- is_physics_interpolated_and_enabled() -> bool
- is_physics_processing() -> bool
- is_physics_processing_internal() -> bool
- is_processing() -> bool
- is_processing_input() -> bool
- is_processing_internal() -> bool
- is_processing_shortcut_input() -> bool
- is_processing_unhandled_input() -> bool
- is_processing_unhandled_key_input() -> bool
- move_child(child_node: Node, to_index: int)
- notify_deferred_thread_group(what: int)
- notify_thread_safe(what: int)
- print_orphan_nodes()
- print_tree()
- print_tree_pretty()
- propagate_call(method: StringName, args: Array = [], parent_first: bool = false)
- propagate_notification(what: int)
- queue_accessibility_update()
- queue_free()
- remove_child(node: Node)
- remove_from_group(group: StringName)
- reparent(new_parent: Node, keep_global_transform: bool = true)
- replace_by(node: Node, keep_groups: bool = false)
- request_ready()
- reset_physics_interpolation()
- rpc(method: StringName) -> int
- rpc_config(method: StringName, config: Variant)
- rpc_id(peer_id: int, method: StringName) -> int
- set_deferred_thread_group(property: StringName, value: Variant)
- set_display_folded(fold: bool)
- set_editable_instance(node: Node, is_editable: bool)
- set_multiplayer_authority(id: int, recursive: bool = true)
- set_physics_process(enable: bool)
- set_physics_process_internal(enable: bool)
- set_process(enable: bool)
- set_process_input(enable: bool)
- set_process_internal(enable: bool)
- set_process_shortcut_input(enable: bool)
- set_process_unhandled_input(enable: bool)
- set_process_unhandled_key_input(enable: bool)
- set_scene_instance_load_placeholder(load_placeholder: bool)
- set_thread_safe(property: StringName, value: Variant)
- set_translation_domain_inherited()
- update_configuration_warnings()

**Signals:**
- child_entered_tree(node: Node)
- child_exiting_tree(node: Node)
- child_order_changed
- editor_description_changed(node: Node)
- editor_state_changed
- ready
- renamed
- replacing_by(node: Node)
- tree_entered
- tree_exited
- tree_exiting

**Enums:**
**Constants:** NOTIFICATION_ENTER_TREE=10, NOTIFICATION_EXIT_TREE=11, NOTIFICATION_MOVED_IN_PARENT=12, NOTIFICATION_READY=13, NOTIFICATION_PAUSED=14, NOTIFICATION_UNPAUSED=15, NOTIFICATION_PHYSICS_PROCESS=16, NOTIFICATION_PROCESS=17, NOTIFICATION_PARENTED=18, NOTIFICATION_UNPARENTED=19, ...
**ProcessMode:** PROCESS_MODE_INHERIT=0, PROCESS_MODE_PAUSABLE=1, PROCESS_MODE_WHEN_PAUSED=2, PROCESS_MODE_ALWAYS=3, PROCESS_MODE_DISABLED=4
**ProcessThreadGroup:** PROCESS_THREAD_GROUP_INHERIT=0, PROCESS_THREAD_GROUP_MAIN_THREAD=1, PROCESS_THREAD_GROUP_SUB_THREAD=2
**ProcessThreadMessages:** FLAG_PROCESS_THREAD_MESSAGES=1, FLAG_PROCESS_THREAD_MESSAGES_PHYSICS=2, FLAG_PROCESS_THREAD_MESSAGES_ALL=3
**PhysicsInterpolationMode:** PHYSICS_INTERPOLATION_MODE_INHERIT=0, PHYSICS_INTERPOLATION_MODE_ON=1, PHYSICS_INTERPOLATION_MODE_OFF=2
**DuplicateFlags:** DUPLICATE_SIGNALS=1, DUPLICATE_GROUPS=2, DUPLICATE_SCRIPTS=4, DUPLICATE_USE_INSTANTIATION=8, DUPLICATE_INTERNAL_STATE=16, DUPLICATE_DEFAULT=15
**InternalMode:** INTERNAL_MODE_DISABLED=0, INTERNAL_MODE_FRONT=1, INTERNAL_MODE_BACK=2
**AutoTranslateMode:** AUTO_TRANSLATE_MODE_INHERIT=0, AUTO_TRANSLATE_MODE_ALWAYS=1, AUTO_TRANSLATE_MODE_DISABLED=2


## Node2D <- CanvasItem

A 2D game object, inherited by all 2D-related nodes. Has a position, rotation, scale, and skew.

**Props:**
- global_position: Vector2
- global_rotation: float
- global_rotation_degrees: float
- global_scale: Vector2
- global_skew: float
- global_transform: Transform2D
- position: Vector2 = Vector2(0, 0)
- rotation: float = 0.0
- rotation_degrees: float
- scale: Vector2 = Vector2(1, 1)
- skew: float = 0.0
- transform: Transform2D

**Methods:**
- apply_scale(ratio: Vector2)
- get_angle_to(point: Vector2) -> float
- get_relative_transform_to_parent(parent: Node) -> Transform2D
- global_translate(offset: Vector2)
- look_at(point: Vector2)
- move_local_x(delta: float, scaled: bool = false)
- move_local_y(delta: float, scaled: bool = false)
- rotate(radians: float)
- to_global(local_point: Vector2) -> Vector2
- to_local(global_point: Vector2) -> Vector2
- translate(offset: Vector2)


## Node3D <- Node

Base object in 3D space, inherited by all 3D nodes.

**Props:**
- basis: Basis
- global_basis: Basis
- global_position: Vector3
- global_rotation: Vector3
- global_rotation_degrees: Vector3
- global_transform: Transform3D
- position: Vector3 = Vector3(0, 0, 0)
- quaternion: Quaternion
- rotation: Vector3 = Vector3(0, 0, 0)
- rotation_degrees: Vector3
- rotation_edit_mode: int (Node3D.RotationEditMode) = 0
- rotation_order: int (EulerOrder) = 2
- scale: Vector3 = Vector3(1, 1, 1)
- top_level: bool = false
- transform: Transform3D = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)
- visibility_parent: NodePath = NodePath("")
- visible: bool = true

**Methods:**
- add_gizmo(gizmo: Node3DGizmo)
- clear_gizmos()
- clear_subgizmo_selection()
- force_update_transform()
- get_gizmos() -> Node3DGizmo[]
- get_global_transform_interpolated() -> Transform3D
- get_parent_node_3d() -> Node3D
- get_world_3d() -> World3D
- global_rotate(axis: Vector3, angle: float)
- global_scale(scale: Vector3)
- global_translate(offset: Vector3)
- hide()
- is_local_transform_notification_enabled() -> bool
- is_scale_disabled() -> bool
- is_transform_notification_enabled() -> bool
- is_visible_in_tree() -> bool
- look_at(target: Vector3, up: Vector3 = Vector3(0, 1, 0), use_model_front: bool = false)
- look_at_from_position(position: Vector3, target: Vector3, up: Vector3 = Vector3(0, 1, 0), use_model_front: bool = false)
- orthonormalize()
- rotate(axis: Vector3, angle: float)
- rotate_object_local(axis: Vector3, angle: float)
- rotate_x(angle: float)
- rotate_y(angle: float)
- rotate_z(angle: float)
- scale_object_local(scale: Vector3)
- set_disable_scale(disable: bool)
- set_identity()
- set_ignore_transform_notification(enabled: bool)
- set_notify_local_transform(enable: bool)
- set_notify_transform(enable: bool)
- set_subgizmo_selection(gizmo: Node3DGizmo, id: int, transform: Transform3D)
- show()
- to_global(local_point: Vector3) -> Vector3
- to_local(global_point: Vector3) -> Vector3
- translate(offset: Vector3)
- translate_object_local(offset: Vector3)
- update_gizmos()

**Signals:**
- visibility_changed

**Enums:**
**Constants:** NOTIFICATION_TRANSFORM_CHANGED=2000, NOTIFICATION_ENTER_WORLD=41, NOTIFICATION_EXIT_WORLD=42, NOTIFICATION_VISIBILITY_CHANGED=43, NOTIFICATION_LOCAL_TRANSFORM_CHANGED=44
**RotationEditMode:** ROTATION_EDIT_MODE_EULER=0, ROTATION_EDIT_MODE_QUATERNION=1, ROTATION_EDIT_MODE_BASIS=2


## Object

Base class for all other classes in the engine.

**Methods:**
- add_user_signal(signal: String, arguments: Array = [])
- call(method: StringName) -> Variant
- call_deferred(method: StringName) -> Variant
- callv(method: StringName, arg_array: Array) -> Variant
- can_translate_messages() -> bool
- cancel_free()
- connect(signal: StringName, callable: Callable, flags: int = 0) -> int
- disconnect(signal: StringName, callable: Callable)
- emit_signal(signal: StringName) -> int
- free()
- get(property: StringName) -> Variant
- get_class() -> String
- get_incoming_connections() -> Dictionary[]
- get_indexed(property_path: NodePath) -> Variant
- get_instance_id() -> int
- get_meta(name: StringName, default: Variant = null) -> Variant
- get_meta_list() -> StringName[]
- get_method_argument_count(method: StringName) -> int
- get_method_list() -> Dictionary[]
- get_property_list() -> Dictionary[]
- get_script() -> Variant
- get_signal_connection_list(signal: StringName) -> Dictionary[]
- get_signal_list() -> Dictionary[]
- get_translation_domain() -> StringName
- has_connections(signal: StringName) -> bool
- has_meta(name: StringName) -> bool
- has_method(method: StringName) -> bool
- has_signal(signal: StringName) -> bool
- has_user_signal(signal: StringName) -> bool
- is_blocking_signals() -> bool
- is_class(class: String) -> bool
- is_connected(signal: StringName, callable: Callable) -> bool
- is_queued_for_deletion() -> bool
- notification(what: int, reversed: bool = false)
- notify_property_list_changed()
- property_can_revert(property: StringName) -> bool
- property_get_revert(property: StringName) -> Variant
- remove_meta(name: StringName)
- remove_user_signal(signal: StringName)
- set(property: StringName, value: Variant)
- set_block_signals(enable: bool)
- set_deferred(property: StringName, value: Variant)
- set_indexed(property_path: NodePath, value: Variant)
- set_message_translation(enable: bool)
- set_meta(name: StringName, value: Variant)
- set_script(script: Variant)
- set_translation_domain(domain: StringName)
- to_string() -> String
- tr(message: StringName, context: StringName = &"") -> String
- tr_n(message: StringName, plural_message: StringName, n: int, context: StringName = &"") -> String

**Signals:**
- property_list_changed
- script_changed

**Enums:**
**Constants:** NOTIFICATION_POSTINITIALIZE=0, NOTIFICATION_PREDELETE=1, NOTIFICATION_EXTENSION_RELOADED=2
**ConnectFlags:** CONNECT_DEFERRED=1, CONNECT_PERSIST=2, CONNECT_ONE_SHOT=4, CONNECT_REFERENCE_COUNTED=8, CONNECT_APPEND_SOURCE_OBJECT=16


## OmniLight3D <- Light3D

Omnidirectional light, such as a light bulb or a candle.

**Props:**
- light_specular: float = 0.5
- omni_attenuation: float = 1.0
- omni_range: float = 5.0
- omni_shadow_mode: int (OmniLight3D.ShadowMode) = 1
- shadow_normal_bias: float = 1.0

**Enums:**
**ShadowMode:** SHADOW_DUAL_PARABOLOID=0, SHADOW_CUBE=1


## OptionButton <- Button

A button that brings up a dropdown with selectable options when pressed.

**Props:**
- action_mode: int (BaseButton.ActionMode) = 0
- alignment: int (HorizontalAlignment) = 0
- allow_reselect: bool = false
- fit_to_longest_item: bool = true
- item_count: int = 0
- selected: int = -1
- toggle_mode: bool = true

**Methods:**
- add_icon_item(texture: Texture2D, label: String, id: int = -1)
- add_item(label: String, id: int = -1)
- add_separator(text: String = "")
- clear()
- get_item_auto_translate_mode(idx: int) -> int
- get_item_icon(idx: int) -> Texture2D
- get_item_id(idx: int) -> int
- get_item_index(id: int) -> int
- get_item_metadata(idx: int) -> Variant
- get_item_text(idx: int) -> String
- get_item_tooltip(idx: int) -> String
- get_popup() -> PopupMenu
- get_selectable_item(from_last: bool = false) -> int
- get_selected_id() -> int
- get_selected_metadata() -> Variant
- has_selectable_items() -> bool
- is_item_disabled(idx: int) -> bool
- is_item_separator(idx: int) -> bool
- remove_item(idx: int)
- select(idx: int)
- set_disable_shortcuts(disabled: bool)
- set_item_auto_translate_mode(idx: int, mode: int)
- set_item_disabled(idx: int, disabled: bool)
- set_item_icon(idx: int, texture: Texture2D)
- set_item_id(idx: int, id: int)
- set_item_metadata(idx: int, metadata: Variant)
- set_item_text(idx: int, text: String)
- set_item_tooltip(idx: int, tooltip: String)
- show_popup()

**Signals:**
- item_focused(index: int)
- item_selected(index: int)


## PackedScene <- Resource

An abstraction of a serialized scene.

**Methods:**
- can_instantiate() -> bool
- get_state() -> SceneState
- instantiate(edit_state: int = 0) -> Node
- pack(path: Node) -> int

**Enums:**
**GenEditState:** GEN_EDIT_STATE_DISABLED=0, GEN_EDIT_STATE_INSTANCE=1, GEN_EDIT_STATE_MAIN=2, GEN_EDIT_STATE_MAIN_INHERITED=3


## Panel <- Control

A GUI control that displays a StyleBox.


## PanelContainer <- Container

A container that keeps its child controls within the area of a StyleBox.

**Props:**
- mouse_filter: int (Control.MouseFilter) = 0


## Path2D <- Node2D

Contains a Curve2D path for PathFollow2D nodes to follow.

**Props:**
- curve: Curve2D


## Path3D <- Node3D

Contains a Curve3D path for PathFollow3D nodes to follow.

**Props:**
- curve: Curve3D
- debug_custom_color: Color = Color(0, 0, 0, 1)

**Signals:**
- curve_changed
- debug_color_changed


## PathFollow2D <- Node2D

Point sampler for a Path2D.

**Props:**
- cubic_interp: bool = true
- h_offset: float = 0.0
- loop: bool = true
- progress: float = 0.0
- progress_ratio: float = 0.0
- rotates: bool = true
- v_offset: float = 0.0


## PathFollow3D <- Node3D

Point sampler for a Path3D.

**Props:**
- cubic_interp: bool = true
- h_offset: float = 0.0
- loop: bool = true
- progress: float = 0.0
- progress_ratio: float = 0.0
- rotation_mode: int (PathFollow3D.RotationMode) = 3
- tilt_enabled: bool = true
- use_model_front: bool = false
- v_offset: float = 0.0

**Methods:**
- correct_posture(transform: Transform3D, rotation_mode: int) -> Transform3D

**Enums:**
**RotationMode:** ROTATION_NONE=0, ROTATION_Y=1, ROTATION_XY=2, ROTATION_XYZ=3, ROTATION_ORIENTED=4


## Plane

A plane in Hessian normal form.

**Props:**
- d: float = 0.0
- normal: Vector3 = Vector3(0, 0, 0)
- x: float = 0.0
- y: float = 0.0
- z: float = 0.0

**Methods:**
- distance_to(point: Vector3) -> float
- get_center() -> Vector3
- has_point(point: Vector3, tolerance: float = 1e-05) -> bool
- intersect_3(b: Plane, c: Plane) -> Variant
- intersects_ray(from: Vector3, dir: Vector3) -> Variant
- intersects_segment(from: Vector3, to: Vector3) -> Variant
- is_equal_approx(to_plane: Plane) -> bool
- is_finite() -> bool
- is_point_over(point: Vector3) -> bool
- normalized() -> Plane
- project(point: Vector3) -> Vector3

**Enums:**
**Constants:** PLANE_YZ=Plane(1, 0, 0, 0), PLANE_XZ=Plane(0, 1, 0, 0), PLANE_XY=Plane(0, 0, 1, 0)


## PointLight2D <- Light2D

Positional 2D light source.

**Props:**
- height: float = 0.0
- offset: Vector2 = Vector2(0, 0)
- texture: Texture2D
- texture_scale: float = 1.0


## PrimitiveMesh <- Mesh

Base class for all primitive meshes. Handles applying a Material to a primitive mesh.

**Props:**
- add_uv2: bool = false
- custom_aabb: AABB = AABB(0, 0, 0, 0, 0, 0)
- flip_faces: bool = false
- material: Material
- uv2_padding: float = 2.0

**Methods:**
- get_mesh_arrays() -> Array
- request_update()


## ProgressBar <- Range

A control used for visual representation of a percentage.

**Props:**
- editor_preview_indeterminate: bool
- fill_mode: int = 0
- indeterminate: bool = false
- show_percentage: bool = true

**Enums:**
**FillMode:** FILL_BEGIN_TO_END=0, FILL_END_TO_BEGIN=1, FILL_TOP_TO_BOTTOM=2, FILL_BOTTOM_TO_TOP=3


## Quaternion

A unit quaternion used for representing 3D rotations.

**Props:**
- w: float = 1.0
- x: float = 0.0
- y: float = 0.0
- z: float = 0.0

**Methods:**
- angle_to(to: Quaternion) -> float
- dot(with: Quaternion) -> float
- exp() -> Quaternion
- from_euler(euler: Vector3) -> Quaternion
- get_angle() -> float
- get_axis() -> Vector3
- get_euler(order: int = 2) -> Vector3
- inverse() -> Quaternion
- is_equal_approx(to: Quaternion) -> bool
- is_finite() -> bool
- is_normalized() -> bool
- length() -> float
- length_squared() -> float
- log() -> Quaternion
- normalized() -> Quaternion
- slerp(to: Quaternion, weight: float) -> Quaternion
- slerpni(to: Quaternion, weight: float) -> Quaternion
- spherical_cubic_interpolate(b: Quaternion, pre_a: Quaternion, post_b: Quaternion, weight: float) -> Quaternion
- spherical_cubic_interpolate_in_time(b: Quaternion, pre_a: Quaternion, post_b: Quaternion, weight: float, b_t: float, pre_a_t: float, post_b_t: float) -> Quaternion

**Enums:**
**Constants:** IDENTITY=Quaternion(0, 0, 0, 1)


## RayCast2D <- Node2D

A ray in 2D space, used to find the first collision object it intersects.

**Props:**
- collide_with_areas: bool = false
- collide_with_bodies: bool = true
- collision_mask: int = 1
- enabled: bool = true
- exclude_parent: bool = true
- hit_from_inside: bool = false
- target_position: Vector2 = Vector2(0, 50)

**Methods:**
- add_exception(node: CollisionObject2D)
- add_exception_rid(rid: RID)
- clear_exceptions()
- force_raycast_update()
- get_collider() -> Object
- get_collider_rid() -> RID
- get_collider_shape() -> int
- get_collision_mask_value(layer_number: int) -> bool
- get_collision_normal() -> Vector2
- get_collision_point() -> Vector2
- is_colliding() -> bool
- remove_exception(node: CollisionObject2D)
- remove_exception_rid(rid: RID)
- set_collision_mask_value(layer_number: int, value: bool)


## RayCast3D <- Node3D

A ray in 3D space, used to find the first collision object it intersects.

**Props:**
- collide_with_areas: bool = false
- collide_with_bodies: bool = true
- collision_mask: int = 1
- debug_shape_custom_color: Color = Color(0, 0, 0, 1)
- debug_shape_thickness: int = 2
- enabled: bool = true
- exclude_parent: bool = true
- hit_back_faces: bool = true
- hit_from_inside: bool = false
- target_position: Vector3 = Vector3(0, -1, 0)

**Methods:**
- add_exception(node: CollisionObject3D)
- add_exception_rid(rid: RID)
- clear_exceptions()
- force_raycast_update()
- get_collider() -> Object
- get_collider_rid() -> RID
- get_collider_shape() -> int
- get_collision_face_index() -> int
- get_collision_mask_value(layer_number: int) -> bool
- get_collision_normal() -> Vector3
- get_collision_point() -> Vector3
- is_colliding() -> bool
- remove_exception(node: CollisionObject3D)
- remove_exception_rid(rid: RID)
- set_collision_mask_value(layer_number: int, value: bool)


## Rect2

A 2D axis-aligned bounding box using floating-point coordinates.

**Props:**
- end: Vector2 = Vector2(0, 0)
- position: Vector2 = Vector2(0, 0)
- size: Vector2 = Vector2(0, 0)

**Methods:**
- abs() -> Rect2
- encloses(b: Rect2) -> bool
- expand(to: Vector2) -> Rect2
- get_area() -> float
- get_center() -> Vector2
- get_support(direction: Vector2) -> Vector2
- grow(amount: float) -> Rect2
- grow_individual(left: float, top: float, right: float, bottom: float) -> Rect2
- grow_side(side: int, amount: float) -> Rect2
- has_area() -> bool
- has_point(point: Vector2) -> bool
- intersection(b: Rect2) -> Rect2
- intersects(b: Rect2, include_borders: bool = false) -> bool
- is_equal_approx(rect: Rect2) -> bool
- is_finite() -> bool
- merge(b: Rect2) -> Rect2


## RectangleShape2D <- Shape2D

A 2D rectangle shape used for physics collision.

**Props:**
- size: Vector2 = Vector2(20, 20)


## RefCounted <- Object

Base class for reference-counted objects.

**Methods:**
- get_reference_count() -> int
- init_ref() -> bool
- reference() -> bool
- unreference() -> bool


## Resource <- RefCounted

Base class for serializable objects.

**Props:**
- resource_local_to_scene: bool = false
- resource_name: String = ""
- resource_path: String = ""
- resource_scene_unique_id: String

**Methods:**
- duplicate(deep: bool = false) -> Resource
- duplicate_deep(deep_subresources_mode: int = 1) -> Resource
- emit_changed()
- generate_scene_unique_id() -> String
- get_id_for_path(path: String) -> String
- get_local_scene() -> Node
- get_rid() -> RID
- is_built_in() -> bool
- reset_state()
- set_id_for_path(path: String, id: String)
- set_path_cache(path: String)
- setup_local_to_scene()
- take_over_path(path: String)

**Signals:**
- changed
- setup_local_to_scene_requested

**Enums:**
**DeepDuplicateMode:** DEEP_DUPLICATE_NONE=0, DEEP_DUPLICATE_INTERNAL=1, DEEP_DUPLICATE_ALL=2


## RichTextLabel <- Control

A control for displaying text that can contain different font styles, images, and basic formatting.

**Props:**
- autowrap_mode: int (TextServer.AutowrapMode) = 3
- autowrap_trim_flags: int (TextServer.LineBreakFlag) = 192
- bbcode_enabled: bool = false
- clip_contents: bool = true
- context_menu_enabled: bool = false
- custom_effects: Array = []
- deselect_on_focus_loss_enabled: bool = true
- drag_and_drop_selection_enabled: bool = true
- fit_content: bool = false
- focus_mode: int (Control.FocusMode) = 3
- hint_underlined: bool = true
- horizontal_alignment: int (HorizontalAlignment) = 0
- justification_flags: int (TextServer.JustificationFlag) = 163
- language: String = ""
- meta_underlined: bool = true
- progress_bar_delay: int = 1000
- scroll_active: bool = true
- scroll_following: bool = false
- scroll_following_visible_characters: bool = false
- selection_enabled: bool = false
- shortcut_keys_enabled: bool = true
- structured_text_bidi_override: int (TextServer.StructuredTextParser) = 0
- structured_text_bidi_override_options: Array = []
- tab_size: int = 4
- tab_stops: PackedFloat32Array = PackedFloat32Array()
- text: String = ""
- text_direction: int (Control.TextDirection) = 0
- threaded: bool = false
- vertical_alignment: int (VerticalAlignment) = 0
- visible_characters: int = -1
- visible_characters_behavior: int (TextServer.VisibleCharactersBehavior) = 0
- visible_ratio: float = 1.0

**Methods:**
- add_hr(width: int = 90, height: int = 2, color: Color = Color(1, 1, 1, 1), alignment: int = 1, width_in_percent: bool = true, height_in_percent: bool = false)
- add_image(image: Texture2D, width: int = 0, height: int = 0, color: Color = Color(1, 1, 1, 1), inline_align: int = 5, region: Rect2 = Rect2(0, 0, 0, 0), key: Variant = null, pad: bool = false, tooltip: String = "", width_in_percent: bool = false, height_in_percent: bool = false, alt_text: String = "")
- add_text(text: String)
- append_text(bbcode: String)
- clear()
- deselect()
- get_character_line(character: int) -> int
- get_character_paragraph(character: int) -> int
- get_content_height() -> int
- get_content_width() -> int
- get_line_count() -> int
- get_line_height(line: int) -> int
- get_line_offset(line: int) -> float
- get_line_range(line: int) -> Vector2i
- get_line_width(line: int) -> int
- get_menu() -> PopupMenu
- get_paragraph_count() -> int
- get_paragraph_offset(paragraph: int) -> float
- get_parsed_text() -> String
- get_selected_text() -> String
- get_selection_from() -> int
- get_selection_line_offset() -> float
- get_selection_to() -> int
- get_total_character_count() -> int
- get_v_scroll_bar() -> VScrollBar
- get_visible_content_rect() -> Rect2i
- get_visible_line_count() -> int
- get_visible_paragraph_count() -> int
- install_effect(effect: Variant)
- invalidate_paragraph(paragraph: int) -> bool
- is_finished() -> bool
- is_menu_visible() -> bool
- is_ready() -> bool
- menu_option(option: int)
- newline()
- parse_bbcode(bbcode: String)
- parse_expressions_for_values(expressions: PackedStringArray) -> Dictionary
- pop()
- pop_all()
- pop_context()
- push_bgcolor(bgcolor: Color)
- push_bold()
- push_bold_italics()
- push_cell()
- push_color(color: Color)
- push_context()
- push_customfx(effect: RichTextEffect, env: Dictionary)
- push_dropcap(string: String, font: Font, size: int, dropcap_margins: Rect2 = Rect2(0, 0, 0, 0), color: Color = Color(1, 1, 1, 1), outline_size: int = 0, outline_color: Color = Color(0, 0, 0, 0))
- push_fgcolor(fgcolor: Color)
- push_font(font: Font, font_size: int = 0)
- push_font_size(font_size: int)
- push_hint(description: String)
- push_indent(level: int)
- push_italics()
- push_language(language: String)
- push_list(level: int, type: int, capitalize: bool, bullet: String = "•")
- push_meta(data: Variant, underline_mode: int = 1, tooltip: String = "")
- push_mono()
- push_normal()
- push_outline_color(color: Color)
- push_outline_size(outline_size: int)
- push_paragraph(alignment: int, base_direction: int = 0, language: String = "", st_parser: int = 0, justification_flags: int = 163, tab_stops: PackedFloat32Array = PackedFloat32Array())
- push_strikethrough(color: Color = Color(0, 0, 0, 0))
- push_table(columns: int, inline_align: int = 0, align_to_row: int = -1, name: String = "")
- push_underline(color: Color = Color(0, 0, 0, 0))
- reload_effects()
- remove_paragraph(paragraph: int, no_invalidate: bool = false) -> bool
- scroll_to_line(line: int)
- scroll_to_paragraph(paragraph: int)
- scroll_to_selection()
- select_all()
- set_cell_border_color(color: Color)
- set_cell_padding(padding: Rect2)
- set_cell_row_background_color(odd_row_bg: Color, even_row_bg: Color)
- set_cell_size_override(min_size: Vector2, max_size: Vector2)
- set_table_column_expand(column: int, expand: bool, ratio: int = 1, shrink: bool = true)
- set_table_column_name(column: int, name: String)
- update_image(key: Variant, mask: int, image: Texture2D, width: int = 0, height: int = 0, color: Color = Color(1, 1, 1, 1), inline_align: int = 5, region: Rect2 = Rect2(0, 0, 0, 0), pad: bool = false, tooltip: String = "", width_in_percent: bool = false, height_in_percent: bool = false)

**Signals:**
- finished
- meta_clicked(meta: Variant)
- meta_hover_ended(meta: Variant)
- meta_hover_started(meta: Variant)

**Enums:**
**ListType:** LIST_NUMBERS=0, LIST_LETTERS=1, LIST_ROMAN=2, LIST_DOTS=3
**MenuItems:** MENU_COPY=0, MENU_SELECT_ALL=1, MENU_MAX=2
**MetaUnderline:** META_UNDERLINE_NEVER=0, META_UNDERLINE_ALWAYS=1, META_UNDERLINE_ON_HOVER=2
**ImageUpdateMask:** UPDATE_TEXTURE=1, UPDATE_SIZE=2, UPDATE_COLOR=4, UPDATE_ALIGNMENT=8, UPDATE_REGION=16, UPDATE_PAD=32, UPDATE_TOOLTIP=64, UPDATE_WIDTH_IN_PERCENT=128


## RigidBody2D <- PhysicsBody2D

A 2D physics body that is moved by a physics simulation.

**Props:**
- angular_damp: float = 0.0
- angular_damp_mode: int (RigidBody2D.DampMode) = 0
- angular_velocity: float = 0.0
- can_sleep: bool = true
- center_of_mass: Vector2 = Vector2(0, 0)
- center_of_mass_mode: int (RigidBody2D.CenterOfMassMode) = 0
- constant_force: Vector2 = Vector2(0, 0)
- constant_torque: float = 0.0
- contact_monitor: bool = false
- continuous_cd: int (RigidBody2D.CCDMode) = 0
- custom_integrator: bool = false
- freeze: bool = false
- freeze_mode: int (RigidBody2D.FreezeMode) = 0
- gravity_scale: float = 1.0
- inertia: float = 0.0
- linear_damp: float = 0.0
- linear_damp_mode: int (RigidBody2D.DampMode) = 0
- linear_velocity: Vector2 = Vector2(0, 0)
- lock_rotation: bool = false
- mass: float = 1.0
- max_contacts_reported: int = 0
- physics_material_override: PhysicsMaterial
- sleeping: bool = false

**Methods:**
- add_constant_central_force(force: Vector2)
- add_constant_force(force: Vector2, position: Vector2 = Vector2(0, 0))
- add_constant_torque(torque: float)
- apply_central_force(force: Vector2)
- apply_central_impulse(impulse: Vector2 = Vector2(0, 0))
- apply_force(force: Vector2, position: Vector2 = Vector2(0, 0))
- apply_impulse(impulse: Vector2, position: Vector2 = Vector2(0, 0))
- apply_torque(torque: float)
- apply_torque_impulse(torque: float)
- get_colliding_bodies() -> Node2D[]
- get_contact_count() -> int
- set_axis_velocity(axis_velocity: Vector2)

**Signals:**
- body_entered(body: Node)
- body_exited(body: Node)
- body_shape_entered(body_rid: RID, body: Node, body_shape_index: int, local_shape_index: int)
- body_shape_exited(body_rid: RID, body: Node, body_shape_index: int, local_shape_index: int)
- sleeping_state_changed

**Enums:**
**FreezeMode:** FREEZE_MODE_STATIC=0, FREEZE_MODE_KINEMATIC=1
**CenterOfMassMode:** CENTER_OF_MASS_MODE_AUTO=0, CENTER_OF_MASS_MODE_CUSTOM=1
**DampMode:** DAMP_MODE_COMBINE=0, DAMP_MODE_REPLACE=1
**CCDMode:** CCD_MODE_DISABLED=0, CCD_MODE_CAST_RAY=1, CCD_MODE_CAST_SHAPE=2


## RigidBody3D <- PhysicsBody3D

A 3D physics body that is moved by a physics simulation.

**Props:**
- angular_damp: float = 0.0
- angular_damp_mode: int (RigidBody3D.DampMode) = 0
- angular_velocity: Vector3 = Vector3(0, 0, 0)
- can_sleep: bool = true
- center_of_mass: Vector3 = Vector3(0, 0, 0)
- center_of_mass_mode: int (RigidBody3D.CenterOfMassMode) = 0
- constant_force: Vector3 = Vector3(0, 0, 0)
- constant_torque: Vector3 = Vector3(0, 0, 0)
- contact_monitor: bool = false
- continuous_cd: bool = false
- custom_integrator: bool = false
- freeze: bool = false
- freeze_mode: int (RigidBody3D.FreezeMode) = 0
- gravity_scale: float = 1.0
- inertia: Vector3 = Vector3(0, 0, 0)
- linear_damp: float = 0.0
- linear_damp_mode: int (RigidBody3D.DampMode) = 0
- linear_velocity: Vector3 = Vector3(0, 0, 0)
- lock_rotation: bool = false
- mass: float = 1.0
- max_contacts_reported: int = 0
- physics_material_override: PhysicsMaterial
- sleeping: bool = false

**Methods:**
- add_constant_central_force(force: Vector3)
- add_constant_force(force: Vector3, position: Vector3 = Vector3(0, 0, 0))
- add_constant_torque(torque: Vector3)
- apply_central_force(force: Vector3)
- apply_central_impulse(impulse: Vector3)
- apply_force(force: Vector3, position: Vector3 = Vector3(0, 0, 0))
- apply_impulse(impulse: Vector3, position: Vector3 = Vector3(0, 0, 0))
- apply_torque(torque: Vector3)
- apply_torque_impulse(impulse: Vector3)
- get_colliding_bodies() -> Node3D[]
- get_contact_count() -> int
- get_inverse_inertia_tensor() -> Basis
- set_axis_velocity(axis_velocity: Vector3)

**Signals:**
- body_entered(body: Node)
- body_exited(body: Node)
- body_shape_entered(body_rid: RID, body: Node, body_shape_index: int, local_shape_index: int)
- body_shape_exited(body_rid: RID, body: Node, body_shape_index: int, local_shape_index: int)
- sleeping_state_changed

**Enums:**
**FreezeMode:** FREEZE_MODE_STATIC=0, FREEZE_MODE_KINEMATIC=1
**CenterOfMassMode:** CENTER_OF_MASS_MODE_AUTO=0, CENTER_OF_MASS_MODE_CUSTOM=1
**DampMode:** DAMP_MODE_COMBINE=0, DAMP_MODE_REPLACE=1


## SceneTree <- MainLoop

Manages the game loop via a hierarchy of nodes.

**Props:**
- auto_accept_quit: bool = true
- current_scene: Node
- debug_collisions_hint: bool = false
- debug_navigation_hint: bool = false
- debug_paths_hint: bool = false
- edited_scene_root: Node
- multiplayer_poll: bool = true
- paused: bool = false
- physics_interpolation: bool = false
- quit_on_go_back: bool = true
- root: Window

**Methods:**
- call_group(group: StringName, method: StringName)
- call_group_flags(flags: int, group: StringName, method: StringName)
- change_scene_to_file(path: String) -> int
- change_scene_to_node(node: Node) -> int
- change_scene_to_packed(packed_scene: PackedScene) -> int
- create_timer(time_sec: float, process_always: bool = true, process_in_physics: bool = false, ignore_time_scale: bool = false) -> SceneTreeTimer
- create_tween() -> Tween
- get_first_node_in_group(group: StringName) -> Node
- get_frame() -> int
- get_multiplayer(for_path: NodePath = NodePath("")) -> MultiplayerAPI
- get_node_count() -> int
- get_node_count_in_group(group: StringName) -> int
- get_nodes_in_group(group: StringName) -> Node[]
- get_processed_tweens() -> Tween[]
- has_group(name: StringName) -> bool
- is_accessibility_enabled() -> bool
- is_accessibility_supported() -> bool
- notify_group(group: StringName, notification: int)
- notify_group_flags(call_flags: int, group: StringName, notification: int)
- queue_delete(obj: Object)
- quit(exit_code: int = 0)
- reload_current_scene() -> int
- set_group(group: StringName, property: String, value: Variant)
- set_group_flags(call_flags: int, group: StringName, property: String, value: Variant)
- set_multiplayer(multiplayer: MultiplayerAPI, root_path: NodePath = NodePath(""))
- unload_current_scene()

**Signals:**
- node_added(node: Node)
- node_configuration_warning_changed(node: Node)
- node_removed(node: Node)
- node_renamed(node: Node)
- physics_frame
- process_frame
- scene_changed
- tree_changed
- tree_process_mode_changed

**Enums:**
**GroupCallFlags:** GROUP_CALL_DEFAULT=0, GROUP_CALL_REVERSE=1, GROUP_CALL_DEFERRED=2, GROUP_CALL_UNIQUE=4


## ScrollContainer <- Container

A container used to provide scrollbars to a child control when needed.

**Props:**
- clip_contents: bool = true
- draw_focus_border: bool = false
- follow_focus: bool = false
- horizontal_scroll_mode: int (ScrollContainer.ScrollMode) = 1
- scroll_deadzone: int = 0
- scroll_hint_mode: int (ScrollContainer.ScrollHintMode) = 0
- scroll_horizontal: int = 0
- scroll_horizontal_custom_step: float = -1.0
- scroll_vertical: int = 0
- scroll_vertical_custom_step: float = -1.0
- tile_scroll_hint: bool = false
- vertical_scroll_mode: int (ScrollContainer.ScrollMode) = 1

**Methods:**
- ensure_control_visible(control: Control)
- get_h_scroll_bar() -> HScrollBar
- get_v_scroll_bar() -> VScrollBar

**Signals:**
- scroll_ended
- scroll_started

**Enums:**
**ScrollMode:** SCROLL_MODE_DISABLED=0, SCROLL_MODE_AUTO=1, SCROLL_MODE_SHOW_ALWAYS=2, SCROLL_MODE_SHOW_NEVER=3, SCROLL_MODE_RESERVE=4
**ScrollHintMode:** SCROLL_HINT_MODE_DISABLED=0, SCROLL_HINT_MODE_ALL=1, SCROLL_HINT_MODE_TOP_AND_LEFT=2, SCROLL_HINT_MODE_BOTTOM_AND_RIGHT=3


## ShaderMaterial <- Material

A material defined by a custom Shader program and the values of its shader parameters.

**Props:**
- shader: Shader

**Methods:**
- get_shader_parameter(param: StringName) -> Variant
- set_shader_parameter(param: StringName, value: Variant)


## Shape2D <- Resource

Abstract base class for 2D shapes used for physics collision.

**Props:**
- custom_solver_bias: float = 0.0

**Methods:**
- collide(local_xform: Transform2D, with_shape: Shape2D, shape_xform: Transform2D) -> bool
- collide_and_get_contacts(local_xform: Transform2D, with_shape: Shape2D, shape_xform: Transform2D) -> PackedVector2Array
- collide_with_motion(local_xform: Transform2D, local_motion: Vector2, with_shape: Shape2D, shape_xform: Transform2D, shape_motion: Vector2) -> bool
- collide_with_motion_and_get_contacts(local_xform: Transform2D, local_motion: Vector2, with_shape: Shape2D, shape_xform: Transform2D, shape_motion: Vector2) -> PackedVector2Array
- draw(canvas_item: RID, color: Color)
- get_rect() -> Rect2


## Shape3D <- Resource

Abstract base class for 3D shapes used for physics collision.

**Props:**
- custom_solver_bias: float = 0.0
- margin: float = 0.04

**Methods:**
- get_debug_mesh() -> ArrayMesh


## ShapeCast2D <- Node2D

A 2D shape that sweeps a region of space to detect CollisionObject2Ds.

**Props:**
- collide_with_areas: bool = false
- collide_with_bodies: bool = true
- collision_mask: int = 1
- collision_result: Array = []
- enabled: bool = true
- exclude_parent: bool = true
- margin: float = 0.0
- max_results: int = 32
- shape: Shape2D
- target_position: Vector2 = Vector2(0, 50)

**Methods:**
- add_exception(node: CollisionObject2D)
- add_exception_rid(rid: RID)
- clear_exceptions()
- force_shapecast_update()
- get_closest_collision_safe_fraction() -> float
- get_closest_collision_unsafe_fraction() -> float
- get_collider(index: int) -> Object
- get_collider_rid(index: int) -> RID
- get_collider_shape(index: int) -> int
- get_collision_count() -> int
- get_collision_mask_value(layer_number: int) -> bool
- get_collision_normal(index: int) -> Vector2
- get_collision_point(index: int) -> Vector2
- is_colliding() -> bool
- remove_exception(node: CollisionObject2D)
- remove_exception_rid(rid: RID)
- set_collision_mask_value(layer_number: int, value: bool)


## ShapeCast3D <- Node3D

A 3D shape that sweeps a region of space to detect CollisionObject3Ds.

**Props:**
- collide_with_areas: bool = false
- collide_with_bodies: bool = true
- collision_mask: int = 1
- collision_result: Array = []
- debug_shape_custom_color: Color = Color(0, 0, 0, 1)
- enabled: bool = true
- exclude_parent: bool = true
- margin: float = 0.0
- max_results: int = 32
- shape: Shape3D
- target_position: Vector3 = Vector3(0, -1, 0)

**Methods:**
- add_exception(node: CollisionObject3D)
- add_exception_rid(rid: RID)
- clear_exceptions()
- force_shapecast_update()
- get_closest_collision_safe_fraction() -> float
- get_closest_collision_unsafe_fraction() -> float
- get_collider(index: int) -> Object
- get_collider_rid(index: int) -> RID
- get_collider_shape(index: int) -> int
- get_collision_count() -> int
- get_collision_mask_value(layer_number: int) -> bool
- get_collision_normal(index: int) -> Vector3
- get_collision_point(index: int) -> Vector3
- is_colliding() -> bool
- remove_exception(node: CollisionObject3D)
- remove_exception_rid(rid: RID)
- resource_changed(resource: Resource)
- set_collision_mask_value(layer_number: int, value: bool)


## Signal

A built-in type representing a signal of an Object.

**Methods:**
- connect(callable: Callable, flags: int = 0) -> int
- disconnect(callable: Callable)
- emit()
- get_connections() -> Array
- get_name() -> StringName
- get_object() -> Object
- get_object_id() -> int
- has_connections() -> bool
- is_connected(callable: Callable) -> bool
- is_null() -> bool


## Slider <- Range

Abstract base class for sliders.

**Props:**
- editable: bool = true
- focus_mode: int (Control.FocusMode) = 2
- scrollable: bool = true
- step: float = 1.0
- tick_count: int = 0
- ticks_on_borders: bool = false
- ticks_position: int (Slider.TickPosition) = 0

**Signals:**
- drag_ended(value_changed: bool)
- drag_started

**Enums:**
**TickPosition:** TICK_POSITION_BOTTOM_RIGHT=0, TICK_POSITION_TOP_LEFT=1, TICK_POSITION_BOTH=2, TICK_POSITION_CENTER=3


## SphereMesh <- PrimitiveMesh

Class representing a spherical PrimitiveMesh.

**Props:**
- height: float = 1.0
- is_hemisphere: bool = false
- radial_segments: int = 64
- radius: float = 0.5
- rings: int = 32


## SphereShape3D <- Shape3D

A 3D sphere shape used for physics collision.

**Props:**
- radius: float = 0.5


## SpinBox <- Range

An input field for numbers.

**Props:**
- alignment: int (HorizontalAlignment) = 0
- custom_arrow_round: bool = false
- custom_arrow_step: float = 0.0
- editable: bool = true
- prefix: String = ""
- select_all_on_focus: bool = false
- size_flags_vertical: int (Control.SizeFlags) = 1
- step: float = 1.0
- suffix: String = ""
- update_on_text_changed: bool = false

**Methods:**
- apply()
- get_line_edit() -> LineEdit


## SpotLight3D <- Light3D

A spotlight, such as a reflector spotlight or a lantern.

**Props:**
- light_specular: float = 0.5
- shadow_bias: float = 0.03
- shadow_normal_bias: float = 1.0
- spot_angle: float = 45.0
- spot_angle_attenuation: float = 1.0
- spot_attenuation: float = 1.0
- spot_range: float = 5.0


## Sprite2D <- Node2D

General-purpose sprite node.

**Props:**
- centered: bool = true
- flip_h: bool = false
- flip_v: bool = false
- frame: int = 0
- frame_coords: Vector2i = Vector2i(0, 0)
- hframes: int = 1
- offset: Vector2 = Vector2(0, 0)
- region_enabled: bool = false
- region_filter_clip_enabled: bool = false
- region_rect: Rect2 = Rect2(0, 0, 0, 0)
- texture: Texture2D
- vframes: int = 1

**Methods:**
- get_rect() -> Rect2
- is_pixel_opaque(pos: Vector2) -> bool

**Signals:**
- frame_changed
- texture_changed


## Sprite3D <- SpriteBase3D

2D sprite node in a 3D world.

**Props:**
- frame: int = 0
- frame_coords: Vector2i = Vector2i(0, 0)
- hframes: int = 1
- region_enabled: bool = false
- region_rect: Rect2 = Rect2(0, 0, 0, 0)
- texture: Texture2D
- vframes: int = 1

**Signals:**
- frame_changed
- texture_changed


## StandardMaterial3D <- BaseMaterial3D

A PBR (Physically Based Rendering) material to be used on 3D objects.


## StaticBody2D <- PhysicsBody2D

A 2D physics body that can't be moved by external forces. When moved manually, it doesn't affect other bodies in its path.

**Props:**
- constant_angular_velocity: float = 0.0
- constant_linear_velocity: Vector2 = Vector2(0, 0)
- physics_material_override: PhysicsMaterial


## StaticBody3D <- PhysicsBody3D

A 3D physics body that can't be moved by external forces. When moved manually, it doesn't affect other bodies in its path.

**Props:**
- constant_angular_velocity: Vector3 = Vector3(0, 0, 0)
- constant_linear_velocity: Vector3 = Vector3(0, 0, 0)
- physics_material_override: PhysicsMaterial


## StyleBox <- Resource

Abstract base class for defining stylized boxes for UI elements.

**Props:**
- content_margin_bottom: float = -1.0
- content_margin_left: float = -1.0
- content_margin_right: float = -1.0
- content_margin_top: float = -1.0

**Methods:**
- draw(canvas_item: RID, rect: Rect2)
- get_content_margin(margin: int) -> float
- get_current_item_drawn() -> CanvasItem
- get_margin(margin: int) -> float
- get_minimum_size() -> Vector2
- get_offset() -> Vector2
- set_content_margin(margin: int, offset: float)
- set_content_margin_all(offset: float)
- test_mask(point: Vector2, rect: Rect2) -> bool


## TextEdit <- Control

A multiline text editor.

**Props:**
- autowrap_mode: int (TextServer.AutowrapMode) = 3
- backspace_deletes_composite_character_enabled: bool = false
- caret_blink: bool = false
- caret_blink_interval: float = 0.65
- caret_draw_when_editable_disabled: bool = false
- caret_mid_grapheme: bool = false
- caret_move_on_right_click: bool = true
- caret_multiple: bool = true
- caret_type: int (TextEdit.CaretType) = 0
- context_menu_enabled: bool = true
- custom_word_separators: String = ""
- deselect_on_focus_loss_enabled: bool = true
- drag_and_drop_selection_enabled: bool = true
- draw_control_chars: bool = false
- draw_spaces: bool = false
- draw_tabs: bool = false
- editable: bool = true
- emoji_menu_enabled: bool = true
- empty_selection_clipboard_enabled: bool = true
- focus_mode: int (Control.FocusMode) = 2
- highlight_all_occurrences: bool = false
- highlight_current_line: bool = false
- indent_wrapped_lines: bool = false
- language: String = ""
- middle_mouse_paste_enabled: bool = true
- minimap_draw: bool = false
- minimap_width: int = 80
- mouse_default_cursor_shape: int (Control.CursorShape) = 1
- placeholder_text: String = ""
- scroll_fit_content_height: bool = false
- scroll_fit_content_width: bool = false
- scroll_horizontal: int = 0
- scroll_past_end_of_file: bool = false
- scroll_smooth: bool = false
- scroll_v_scroll_speed: float = 80.0
- scroll_vertical: float = 0.0
- selecting_enabled: bool = true
- shortcut_keys_enabled: bool = true
- structured_text_bidi_override: int (TextServer.StructuredTextParser) = 0
- structured_text_bidi_override_options: Array = []
- syntax_highlighter: SyntaxHighlighter
- tab_input_mode: bool = true
- text: String = ""
- text_direction: int (Control.TextDirection) = 0
- use_custom_word_separators: bool = false
- use_default_word_separators: bool = true
- virtual_keyboard_enabled: bool = true
- virtual_keyboard_show_on_focus: bool = true
- wrap_mode: int (TextEdit.LineWrappingMode) = 0

**Methods:**
- add_caret(line: int, column: int) -> int
- add_caret_at_carets(below: bool)
- add_gutter(at: int = -1)
- add_selection_for_next_occurrence()
- adjust_carets_after_edit(caret: int, from_line: int, from_col: int, to_line: int, to_col: int)
- adjust_viewport_to_caret(caret_index: int = 0)
- apply_ime()
- backspace(caret_index: int = -1)
- begin_complex_operation()
- begin_multicaret_edit()
- cancel_ime()
- center_viewport_to_caret(caret_index: int = 0)
- clear()
- clear_undo_history()
- collapse_carets(from_line: int, from_column: int, to_line: int, to_column: int, inclusive: bool = false)
- copy(caret_index: int = -1)
- cut(caret_index: int = -1)
- delete_selection(caret_index: int = -1)
- deselect(caret_index: int = -1)
- end_action()
- end_complex_operation()
- end_multicaret_edit()
- get_caret_column(caret_index: int = 0) -> int
- get_caret_count() -> int
- get_caret_draw_pos(caret_index: int = 0) -> Vector2
- get_caret_index_edit_order() -> PackedInt32Array
- get_caret_line(caret_index: int = 0) -> int
- get_caret_wrap_index(caret_index: int = 0) -> int
- get_first_non_whitespace_column(line: int) -> int
- get_first_visible_line() -> int
- get_gutter_count() -> int
- get_gutter_name(gutter: int) -> String
- get_gutter_type(gutter: int) -> int
- get_gutter_width(gutter: int) -> int
- get_h_scroll_bar() -> HScrollBar
- get_indent_level(line: int) -> int
- get_last_full_visible_line() -> int
- get_last_full_visible_line_wrap_index() -> int
- get_last_unhidden_line() -> int
- get_line(line: int) -> String
- get_line_background_color(line: int) -> Color
- get_line_column_at_pos(position: Vector2i, clamp_line: bool = true, clamp_column: bool = true) -> Vector2i
- get_line_count() -> int
- get_line_gutter_icon(line: int, gutter: int) -> Texture2D
- get_line_gutter_item_color(line: int, gutter: int) -> Color
- get_line_gutter_metadata(line: int, gutter: int) -> Variant
- get_line_gutter_text(line: int, gutter: int) -> String
- get_line_height() -> int
- get_line_ranges_from_carets(only_selections: bool = false, merge_adjacent: bool = true) -> Vector2i[]
- get_line_width(line: int, wrap_index: int = -1) -> int
- get_line_with_ime(line: int) -> String
- get_line_wrap_count(line: int) -> int
- get_line_wrap_index_at_column(line: int, column: int) -> int
- get_line_wrapped_text(line: int) -> PackedStringArray
- get_local_mouse_pos() -> Vector2
- get_menu() -> PopupMenu
- get_minimap_line_at_pos(position: Vector2i) -> int
- get_minimap_visible_lines() -> int
- get_next_composite_character_column(line: int, column: int) -> int
- get_next_visible_line_index_offset_from(line: int, wrap_index: int, visible_amount: int) -> Vector2i
- get_next_visible_line_offset_from(line: int, visible_amount: int) -> int
- get_pos_at_line_column(line: int, column: int) -> Vector2i
- get_previous_composite_character_column(line: int, column: int) -> int
- get_rect_at_line_column(line: int, column: int) -> Rect2i
- get_saved_version() -> int
- get_scroll_pos_for_line(line: int, wrap_index: int = 0) -> float
- get_selected_text(caret_index: int = -1) -> String
- get_selection_at_line_column(line: int, column: int, include_edges: bool = true, only_selections: bool = true) -> int
- get_selection_column(caret_index: int = 0) -> int
- get_selection_from_column(caret_index: int = 0) -> int
- get_selection_from_line(caret_index: int = 0) -> int
- get_selection_line(caret_index: int = 0) -> int
- get_selection_mode() -> int
- get_selection_origin_column(caret_index: int = 0) -> int
- get_selection_origin_line(caret_index: int = 0) -> int
- get_selection_to_column(caret_index: int = 0) -> int
- get_selection_to_line(caret_index: int = 0) -> int
- get_sorted_carets(include_ignored_carets: bool = false) -> PackedInt32Array
- get_tab_size() -> int
- get_total_gutter_width() -> int
- get_total_visible_line_count() -> int
- get_v_scroll_bar() -> VScrollBar
- get_version() -> int
- get_visible_line_count() -> int
- get_visible_line_count_in_range(from_line: int, to_line: int) -> int
- get_word_at_pos(position: Vector2) -> String
- get_word_under_caret(caret_index: int = -1) -> String
- has_ime_text() -> bool
- has_redo() -> bool
- has_selection(caret_index: int = -1) -> bool
- has_undo() -> bool
- insert_line_at(line: int, text: String)
- insert_text(text: String, line: int, column: int, before_selection_begin: bool = true, before_selection_end: bool = false)
- insert_text_at_caret(text: String, caret_index: int = -1)
- is_caret_after_selection_origin(caret_index: int = 0) -> bool
- is_caret_visible(caret_index: int = 0) -> bool
- is_dragging_cursor() -> bool
- is_gutter_clickable(gutter: int) -> bool
- is_gutter_drawn(gutter: int) -> bool
- is_gutter_overwritable(gutter: int) -> bool
- is_in_mulitcaret_edit() -> bool
- is_line_gutter_clickable(line: int, gutter: int) -> bool
- is_line_wrapped(line: int) -> bool
- is_menu_visible() -> bool
- is_mouse_over_selection(edges: bool, caret_index: int = -1) -> bool
- is_overtype_mode_enabled() -> bool
- menu_option(option: int)
- merge_gutters(from_line: int, to_line: int)
- merge_overlapping_carets()
- multicaret_edit_ignore_caret(caret_index: int) -> bool
- paste(caret_index: int = -1)
- paste_primary_clipboard(caret_index: int = -1)
- redo()
- remove_caret(caret: int)
- remove_gutter(gutter: int)
- remove_line_at(line: int, move_carets_down: bool = true)
- remove_secondary_carets()
- remove_text(from_line: int, from_column: int, to_line: int, to_column: int)
- search(text: String, flags: int, from_line: int, from_column: int) -> Vector2i
- select(origin_line: int, origin_column: int, caret_line: int, caret_column: int, caret_index: int = 0)
- select_all()
- select_word_under_caret(caret_index: int = -1)
- set_caret_column(column: int, adjust_viewport: bool = true, caret_index: int = 0)
- set_caret_line(line: int, adjust_viewport: bool = true, can_be_hidden: bool = true, wrap_index: int = 0, caret_index: int = 0)
- set_gutter_clickable(gutter: int, clickable: bool)
- set_gutter_custom_draw(column: int, draw_callback: Callable)
- set_gutter_draw(gutter: int, draw: bool)
- set_gutter_name(gutter: int, name: String)
- set_gutter_overwritable(gutter: int, overwritable: bool)
- set_gutter_type(gutter: int, type: int)
- set_gutter_width(gutter: int, width: int)
- set_line(line: int, new_text: String)
- set_line_as_center_visible(line: int, wrap_index: int = 0)
- set_line_as_first_visible(line: int, wrap_index: int = 0)
- set_line_as_last_visible(line: int, wrap_index: int = 0)
- set_line_background_color(line: int, color: Color)
- set_line_gutter_clickable(line: int, gutter: int, clickable: bool)
- set_line_gutter_icon(line: int, gutter: int, icon: Texture2D)
- set_line_gutter_item_color(line: int, gutter: int, color: Color)
- set_line_gutter_metadata(line: int, gutter: int, metadata: Variant)
- set_line_gutter_text(line: int, gutter: int, text: String)
- set_overtype_mode_enabled(enabled: bool)
- set_search_flags(flags: int)
- set_search_text(search_text: String)
- set_selection_mode(mode: int)
- set_selection_origin_column(column: int, caret_index: int = 0)
- set_selection_origin_line(line: int, can_be_hidden: bool = true, wrap_index: int = -1, caret_index: int = 0)
- set_tab_size(size: int)
- set_tooltip_request_func(callback: Callable)
- skip_selection_for_next_occurrence()
- start_action(action: int)
- swap_lines(from_line: int, to_line: int)
- tag_saved_version()
- undo()

**Signals:**
- caret_changed
- gutter_added
- gutter_clicked(line: int, gutter: int)
- gutter_removed
- lines_edited_from(from_line: int, to_line: int)
- text_changed
- text_set

**Enums:**
**MenuItems:** MENU_CUT=0, MENU_COPY=1, MENU_PASTE=2, MENU_CLEAR=3, MENU_SELECT_ALL=4, MENU_UNDO=5, MENU_REDO=6, MENU_SUBMENU_TEXT_DIR=7, MENU_DIR_INHERITED=8, MENU_DIR_AUTO=9, ...
**EditAction:** ACTION_NONE=0, ACTION_TYPING=1, ACTION_BACKSPACE=2, ACTION_DELETE=3
**SearchFlags:** SEARCH_MATCH_CASE=1, SEARCH_WHOLE_WORDS=2, SEARCH_BACKWARDS=4
**CaretType:** CARET_TYPE_LINE=0, CARET_TYPE_BLOCK=1
**SelectionMode:** SELECTION_MODE_NONE=0, SELECTION_MODE_SHIFT=1, SELECTION_MODE_POINTER=2, SELECTION_MODE_WORD=3, SELECTION_MODE_LINE=4
**LineWrappingMode:** LINE_WRAPPING_NONE=0, LINE_WRAPPING_BOUNDARY=1
**GutterType:** GUTTER_TYPE_STRING=0, GUTTER_TYPE_ICON=1, GUTTER_TYPE_CUSTOM=2


## Texture2D <- Texture

Texture for 2D and 3D.

**Methods:**
- create_placeholder() -> Resource
- draw(canvas_item: RID, position: Vector2, modulate: Color = Color(1, 1, 1, 1), transpose: bool = false)
- draw_rect(canvas_item: RID, rect: Rect2, tile: bool, modulate: Color = Color(1, 1, 1, 1), transpose: bool = false)
- draw_rect_region(canvas_item: RID, rect: Rect2, src_rect: Rect2, modulate: Color = Color(1, 1, 1, 1), transpose: bool = false, clip_uv: bool = true)
- get_height() -> int
- get_image() -> Image
- get_size() -> Vector2
- get_width() -> int
- has_alpha() -> bool


## TextureButton <- BaseButton

Texture-based button. Supports Pressed, Hover, Disabled and Focused states.

**Props:**
- flip_h: bool = false
- flip_v: bool = false
- ignore_texture_size: bool = false
- stretch_mode: int (TextureButton.StretchMode) = 2
- texture_click_mask: BitMap
- texture_disabled: Texture2D
- texture_focused: Texture2D
- texture_hover: Texture2D
- texture_normal: Texture2D
- texture_pressed: Texture2D

**Enums:**
**StretchMode:** STRETCH_SCALE=0, STRETCH_TILE=1, STRETCH_KEEP=2, STRETCH_KEEP_CENTERED=3, STRETCH_KEEP_ASPECT=4, STRETCH_KEEP_ASPECT_CENTERED=5, STRETCH_KEEP_ASPECT_COVERED=6


## TextureRect <- Control

A control that displays a texture.

**Props:**
- expand_mode: int (TextureRect.ExpandMode) = 0
- flip_h: bool = false
- flip_v: bool = false
- mouse_filter: int (Control.MouseFilter) = 1
- stretch_mode: int (TextureRect.StretchMode) = 0
- texture: Texture2D

**Enums:**
**ExpandMode:** EXPAND_KEEP_SIZE=0, EXPAND_IGNORE_SIZE=1, EXPAND_FIT_WIDTH=2, EXPAND_FIT_WIDTH_PROPORTIONAL=3, EXPAND_FIT_HEIGHT=4, EXPAND_FIT_HEIGHT_PROPORTIONAL=5
**StretchMode:** STRETCH_SCALE=0, STRETCH_TILE=1, STRETCH_KEEP=2, STRETCH_KEEP_CENTERED=3, STRETCH_KEEP_ASPECT=4, STRETCH_KEEP_ASPECT_CENTERED=5, STRETCH_KEEP_ASPECT_COVERED=6


## Theme <- Resource

A resource used for styling/skinning Controls and Windows.

**Props:**
- default_base_scale: float = 0.0
- default_font: Font
- default_font_size: int = -1

**Methods:**
- add_type(theme_type: StringName)
- clear()
- clear_color(name: StringName, theme_type: StringName)
- clear_constant(name: StringName, theme_type: StringName)
- clear_font(name: StringName, theme_type: StringName)
- clear_font_size(name: StringName, theme_type: StringName)
- clear_icon(name: StringName, theme_type: StringName)
- clear_stylebox(name: StringName, theme_type: StringName)
- clear_theme_item(data_type: int, name: StringName, theme_type: StringName)
- clear_type_variation(theme_type: StringName)
- get_color(name: StringName, theme_type: StringName) -> Color
- get_color_list(theme_type: String) -> PackedStringArray
- get_color_type_list() -> PackedStringArray
- get_constant(name: StringName, theme_type: StringName) -> int
- get_constant_list(theme_type: String) -> PackedStringArray
- get_constant_type_list() -> PackedStringArray
- get_font(name: StringName, theme_type: StringName) -> Font
- get_font_list(theme_type: String) -> PackedStringArray
- get_font_size(name: StringName, theme_type: StringName) -> int
- get_font_size_list(theme_type: String) -> PackedStringArray
- get_font_size_type_list() -> PackedStringArray
- get_font_type_list() -> PackedStringArray
- get_icon(name: StringName, theme_type: StringName) -> Texture2D
- get_icon_list(theme_type: String) -> PackedStringArray
- get_icon_type_list() -> PackedStringArray
- get_stylebox(name: StringName, theme_type: StringName) -> StyleBox
- get_stylebox_list(theme_type: String) -> PackedStringArray
- get_stylebox_type_list() -> PackedStringArray
- get_theme_item(data_type: int, name: StringName, theme_type: StringName) -> Variant
- get_theme_item_list(data_type: int, theme_type: String) -> PackedStringArray
- get_theme_item_type_list(data_type: int) -> PackedStringArray
- get_type_list() -> PackedStringArray
- get_type_variation_base(theme_type: StringName) -> StringName
- get_type_variation_list(base_type: StringName) -> PackedStringArray
- has_color(name: StringName, theme_type: StringName) -> bool
- has_constant(name: StringName, theme_type: StringName) -> bool
- has_default_base_scale() -> bool
- has_default_font() -> bool
- has_default_font_size() -> bool
- has_font(name: StringName, theme_type: StringName) -> bool
- has_font_size(name: StringName, theme_type: StringName) -> bool
- has_icon(name: StringName, theme_type: StringName) -> bool
- has_stylebox(name: StringName, theme_type: StringName) -> bool
- has_theme_item(data_type: int, name: StringName, theme_type: StringName) -> bool
- is_type_variation(theme_type: StringName, base_type: StringName) -> bool
- merge_with(other: Theme)
- remove_type(theme_type: StringName)
- rename_color(old_name: StringName, name: StringName, theme_type: StringName)
- rename_constant(old_name: StringName, name: StringName, theme_type: StringName)
- rename_font(old_name: StringName, name: StringName, theme_type: StringName)
- rename_font_size(old_name: StringName, name: StringName, theme_type: StringName)
- rename_icon(old_name: StringName, name: StringName, theme_type: StringName)
- rename_stylebox(old_name: StringName, name: StringName, theme_type: StringName)
- rename_theme_item(data_type: int, old_name: StringName, name: StringName, theme_type: StringName)
- rename_type(old_theme_type: StringName, theme_type: StringName)
- set_color(name: StringName, theme_type: StringName, color: Color)
- set_constant(name: StringName, theme_type: StringName, constant: int)
- set_font(name: StringName, theme_type: StringName, font: Font)
- set_font_size(name: StringName, theme_type: StringName, font_size: int)
- set_icon(name: StringName, theme_type: StringName, texture: Texture2D)
- set_stylebox(name: StringName, theme_type: StringName, texture: StyleBox)
- set_theme_item(data_type: int, name: StringName, theme_type: StringName, value: Variant)
- set_type_variation(theme_type: StringName, base_type: StringName)

**Enums:**
**DataType:** DATA_TYPE_COLOR=0, DATA_TYPE_CONSTANT=1, DATA_TYPE_FONT=2, DATA_TYPE_FONT_SIZE=3, DATA_TYPE_ICON=4, DATA_TYPE_STYLEBOX=5, DATA_TYPE_MAX=6


## TileMapLayer <- Node2D

Node for 2D tile-based maps.

**Props:**
- collision_enabled: bool = true
- collision_visibility_mode: int (TileMapLayer.DebugVisibilityMode) = 0
- enabled: bool = true
- navigation_enabled: bool = true
- navigation_visibility_mode: int (TileMapLayer.DebugVisibilityMode) = 0
- occlusion_enabled: bool = true
- physics_quadrant_size: int = 16
- rendering_quadrant_size: int = 16
- tile_map_data: PackedByteArray = PackedByteArray()
- tile_set: TileSet
- use_kinematic_bodies: bool = false
- x_draw_order_reversed: bool = false
- y_sort_origin: int = 0

**Methods:**
- clear()
- erase_cell(coords: Vector2i)
- fix_invalid_tiles()
- get_cell_alternative_tile(coords: Vector2i) -> int
- get_cell_atlas_coords(coords: Vector2i) -> Vector2i
- get_cell_source_id(coords: Vector2i) -> int
- get_cell_tile_data(coords: Vector2i) -> TileData
- get_coords_for_body_rid(body: RID) -> Vector2i
- get_navigation_map() -> RID
- get_neighbor_cell(coords: Vector2i, neighbor: int) -> Vector2i
- get_pattern(coords_array: Vector2i[]) -> TileMapPattern
- get_surrounding_cells(coords: Vector2i) -> Vector2i[]
- get_used_cells() -> Vector2i[]
- get_used_cells_by_id(source_id: int = -1, atlas_coords: Vector2i = Vector2i(-1, -1), alternative_tile: int = -1) -> Vector2i[]
- get_used_rect() -> Rect2i
- has_body_rid(body: RID) -> bool
- is_cell_flipped_h(coords: Vector2i) -> bool
- is_cell_flipped_v(coords: Vector2i) -> bool
- is_cell_transposed(coords: Vector2i) -> bool
- local_to_map(local_position: Vector2) -> Vector2i
- map_pattern(position_in_tilemap: Vector2i, coords_in_pattern: Vector2i, pattern: TileMapPattern) -> Vector2i
- map_to_local(map_position: Vector2i) -> Vector2
- notify_runtime_tile_data_update()
- set_cell(coords: Vector2i, source_id: int = -1, atlas_coords: Vector2i = Vector2i(-1, -1), alternative_tile: int = 0)
- set_cells_terrain_connect(cells: Vector2i[], terrain_set: int, terrain: int, ignore_empty_terrains: bool = true)
- set_cells_terrain_path(path: Vector2i[], terrain_set: int, terrain: int, ignore_empty_terrains: bool = true)
- set_navigation_map(map: RID)
- set_pattern(position: Vector2i, pattern: TileMapPattern)
- update_internals()

**Signals:**
- changed

**Enums:**
**DebugVisibilityMode:** DEBUG_VISIBILITY_MODE_DEFAULT=0, DEBUG_VISIBILITY_MODE_FORCE_HIDE=2, DEBUG_VISIBILITY_MODE_FORCE_SHOW=1


## TileSet <- Resource

Tile library for tilemaps.

**Props:**
- tile_layout: int (TileSet.TileLayout) = 0
- tile_offset_axis: int (TileSet.TileOffsetAxis) = 0
- tile_shape: int (TileSet.TileShape) = 0
- tile_size: Vector2i = Vector2i(16, 16)
- uv_clipping: bool = false

**Methods:**
- add_custom_data_layer(to_position: int = -1)
- add_navigation_layer(to_position: int = -1)
- add_occlusion_layer(to_position: int = -1)
- add_pattern(pattern: TileMapPattern, index: int = -1) -> int
- add_physics_layer(to_position: int = -1)
- add_source(source: TileSetSource, atlas_source_id_override: int = -1) -> int
- add_terrain(terrain_set: int, to_position: int = -1)
- add_terrain_set(to_position: int = -1)
- cleanup_invalid_tile_proxies()
- clear_tile_proxies()
- get_alternative_level_tile_proxy(source_from: int, coords_from: Vector2i, alternative_from: int) -> Array
- get_coords_level_tile_proxy(source_from: int, coords_from: Vector2i) -> Array
- get_custom_data_layer_by_name(layer_name: String) -> int
- get_custom_data_layer_name(layer_index: int) -> String
- get_custom_data_layer_type(layer_index: int) -> int
- get_custom_data_layers_count() -> int
- get_navigation_layer_layer_value(layer_index: int, layer_number: int) -> bool
- get_navigation_layer_layers(layer_index: int) -> int
- get_navigation_layers_count() -> int
- get_next_source_id() -> int
- get_occlusion_layer_light_mask(layer_index: int) -> int
- get_occlusion_layer_sdf_collision(layer_index: int) -> bool
- get_occlusion_layers_count() -> int
- get_pattern(index: int = -1) -> TileMapPattern
- get_patterns_count() -> int
- get_physics_layer_collision_layer(layer_index: int) -> int
- get_physics_layer_collision_mask(layer_index: int) -> int
- get_physics_layer_collision_priority(layer_index: int) -> float
- get_physics_layer_physics_material(layer_index: int) -> PhysicsMaterial
- get_physics_layers_count() -> int
- get_source(source_id: int) -> TileSetSource
- get_source_count() -> int
- get_source_id(index: int) -> int
- get_source_level_tile_proxy(source_from: int) -> int
- get_terrain_color(terrain_set: int, terrain_index: int) -> Color
- get_terrain_name(terrain_set: int, terrain_index: int) -> String
- get_terrain_set_mode(terrain_set: int) -> int
- get_terrain_sets_count() -> int
- get_terrains_count(terrain_set: int) -> int
- has_alternative_level_tile_proxy(source_from: int, coords_from: Vector2i, alternative_from: int) -> bool
- has_coords_level_tile_proxy(source_from: int, coords_from: Vector2i) -> bool
- has_custom_data_layer_by_name(layer_name: String) -> bool
- has_source(source_id: int) -> bool
- has_source_level_tile_proxy(source_from: int) -> bool
- map_tile_proxy(source_from: int, coords_from: Vector2i, alternative_from: int) -> Array
- move_custom_data_layer(layer_index: int, to_position: int)
- move_navigation_layer(layer_index: int, to_position: int)
- move_occlusion_layer(layer_index: int, to_position: int)
- move_physics_layer(layer_index: int, to_position: int)
- move_terrain(terrain_set: int, terrain_index: int, to_position: int)
- move_terrain_set(terrain_set: int, to_position: int)
- remove_alternative_level_tile_proxy(source_from: int, coords_from: Vector2i, alternative_from: int)
- remove_coords_level_tile_proxy(source_from: int, coords_from: Vector2i)
- remove_custom_data_layer(layer_index: int)
- remove_navigation_layer(layer_index: int)
- remove_occlusion_layer(layer_index: int)
- remove_pattern(index: int)
- remove_physics_layer(layer_index: int)
- remove_source(source_id: int)
- remove_source_level_tile_proxy(source_from: int)
- remove_terrain(terrain_set: int, terrain_index: int)
- remove_terrain_set(terrain_set: int)
- set_alternative_level_tile_proxy(source_from: int, coords_from: Vector2i, alternative_from: int, source_to: int, coords_to: Vector2i, alternative_to: int)
- set_coords_level_tile_proxy(p_source_from: int, coords_from: Vector2i, source_to: int, coords_to: Vector2i)
- set_custom_data_layer_name(layer_index: int, layer_name: String)
- set_custom_data_layer_type(layer_index: int, layer_type: int)
- set_navigation_layer_layer_value(layer_index: int, layer_number: int, value: bool)
- set_navigation_layer_layers(layer_index: int, layers: int)
- set_occlusion_layer_light_mask(layer_index: int, light_mask: int)
- set_occlusion_layer_sdf_collision(layer_index: int, sdf_collision: bool)
- set_physics_layer_collision_layer(layer_index: int, layer: int)
- set_physics_layer_collision_mask(layer_index: int, mask: int)
- set_physics_layer_collision_priority(layer_index: int, priority: float)
- set_physics_layer_physics_material(layer_index: int, physics_material: PhysicsMaterial)
- set_source_id(source_id: int, new_source_id: int)
- set_source_level_tile_proxy(source_from: int, source_to: int)
- set_terrain_color(terrain_set: int, terrain_index: int, color: Color)
- set_terrain_name(terrain_set: int, terrain_index: int, name: String)
- set_terrain_set_mode(terrain_set: int, mode: int)

**Enums:**
**TileShape:** TILE_SHAPE_SQUARE=0, TILE_SHAPE_ISOMETRIC=1, TILE_SHAPE_HALF_OFFSET_SQUARE=2, TILE_SHAPE_HEXAGON=3
**TileLayout:** TILE_LAYOUT_STACKED=0, TILE_LAYOUT_STACKED_OFFSET=1, TILE_LAYOUT_STAIRS_RIGHT=2, TILE_LAYOUT_STAIRS_DOWN=3, TILE_LAYOUT_DIAMOND_RIGHT=4, TILE_LAYOUT_DIAMOND_DOWN=5
**TileOffsetAxis:** TILE_OFFSET_AXIS_HORIZONTAL=0, TILE_OFFSET_AXIS_VERTICAL=1
**CellNeighbor:** CELL_NEIGHBOR_RIGHT_SIDE=0, CELL_NEIGHBOR_RIGHT_CORNER=1, CELL_NEIGHBOR_BOTTOM_RIGHT_SIDE=2, CELL_NEIGHBOR_BOTTOM_RIGHT_CORNER=3, CELL_NEIGHBOR_BOTTOM_SIDE=4, CELL_NEIGHBOR_BOTTOM_CORNER=5, CELL_NEIGHBOR_BOTTOM_LEFT_SIDE=6, CELL_NEIGHBOR_BOTTOM_LEFT_CORNER=7, CELL_NEIGHBOR_LEFT_SIDE=8, CELL_NEIGHBOR_LEFT_CORNER=9, ...
**TerrainMode:** TERRAIN_MODE_MATCH_CORNERS_AND_SIDES=0, TERRAIN_MODE_MATCH_CORNERS=1, TERRAIN_MODE_MATCH_SIDES=2


## Timer <- Node

A countdown timer.

**Props:**
- autostart: bool = false
- ignore_time_scale: bool = false
- one_shot: bool = false
- paused: bool
- process_callback: int (Timer.TimerProcessCallback) = 1
- time_left: float
- wait_time: float = 1.0

**Methods:**
- is_stopped() -> bool
- start(time_sec: float = -1)
- stop()

**Signals:**
- timeout

**Enums:**
**TimerProcessCallback:** TIMER_PROCESS_PHYSICS=0, TIMER_PROCESS_IDLE=1


## Transform2D

A 2×3 matrix representing a 2D transformation.

**Props:**
- origin: Vector2 = Vector2(0, 0)
- x: Vector2 = Vector2(1, 0)
- y: Vector2 = Vector2(0, 1)

**Methods:**
- affine_inverse() -> Transform2D
- basis_xform(v: Vector2) -> Vector2
- basis_xform_inv(v: Vector2) -> Vector2
- determinant() -> float
- get_origin() -> Vector2
- get_rotation() -> float
- get_scale() -> Vector2
- get_skew() -> float
- interpolate_with(xform: Transform2D, weight: float) -> Transform2D
- inverse() -> Transform2D
- is_conformal() -> bool
- is_equal_approx(xform: Transform2D) -> bool
- is_finite() -> bool
- looking_at(target: Vector2 = Vector2(0, 0)) -> Transform2D
- orthonormalized() -> Transform2D
- rotated(angle: float) -> Transform2D
- rotated_local(angle: float) -> Transform2D
- scaled(scale: Vector2) -> Transform2D
- scaled_local(scale: Vector2) -> Transform2D
- translated(offset: Vector2) -> Transform2D
- translated_local(offset: Vector2) -> Transform2D

**Enums:**
**Constants:** IDENTITY=Transform2D(1, 0, 0, 1, 0, 0), FLIP_X=Transform2D(-1, 0, 0, 1, 0, 0), FLIP_Y=Transform2D(1, 0, 0, -1, 0, 0)


## Transform3D

A 3×4 matrix representing a 3D transformation.

**Props:**
- basis: Basis = Basis(1, 0, 0, 0, 1, 0, 0, 0, 1)
- origin: Vector3 = Vector3(0, 0, 0)

**Methods:**
- affine_inverse() -> Transform3D
- interpolate_with(xform: Transform3D, weight: float) -> Transform3D
- inverse() -> Transform3D
- is_equal_approx(xform: Transform3D) -> bool
- is_finite() -> bool
- looking_at(target: Vector3, up: Vector3 = Vector3(0, 1, 0), use_model_front: bool = false) -> Transform3D
- orthonormalized() -> Transform3D
- rotated(axis: Vector3, angle: float) -> Transform3D
- rotated_local(axis: Vector3, angle: float) -> Transform3D
- scaled(scale: Vector3) -> Transform3D
- scaled_local(scale: Vector3) -> Transform3D
- translated(offset: Vector3) -> Transform3D
- translated_local(offset: Vector3) -> Transform3D

**Enums:**
**Constants:** IDENTITY=Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0), FLIP_X=Transform3D(-1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0), FLIP_Y=Transform3D(1, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0), FLIP_Z=Transform3D(1, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0)


## Tree <- Control

A control used to show a set of internal TreeItems in a hierarchical structure.

**Props:**
- allow_reselect: bool = false
- allow_rmb_select: bool = false
- allow_search: bool = true
- auto_tooltip: bool = true
- clip_contents: bool = true
- column_titles_visible: bool = false
- columns: int = 1
- drop_mode_flags: int = 0
- enable_drag_unfolding: bool = true
- enable_recursive_folding: bool = true
- focus_mode: int (Control.FocusMode) = 2
- hide_folding: bool = false
- hide_root: bool = false
- scroll_hint_mode: int (Tree.ScrollHintMode) = 0
- scroll_horizontal_enabled: bool = true
- scroll_vertical_enabled: bool = true
- select_mode: int (Tree.SelectMode) = 0
- tile_scroll_hint: bool = false

**Methods:**
- clear()
- create_item(parent: TreeItem = null, index: int = -1) -> TreeItem
- deselect_all()
- edit_selected(force_edit: bool = false) -> bool
- ensure_cursor_is_visible()
- get_button_id_at_position(position: Vector2) -> int
- get_column_at_position(position: Vector2) -> int
- get_column_expand_ratio(column: int) -> int
- get_column_title(column: int) -> String
- get_column_title_alignment(column: int) -> int
- get_column_title_direction(column: int) -> int
- get_column_title_language(column: int) -> String
- get_column_title_tooltip_text(column: int) -> String
- get_column_width(column: int) -> int
- get_custom_popup_rect() -> Rect2
- get_drop_section_at_position(position: Vector2) -> int
- get_edited() -> TreeItem
- get_edited_column() -> int
- get_item_area_rect(item: TreeItem, column: int = -1, button_index: int = -1) -> Rect2
- get_item_at_position(position: Vector2) -> TreeItem
- get_next_selected(from: TreeItem) -> TreeItem
- get_pressed_button() -> int
- get_root() -> TreeItem
- get_scroll() -> Vector2
- get_selected() -> TreeItem
- get_selected_column() -> int
- is_column_clipping_content(column: int) -> bool
- is_column_expanding(column: int) -> bool
- scroll_to_item(item: TreeItem, center_on_item: bool = false)
- set_column_clip_content(column: int, enable: bool)
- set_column_custom_minimum_width(column: int, min_width: int)
- set_column_expand(column: int, expand: bool)
- set_column_expand_ratio(column: int, ratio: int)
- set_column_title(column: int, title: String)
- set_column_title_alignment(column: int, title_alignment: int)
- set_column_title_direction(column: int, direction: int)
- set_column_title_language(column: int, language: String)
- set_column_title_tooltip_text(column: int, tooltip_text: String)
- set_selected(item: TreeItem, column: int)

**Signals:**
- button_clicked(item: TreeItem, column: int, id: int, mouse_button_index: int)
- cell_selected
- check_propagated_to_item(item: TreeItem, column: int)
- column_title_clicked(column: int, mouse_button_index: int)
- custom_item_clicked(mouse_button_index: int)
- custom_popup_edited(arrow_clicked: bool)
- empty_clicked(click_position: Vector2, mouse_button_index: int)
- item_activated
- item_collapsed(item: TreeItem)
- item_edited
- item_icon_double_clicked
- item_mouse_selected(mouse_position: Vector2, mouse_button_index: int)
- item_selected
- multi_selected(item: TreeItem, column: int, selected: bool)
- nothing_selected

**Enums:**
**SelectMode:** SELECT_SINGLE=0, SELECT_ROW=1, SELECT_MULTI=2
**DropModeFlags:** DROP_MODE_DISABLED=0, DROP_MODE_ON_ITEM=1, DROP_MODE_INBETWEEN=2
**ScrollHintMode:** SCROLL_HINT_MODE_DISABLED=0, SCROLL_HINT_MODE_BOTH=1, SCROLL_HINT_MODE_TOP=2, SCROLL_HINT_MODE_BOTTOM=3


## Tween <- RefCounted

Lightweight object used for general-purpose animation via script, using Tweeners.

**Methods:**
- bind_node(node: Node) -> Tween
- chain() -> Tween
- custom_step(delta: float) -> bool
- get_loops_left() -> int
- get_total_elapsed_time() -> float
- interpolate_value(initial_value: Variant, delta_value: Variant, elapsed_time: float, duration: float, trans_type: int, ease_type: int) -> Variant
- is_running() -> bool
- is_valid() -> bool
- kill()
- parallel() -> Tween
- pause()
- play()
- set_ease(ease: int) -> Tween
- set_ignore_time_scale(ignore: bool = true) -> Tween
- set_loops(loops: int = 0) -> Tween
- set_parallel(parallel: bool = true) -> Tween
- set_pause_mode(mode: int) -> Tween
- set_process_mode(mode: int) -> Tween
- set_speed_scale(speed: float) -> Tween
- set_trans(trans: int) -> Tween
- stop()
- tween_callback(callback: Callable) -> CallbackTweener
- tween_interval(time: float) -> IntervalTweener
- tween_method(method: Callable, from: Variant, to: Variant, duration: float) -> MethodTweener
- tween_property(object: Object, property: NodePath, final_val: Variant, duration: float) -> PropertyTweener
- tween_subtween(subtween: Tween) -> SubtweenTweener

**Signals:**
- finished
- loop_finished(loop_count: int)
- step_finished(idx: int)

**Enums:**
**TweenProcessMode:** TWEEN_PROCESS_PHYSICS=0, TWEEN_PROCESS_IDLE=1
**TweenPauseMode:** TWEEN_PAUSE_BOUND=0, TWEEN_PAUSE_STOP=1, TWEEN_PAUSE_PROCESS=2
**TransitionType:** TRANS_LINEAR=0, TRANS_SINE=1, TRANS_QUINT=2, TRANS_QUART=3, TRANS_QUAD=4, TRANS_EXPO=5, TRANS_ELASTIC=6, TRANS_CUBIC=7, TRANS_CIRC=8, TRANS_BOUNCE=9, ...
**EaseType:** EASE_IN=0, EASE_OUT=1, EASE_IN_OUT=2, EASE_OUT_IN=3


## VBoxContainer <- BoxContainer

A container that arranges its child controls vertically.


## VSlider <- Slider

A vertical slider that goes from bottom (min) to top (max).

**Props:**
- size_flags_horizontal: int (Control.SizeFlags) = 0
- size_flags_vertical: int (Control.SizeFlags) = 1


## Vector2

A 2D vector using floating-point coordinates.

**Props:**
- x: float = 0.0
- y: float = 0.0

**Methods:**
- abs() -> Vector2
- angle() -> float
- angle_to(to: Vector2) -> float
- angle_to_point(to: Vector2) -> float
- aspect() -> float
- bezier_derivative(control_1: Vector2, control_2: Vector2, end: Vector2, t: float) -> Vector2
- bezier_interpolate(control_1: Vector2, control_2: Vector2, end: Vector2, t: float) -> Vector2
- bounce(n: Vector2) -> Vector2
- ceil() -> Vector2
- clamp(min: Vector2, max: Vector2) -> Vector2
- clampf(min: float, max: float) -> Vector2
- cross(with: Vector2) -> float
- cubic_interpolate(b: Vector2, pre_a: Vector2, post_b: Vector2, weight: float) -> Vector2
- cubic_interpolate_in_time(b: Vector2, pre_a: Vector2, post_b: Vector2, weight: float, b_t: float, pre_a_t: float, post_b_t: float) -> Vector2
- direction_to(to: Vector2) -> Vector2
- distance_squared_to(to: Vector2) -> float
- distance_to(to: Vector2) -> float
- dot(with: Vector2) -> float
- floor() -> Vector2
- from_angle(angle: float) -> Vector2
- is_equal_approx(to: Vector2) -> bool
- is_finite() -> bool
- is_normalized() -> bool
- is_zero_approx() -> bool
- length() -> float
- length_squared() -> float
- lerp(to: Vector2, weight: float) -> Vector2
- limit_length(length: float = 1.0) -> Vector2
- max(with: Vector2) -> Vector2
- max_axis_index() -> int
- maxf(with: float) -> Vector2
- min(with: Vector2) -> Vector2
- min_axis_index() -> int
- minf(with: float) -> Vector2
- move_toward(to: Vector2, delta: float) -> Vector2
- normalized() -> Vector2
- orthogonal() -> Vector2
- posmod(mod: float) -> Vector2
- posmodv(modv: Vector2) -> Vector2
- project(b: Vector2) -> Vector2
- reflect(line: Vector2) -> Vector2
- rotated(angle: float) -> Vector2
- round() -> Vector2
- sign() -> Vector2
- slerp(to: Vector2, weight: float) -> Vector2
- slide(n: Vector2) -> Vector2
- snapped(step: Vector2) -> Vector2
- snappedf(step: float) -> Vector2

**Enums:**
**Axis:** AXIS_X=0, AXIS_Y=1
**Constants:** ZERO=Vector2(0, 0), ONE=Vector2(1, 1), INF=Vector2(inf, inf), LEFT=Vector2(-1, 0), RIGHT=Vector2(1, 0), UP=Vector2(0, -1), DOWN=Vector2(0, 1)


## Vector3

A 3D vector using floating-point coordinates.

**Props:**
- x: float = 0.0
- y: float = 0.0
- z: float = 0.0

**Methods:**
- abs() -> Vector3
- angle_to(to: Vector3) -> float
- bezier_derivative(control_1: Vector3, control_2: Vector3, end: Vector3, t: float) -> Vector3
- bezier_interpolate(control_1: Vector3, control_2: Vector3, end: Vector3, t: float) -> Vector3
- bounce(n: Vector3) -> Vector3
- ceil() -> Vector3
- clamp(min: Vector3, max: Vector3) -> Vector3
- clampf(min: float, max: float) -> Vector3
- cross(with: Vector3) -> Vector3
- cubic_interpolate(b: Vector3, pre_a: Vector3, post_b: Vector3, weight: float) -> Vector3
- cubic_interpolate_in_time(b: Vector3, pre_a: Vector3, post_b: Vector3, weight: float, b_t: float, pre_a_t: float, post_b_t: float) -> Vector3
- direction_to(to: Vector3) -> Vector3
- distance_squared_to(to: Vector3) -> float
- distance_to(to: Vector3) -> float
- dot(with: Vector3) -> float
- floor() -> Vector3
- inverse() -> Vector3
- is_equal_approx(to: Vector3) -> bool
- is_finite() -> bool
- is_normalized() -> bool
- is_zero_approx() -> bool
- length() -> float
- length_squared() -> float
- lerp(to: Vector3, weight: float) -> Vector3
- limit_length(length: float = 1.0) -> Vector3
- max(with: Vector3) -> Vector3
- max_axis_index() -> int
- maxf(with: float) -> Vector3
- min(with: Vector3) -> Vector3
- min_axis_index() -> int
- minf(with: float) -> Vector3
- move_toward(to: Vector3, delta: float) -> Vector3
- normalized() -> Vector3
- octahedron_decode(uv: Vector2) -> Vector3
- octahedron_encode() -> Vector2
- outer(with: Vector3) -> Basis
- posmod(mod: float) -> Vector3
- posmodv(modv: Vector3) -> Vector3
- project(b: Vector3) -> Vector3
- reflect(n: Vector3) -> Vector3
- rotated(axis: Vector3, angle: float) -> Vector3
- round() -> Vector3
- sign() -> Vector3
- signed_angle_to(to: Vector3, axis: Vector3) -> float
- slerp(to: Vector3, weight: float) -> Vector3
- slide(n: Vector3) -> Vector3
- snapped(step: Vector3) -> Vector3
- snappedf(step: float) -> Vector3

**Enums:**
**Axis:** AXIS_X=0, AXIS_Y=1, AXIS_Z=2
**Constants:** ZERO=Vector3(0, 0, 0), ONE=Vector3(1, 1, 1), INF=Vector3(inf, inf, inf), LEFT=Vector3(-1, 0, 0), RIGHT=Vector3(1, 0, 0), UP=Vector3(0, 1, 0), DOWN=Vector3(0, -1, 0), FORWARD=Vector3(0, 0, -1), BACK=Vector3(0, 0, 1), MODEL_LEFT=Vector3(1, 0, 0), ...


## Vector4

A 4D vector using floating-point coordinates.

**Props:**
- w: float = 0.0
- x: float = 0.0
- y: float = 0.0
- z: float = 0.0

**Methods:**
- abs() -> Vector4
- ceil() -> Vector4
- clamp(min: Vector4, max: Vector4) -> Vector4
- clampf(min: float, max: float) -> Vector4
- cubic_interpolate(b: Vector4, pre_a: Vector4, post_b: Vector4, weight: float) -> Vector4
- cubic_interpolate_in_time(b: Vector4, pre_a: Vector4, post_b: Vector4, weight: float, b_t: float, pre_a_t: float, post_b_t: float) -> Vector4
- direction_to(to: Vector4) -> Vector4
- distance_squared_to(to: Vector4) -> float
- distance_to(to: Vector4) -> float
- dot(with: Vector4) -> float
- floor() -> Vector4
- inverse() -> Vector4
- is_equal_approx(to: Vector4) -> bool
- is_finite() -> bool
- is_normalized() -> bool
- is_zero_approx() -> bool
- length() -> float
- length_squared() -> float
- lerp(to: Vector4, weight: float) -> Vector4
- max(with: Vector4) -> Vector4
- max_axis_index() -> int
- maxf(with: float) -> Vector4
- min(with: Vector4) -> Vector4
- min_axis_index() -> int
- minf(with: float) -> Vector4
- normalized() -> Vector4
- posmod(mod: float) -> Vector4
- posmodv(modv: Vector4) -> Vector4
- round() -> Vector4
- sign() -> Vector4
- snapped(step: Vector4) -> Vector4
- snappedf(step: float) -> Vector4

**Enums:**
**Axis:** AXIS_X=0, AXIS_Y=1, AXIS_Z=2, AXIS_W=3
**Constants:** ZERO=Vector4(0, 0, 0, 0), ONE=Vector4(1, 1, 1, 1), INF=Vector4(inf, inf, inf, inf)

