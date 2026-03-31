## AudioStream <- Resource

Base class for audio streams. Audio streams are used for sound effects and music playback, and support WAV (via AudioStreamWAV), Ogg (via AudioStreamOggVorbis), and MP3 (via AudioStreamMP3) file formats.

**Methods:**
- _get_bar_beats() -> int - Override this method to return the bar beats of this stream.
- _get_beat_count() -> int - Overridable method. Should return the total number of beats of this audio stream. Used by the engine to determine the position of every beat. Ideally, the returned value should be based off the stream's sample rate (`AudioStreamWAV.mix_rate`, for example).
- _get_bpm() -> float - Overridable method. Should return the tempo of this audio stream, in beats per minute (BPM). Used by the engine to determine the position of every beat. Ideally, the returned value should be based off the stream's sample rate (`AudioStreamWAV.mix_rate`, for example).
- _get_length() -> float - Override this method to customize the returned value of `get_length`. Should return the length of this audio stream, in seconds.
- _get_parameter_list() -> Dictionary[] - Return the controllable parameters of this stream. This array contains dictionaries with a property info description format (see `Object.get_property_list`). Additionally, the default value for this parameter must be added tho each dictionary in "default_value" field.
- _get_stream_name() -> String - Override this method to customize the name assigned to this audio stream. Unused by the engine.
- _get_tags() -> Dictionary - Override this method to customize the tags for this audio stream. Should return a Dictionary of strings with the tag as the key and its content as the value. Commonly used tags include `title`, `artist`, `album`, `tracknumber`, and `date`.
- _has_loop() -> bool - Override this method to return `true` if this stream has a loop.
- _instantiate_playback() -> AudioStreamPlayback - Override this method to customize the returned value of `instantiate_playback`. Should return a new AudioStreamPlayback created when the stream is played (such as by an AudioStreamPlayer).
- _is_monophonic() -> bool - Override this method to customize the returned value of `is_monophonic`. Should return `true` if this audio stream only supports one channel.
- can_be_sampled() -> bool - Returns if the current AudioStream can be used as a sample. Only static streams can be sampled.
- generate_sample() -> AudioSample - Generates an AudioSample based on the current stream.
- get_length() -> float - Returns the length of the audio stream in seconds. If this stream is an AudioStreamRandomizer, returns the length of the last played stream. If this stream has an indefinite length (such as for AudioStreamGenerator and AudioStreamMicrophone), returns `0.0`.
- instantiate_playback() -> AudioStreamPlayback - Returns a newly created AudioStreamPlayback intended to play this audio stream. Useful for when you want to extend `_instantiate_playback` but call `instantiate_playback` from an internally held AudioStream subresource. An example of this can be found in the source code for `AudioStreamRandomPitch::instantiate_playback`.
- is_meta_stream() -> bool - Returns `true` if the stream is a collection of other streams, `false` otherwise.
- is_monophonic() -> bool - Returns `true` if this audio stream only supports one channel (*monophony*), or `false` if the audio stream supports two or more channels (*polyphony*).

**Signals:**
- parameter_list_changed - Signal to be emitted to notify when the parameter list changed.

