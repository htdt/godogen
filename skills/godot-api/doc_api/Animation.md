## Animation <- Resource

This resource holds data that can be used to animate anything in the engine. Animations are divided into tracks and each track must be linked to a node. The state of that node can be changed through time, by adding timed keys (events) to the track. Animations are just data containers, and must be added to nodes such as an AnimationPlayer to be played back. Animation tracks have different types, each with its own set of dedicated methods. Check `TrackType` to see available types. **Note:** For 3D position/rotation/scale, using the dedicated `TYPE_POSITION_3D`, `TYPE_ROTATION_3D` and `TYPE_SCALE_3D` track types instead of `TYPE_VALUE` is recommended for performance reasons.

**Props:**
- capture_included: bool = false
- length: float = 1.0
- loop_mode: int (Animation.LoopMode) = 0
- step: float = 0.033333335

- **capture_included**: Returns `true` if the capture track is included. This is a cached readonly value for performance.
- **length**: The total length of the animation (in seconds). **Note:** Length is not delimited by the last key, as this one may be before or after the end to ensure correct interpolation and looping.
- **loop_mode**: Determines the behavior of both ends of the animation timeline during animation playback. This indicates whether and how the animation should be restarted, and is also used to correctly interpolate animation cycles.
- **step**: The animation step value.

