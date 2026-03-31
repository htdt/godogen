## SpriteFrames <- Resource

Sprite frame library for an AnimatedSprite2D or AnimatedSprite3D node. Contains frames and animation data for playback.

**Methods:**
- add_animation(anim: StringName) - Adds a new `anim` animation to the library.
- add_frame(anim: StringName, texture: Texture2D, duration: float = 1.0, at_position: int = -1) - Adds a frame to the `anim` animation. If `at_position` is `-1`, the frame will be added to the end of the animation. `duration` specifies the relative duration, see `get_frame_duration` for details.
- clear(anim: StringName) - Removes all frames from the `anim` animation.
- clear_all() - Removes all animations. An empty `default` animation will be created.
- duplicate_animation(anim_from: StringName, anim_to: StringName) - Duplicates the animation `anim_from` to a new animation named `anim_to`. Fails if `anim_to` already exists, or if `anim_from` does not exist.
- get_animation_loop(anim: StringName) -> bool - Returns `true` if the given animation is configured to loop when it finishes playing. Otherwise, returns `false`.
- get_animation_names() -> PackedStringArray - Returns an array containing the names associated to each animation. Values are placed in alphabetical order.
- get_animation_speed(anim: StringName) -> float - Returns the speed in frames per second for the `anim` animation.
- get_frame_count(anim: StringName) -> int - Returns the number of frames for the `anim` animation.
- get_frame_duration(anim: StringName, idx: int) -> float - Returns a relative duration of the frame `idx` in the `anim` animation (defaults to `1.0`). For example, a frame with a duration of `2.0` is displayed twice as long as a frame with a duration of `1.0`. You can calculate the absolute duration (in seconds) of a frame using the following formula: In this example, `playing_speed` refers to either `AnimatedSprite2D.get_playing_speed` or `AnimatedSprite3D.get_playing_speed`.
- get_frame_texture(anim: StringName, idx: int) -> Texture2D - Returns the texture of the frame `idx` in the `anim` animation.
- has_animation(anim: StringName) -> bool - Returns `true` if the `anim` animation exists.
- remove_animation(anim: StringName) - Removes the `anim` animation.
- remove_frame(anim: StringName, idx: int) - Removes the `anim` animation's frame `idx`.
- rename_animation(anim: StringName, newname: StringName) - Changes the `anim` animation's name to `newname`.
- set_animation_loop(anim: StringName, loop: bool) - If `loop` is `true`, the `anim` animation will loop when it reaches the end, or the start if it is played in reverse.
- set_animation_speed(anim: StringName, fps: float) - Sets the speed for the `anim` animation in frames per second.
- set_frame(anim: StringName, idx: int, texture: Texture2D, duration: float = 1.0) - Sets the `texture` and the `duration` of the frame `idx` in the `anim` animation. `duration` specifies the relative duration, see `get_frame_duration` for details.

