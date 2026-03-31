## AudioStreamPlayback <- RefCounted

Can play, loop, pause a scroll through audio. See AudioStream and AudioStreamOggVorbis for usage.

**Methods:**
- _get_loop_count() -> int - Overridable method. Should return how many times this audio stream has looped. Most built-in playbacks always return `0`.
- _get_parameter(name: StringName) -> Variant - Return the current value of a playback parameter by name (see `AudioStream._get_parameter_list`).
- _get_playback_position() -> float - Overridable method. Should return the current progress along the audio stream, in seconds.
- _is_playing() -> bool - Overridable method. Should return `true` if this playback is active and playing its audio stream.
- _mix(buffer: AudioFrame*, rate_scale: float, frames: int) -> int - Override this method to customize how the audio stream is mixed. This method is called even if the playback is not active. **Note:** It is not useful to override this method in GDScript or C#. Only GDExtension can take advantage of it.
- _seek(position: float) - Override this method to customize what happens when seeking this audio stream at the given `position`, such as by calling `AudioStreamPlayer.seek`.
- _set_parameter(name: StringName, value: Variant) - Set the current value of a playback parameter by name (see `AudioStream._get_parameter_list`).
- _start(from_pos: float) - Override this method to customize what happens when the playback starts at the given position, such as by calling `AudioStreamPlayer.play`.
- _stop() - Override this method to customize what happens when the playback is stopped, such as by calling `AudioStreamPlayer.stop`.
- _tag_used_streams() - Overridable method. Called whenever the audio stream is mixed if the playback is active and `AudioServer.set_enable_tagging_used_audio_streams` has been set to `true`. Editor plugins may use this method to "tag" the current position along the audio stream and display it in a preview.
- get_loop_count() -> int - Returns the number of times the stream has looped.
- get_playback_position() -> float - Returns the current position in the stream, in seconds.
- get_sample_playback() -> AudioSamplePlayback - Returns the AudioSamplePlayback associated with this AudioStreamPlayback for playing back the audio sample of this stream.
- is_playing() -> bool - Returns `true` if the stream is playing.
- mix_audio(rate_scale: float, frames: int) -> PackedVector2Array - Mixes up to `frames` of audio from the stream from the current position, at a rate of `rate_scale`, advancing the stream. Returns a PackedVector2Array where each element holds the left and right channel volume levels of each frame. **Note:** Can return fewer frames than requested, make sure to use the size of the return value.
- seek(time: float = 0.0) - Seeks the stream at the given `time`, in seconds.
- set_sample_playback(playback_sample: AudioSamplePlayback) - Associates AudioSamplePlayback to this AudioStreamPlayback for playing back the audio sample of this stream.
- start(from_pos: float = 0.0) - Starts the stream from the given `from_pos`, in seconds.
- stop() - Stops the stream.