**Methods:**
- add_marker(name: StringName, time: float) - Adds a marker to this Animation.
- add_track(type: int, at_position: int = -1) -> int - Adds a track to the Animation.
- animation_track_get_key_animation(track_idx: int, key_idx: int) -> StringName - Returns the animation name at the key identified by `key_idx`. The `track_idx` must be the index of an Animation Track.
- animation_track_insert_key(track_idx: int, time: float, animation: StringName) -> int - Inserts a key with value `animation` at the given `time` (in seconds). The `track_idx` must be the index of an Animation Track.
- animation_track_set_key_animation(track_idx: int, key_idx: int, animation: StringName) - Sets the key identified by `key_idx` to value `animation`. The `track_idx` must be the index of an Animation Track.
- audio_track_get_key_end_offset(track_idx: int, key_idx: int) -> float - Returns the end offset of the key identified by `key_idx`. The `track_idx` must be the index of an Audio Track. End offset is the number of seconds cut off at the ending of the audio stream.
- audio_track_get_key_start_offset(track_idx: int, key_idx: int) -> float - Returns the start offset of the key identified by `key_idx`. The `track_idx` must be the index of an Audio Track. Start offset is the number of seconds cut off at the beginning of the audio stream.
- audio_track_get_key_stream(track_idx: int, key_idx: int) -> Resource - Returns the audio stream of the key identified by `key_idx`. The `track_idx` must be the index of an Audio Track.
- audio_track_insert_key(track_idx: int, time: float, stream: Resource, start_offset: float = 0, end_offset: float = 0) -> int - Inserts an Audio Track key at the given `time` in seconds. The `track_idx` must be the index of an Audio Track. `stream` is the AudioStream resource to play. `start_offset` is the number of seconds cut off at the beginning of the audio stream, while `end_offset` is at the ending.
- audio_track_is_use_blend(track_idx: int) -> bool - Returns `true` if the track at `track_idx` will be blended with other animations.
- audio_track_set_key_end_offset(track_idx: int, key_idx: int, offset: float) - Sets the end offset of the key identified by `key_idx` to value `offset`. The `track_idx` must be the index of an Audio Track.
- audio_track_set_key_start_offset(track_idx: int, key_idx: int, offset: float) - Sets the start offset of the key identified by `key_idx` to value `offset`. The `track_idx` must be the index of an Audio Track.
- audio_track_set_key_stream(track_idx: int, key_idx: int, stream: Resource) - Sets the stream of the key identified by `key_idx` to value `stream`. The `track_idx` must be the index of an Audio Track.
- audio_track_set_use_blend(track_idx: int, enable: bool) - Sets whether the track will be blended with other animations. If `true`, the audio playback volume changes depending on the blend value.
- bezier_track_get_key_in_handle(track_idx: int, key_idx: int) -> Vector2 - Returns the in handle of the key identified by `key_idx`. The `track_idx` must be the index of a Bezier Track.
- bezier_track_get_key_out_handle(track_idx: int, key_idx: int) -> Vector2 - Returns the out handle of the key identified by `key_idx`. The `track_idx` must be the index of a Bezier Track.
- bezier_track_get_key_value(track_idx: int, key_idx: int) -> float - Returns the value of the key identified by `key_idx`. The `track_idx` must be the index of a Bezier Track.
- bezier_track_insert_key(track_idx: int, time: float, value: float, in_handle: Vector2 = Vector2(0, 0), out_handle: Vector2 = Vector2(0, 0)) -> int - Inserts a Bezier Track key at the given `time` in seconds. The `track_idx` must be the index of a Bezier Track. `in_handle` is the left-side weight of the added Bezier curve point, `out_handle` is the right-side one, while `value` is the actual value at this point.
- bezier_track_interpolate(track_idx: int, time: float) -> float - Returns the interpolated value at the given `time` (in seconds). The `track_idx` must be the index of a Bezier Track.
- bezier_track_set_key_in_handle(track_idx: int, key_idx: int, in_handle: Vector2, balanced_value_time_ratio: float = 1.0) - Sets the in handle of the key identified by `key_idx` to value `in_handle`. The `track_idx` must be the index of a Bezier Track.
- bezier_track_set_key_out_handle(track_idx: int, key_idx: int, out_handle: Vector2, balanced_value_time_ratio: float = 1.0) - Sets the out handle of the key identified by `key_idx` to value `out_handle`. The `track_idx` must be the index of a Bezier Track.
- bezier_track_set_key_value(track_idx: int, key_idx: int, value: float) - Sets the value of the key identified by `key_idx` to the given value. The `track_idx` must be the index of a Bezier Track.
- blend_shape_track_insert_key(track_idx: int, time: float, amount: float) -> int - Inserts a key in a given blend shape track. Returns the key index.
- blend_shape_track_interpolate(track_idx: int, time_sec: float, backward: bool = false) -> float - Returns the interpolated blend shape value at the given time (in seconds). The `track_idx` must be the index of a blend shape track.
- clear() - Clear the animation (clear all tracks and reset all).
- compress(page_size: int = 8192, fps: int = 120, split_tolerance: float = 4.0) - Compress the animation and all its tracks in-place. This will make `track_is_compressed` return `true` once called on this Animation. Compressed tracks require less memory to be played, and are designed to be used for complex 3D animations (such as cutscenes) imported from external 3D software. Compression is lossy, but the difference is usually not noticeable in real world conditions. **Note:** Compressed tracks have various limitations (such as not being editable from the editor), so only use compressed animations if you actually need them.
- copy_track(track_idx: int, to_animation: Animation) - Adds a new track to `to_animation` that is a copy of the given track from this animation.
- find_track(path: NodePath, type: int) -> int - Returns the index of the specified track. If the track is not found, return -1.
- get_marker_at_time(time: float) -> StringName - Returns the name of the marker located at the given time.
- get_marker_color(name: StringName) -> Color - Returns the given marker's color.
- get_marker_names() -> PackedStringArray - Returns every marker in this Animation, sorted ascending by time.
- get_marker_time(name: StringName) -> float - Returns the given marker's time.
- get_next_marker(time: float) -> StringName - Returns the closest marker that comes after the given time. If no such marker exists, an empty string is returned.
- get_prev_marker(time: float) -> StringName - Returns the closest marker that comes before the given time. If no such marker exists, an empty string is returned.
- get_track_count() -> int - Returns the amount of tracks in the animation.
- has_marker(name: StringName) -> bool - Returns `true` if this Animation contains a marker with the given name.
- method_track_get_name(track_idx: int, key_idx: int) -> StringName - Returns the method name of a method track.
- method_track_get_params(track_idx: int, key_idx: int) -> Array - Returns the arguments values to be called on a method track for a given key in a given track.
- optimize(allowed_velocity_err: float = 0.01, allowed_angular_err: float = 0.01, precision: int = 3) - Optimize the animation and all its tracks in-place. This will preserve only as many keys as are necessary to keep the animation within the specified bounds.
- position_track_insert_key(track_idx: int, time: float, position: Vector3) -> int - Inserts a key in a given 3D position track. Returns the key index.
- position_track_interpolate(track_idx: int, time_sec: float, backward: bool = false) -> Vector3 - Returns the interpolated position value at the given time (in seconds). The `track_idx` must be the index of a 3D position track.
- remove_marker(name: StringName) - Removes the marker with the given name from this Animation.
- remove_track(track_idx: int) - Removes a track by specifying the track index.
- rotation_track_insert_key(track_idx: int, time: float, rotation: Quaternion) -> int - Inserts a key in a given 3D rotation track. Returns the key index.
- rotation_track_interpolate(track_idx: int, time_sec: float, backward: bool = false) -> Quaternion - Returns the interpolated rotation value at the given time (in seconds). The `track_idx` must be the index of a 3D rotation track.
- scale_track_insert_key(track_idx: int, time: float, scale: Vector3) -> int - Inserts a key in a given 3D scale track. Returns the key index.
- scale_track_interpolate(track_idx: int, time_sec: float, backward: bool = false) -> Vector3 - Returns the interpolated scale value at the given time (in seconds). The `track_idx` must be the index of a 3D scale track.
- set_marker_color(name: StringName, color: Color) - Sets the given marker's color.
- track_find_key(track_idx: int, time: float, find_mode: int = 0, limit: bool = false, backward: bool = false) -> int - Finds the key index by time in a given track. Optionally, only find it if the approx/exact time is given. If `limit` is `true`, it does not return keys outside the animation range. If `backward` is `true`, the direction is reversed in methods that rely on one directional processing. For example, in case `find_mode` is `FIND_MODE_NEAREST`, if there is no key in the current position just after seeked, the first key found is retrieved by searching before the position, but if `backward` is `true`, the first key found is retrieved after the position.
- track_get_interpolation_loop_wrap(track_idx: int) -> bool - Returns `true` if the track at `track_idx` wraps the interpolation loop. New tracks wrap the interpolation loop by default.
- track_get_interpolation_type(track_idx: int) -> int - Returns the interpolation type of a given track.
- track_get_key_count(track_idx: int) -> int - Returns the number of keys in a given track.
- track_get_key_time(track_idx: int, key_idx: int) -> float - Returns the time at which the key is located.
- track_get_key_transition(track_idx: int, key_idx: int) -> float - Returns the transition curve (easing) for a specific key (see the built-in math function `@GlobalScope.ease`).
- track_get_key_value(track_idx: int, key_idx: int) -> Variant - Returns the value of a given key in a given track.
- track_get_path(track_idx: int) -> NodePath - Gets the path of a track. For more information on the path format, see `track_set_path`.
- track_get_type(track_idx: int) -> int - Gets the type of a track.
- track_insert_key(track_idx: int, time: float, key: Variant, transition: float = 1) -> int - Inserts a generic key in a given track. Returns the key index.
- track_is_compressed(track_idx: int) -> bool - Returns `true` if the track is compressed, `false` otherwise. See also `compress`.
- track_is_enabled(track_idx: int) -> bool - Returns `true` if the track at index `track_idx` is enabled.
- track_is_imported(track_idx: int) -> bool - Returns `true` if the given track is imported. Else, return `false`.
- track_move_down(track_idx: int) - Moves a track down.
- track_move_to(track_idx: int, to_idx: int) - Changes the index position of track `track_idx` to the one defined in `to_idx`.
- track_move_up(track_idx: int) - Moves a track up.
- track_remove_key(track_idx: int, key_idx: int) - Removes a key by index in a given track.
- track_remove_key_at_time(track_idx: int, time: float) - Removes a key at `time` in a given track.
- track_set_enabled(track_idx: int, enabled: bool) - Enables/disables the given track. Tracks are enabled by default.
- track_set_imported(track_idx: int, imported: bool) - Sets the given track as imported or not.
- track_set_interpolation_loop_wrap(track_idx: int, interpolation: bool) - If `true`, the track at `track_idx` wraps the interpolation loop.
- track_set_interpolation_type(track_idx: int, interpolation: int) - Sets the interpolation type of a given track.
- track_set_key_time(track_idx: int, key_idx: int, time: float) - Sets the time of an existing key.
- track_set_key_transition(track_idx: int, key_idx: int, transition: float) - Sets the transition curve (easing) for a specific key (see the built-in math function `@GlobalScope.ease`).
- track_set_key_value(track_idx: int, key: int, value: Variant) - Sets the value of an existing key.
- track_set_path(track_idx: int, path: NodePath) - Sets the path of a track. Paths must be valid scene-tree paths to a node and must be specified starting from the `AnimationMixer.root_node` that will reproduce the animation. Tracks that control properties or bones must append their name after the path, separated by `":"`. For example, `"character/skeleton:ankle"` or `"character/mesh:transform/local"`.
- track_swap(track_idx: int, with_idx: int) - Swaps the track `track_idx`'s index position with the track `with_idx`.
- value_track_get_update_mode(track_idx: int) -> int - Returns the update mode of a value track.
- value_track_interpolate(track_idx: int, time_sec: float, backward: bool = false) -> Variant - Returns the interpolated value at the given time (in seconds). The `track_idx` must be the index of a value track. A `backward` mainly affects the direction of key retrieval of the track with `UPDATE_DISCRETE` converted by `AnimationMixer.ANIMATION_CALLBACK_MODE_DISCRETE_FORCE_CONTINUOUS` to match the result with `track_find_key`.
- value_track_set_update_mode(track_idx: int, mode: int) - Sets the update mode of a value track.

**Enums:**
**TrackType:** TYPE_VALUE=0, TYPE_POSITION_3D=1, TYPE_ROTATION_3D=2, TYPE_SCALE_3D=3, TYPE_BLEND_SHAPE=4, TYPE_METHOD=5, TYPE_BEZIER=6, TYPE_AUDIO=7, TYPE_ANIMATION=8
  - TYPE_VALUE: Value tracks set values in node properties, but only those which can be interpolated. For 3D position/rotation/scale, using the dedicated `TYPE_POSITION_3D`, `TYPE_ROTATION_3D` and `TYPE_SCALE_3D` track types instead of `TYPE_VALUE` is recommended for performance reasons.
  - TYPE_POSITION_3D: 3D position track (values are stored in Vector3s).
  - TYPE_ROTATION_3D: 3D rotation track (values are stored in Quaternions).
  - TYPE_SCALE_3D: 3D scale track (values are stored in Vector3s).
  - TYPE_BLEND_SHAPE: Blend shape track.
  - TYPE_METHOD: Method tracks call functions with given arguments per key.
  - TYPE_BEZIER: Bezier tracks are used to interpolate a value using custom curves. They can also be used to animate sub-properties of vectors and colors (e.g. alpha value of a Color).
  - TYPE_AUDIO: Audio tracks are used to play an audio stream with either type of AudioStreamPlayer. The stream can be trimmed and previewed in the animation.
  - TYPE_ANIMATION: Animation tracks play animations in other AnimationPlayer nodes.
**InterpolationType:** INTERPOLATION_NEAREST=0, INTERPOLATION_LINEAR=1, INTERPOLATION_CUBIC=2, INTERPOLATION_LINEAR_ANGLE=3, INTERPOLATION_CUBIC_ANGLE=4
  - INTERPOLATION_NEAREST: No interpolation (nearest value).
  - INTERPOLATION_LINEAR: Linear interpolation.
  - INTERPOLATION_CUBIC: Cubic interpolation. This looks smoother than linear interpolation, but is more expensive to interpolate. Stick to `INTERPOLATION_LINEAR` for complex 3D animations imported from external software, even if it requires using a higher animation framerate in return.
  - INTERPOLATION_LINEAR_ANGLE: Linear interpolation with shortest path rotation. **Note:** The result value is always normalized and may not match the key value.
  - INTERPOLATION_CUBIC_ANGLE: Cubic interpolation with shortest path rotation. **Note:** The result value is always normalized and may not match the key value.
**UpdateMode:** UPDATE_CONTINUOUS=0, UPDATE_DISCRETE=1, UPDATE_CAPTURE=2
  - UPDATE_CONTINUOUS: Update between keyframes and hold the value.
  - UPDATE_DISCRETE: Update at the keyframes.
  - UPDATE_CAPTURE: Same as `UPDATE_CONTINUOUS` but works as a flag to capture the value of the current object and perform interpolation in some methods. See also `AnimationMixer.capture`, `AnimationPlayer.playback_auto_capture`, and `AnimationPlayer.play_with_capture`.
**LoopMode:** LOOP_NONE=0, LOOP_LINEAR=1, LOOP_PINGPONG=2
  - LOOP_NONE: At both ends of the animation, the animation will stop playing.
  - LOOP_LINEAR: At both ends of the animation, the animation will be repeated without changing the playback direction.
  - LOOP_PINGPONG: Repeats playback and reverse playback at both ends of the animation.
**LoopedFlag:** LOOPED_FLAG_NONE=0, LOOPED_FLAG_END=1, LOOPED_FLAG_START=2
  - LOOPED_FLAG_NONE: This flag indicates that the animation proceeds without any looping.
  - LOOPED_FLAG_END: This flag indicates that the animation has reached the end of the animation and just after loop processed.
  - LOOPED_FLAG_START: This flag indicates that the animation has reached the start of the animation and just after loop processed.
**FindMode:** FIND_MODE_NEAREST=0, FIND_MODE_APPROX=1, FIND_MODE_EXACT=2
  - FIND_MODE_NEAREST: Finds the nearest time key.
  - FIND_MODE_APPROX: Finds only the key with approximating the time.
  - FIND_MODE_EXACT: Finds only the key with matching the time.

