## AudioServer <- Object

AudioServer is a low-level server interface for audio access. It is in charge of creating sample data (playable audio) as well as its playback via a voice interface.

**Props:**
- bus_count: int = 1
- input_device: String = "Default"
- output_device: String = "Default"
- playback_speed_scale: float = 1.0

- **bus_count**: Number of available audio buses.
- **input_device**: Name of the current device for audio input (see `get_input_device_list`). On systems with multiple audio inputs (such as analog, USB and HDMI audio), this can be used to select the audio input device. The value `"Default"` will record audio on the system-wide default audio input. If an invalid device name is set, the value will be reverted back to `"Default"`. **Note:** `ProjectSettings.audio/driver/enable_input` must be `true` for audio input to work. See also that setting's description for caveats related to permissions and operating system privacy settings.
- **output_device**: Name of the current device for audio output (see `get_output_device_list`). On systems with multiple audio outputs (such as analog, USB and HDMI audio), this can be used to select the audio output device. The value `"Default"` will play audio on the system-wide default audio output. If an invalid device name is set, the value will be reverted back to `"Default"`.
- **playback_speed_scale**: Scales the rate at which audio is played (i.e. setting it to `0.5` will make the audio be played at half its speed). See also `Engine.time_scale` to affect the general simulation speed, which is independent from `AudioServer.playback_speed_scale`.

**Methods:**
- add_bus(at_position: int = -1) - Adds a bus at `at_position`.
- add_bus_effect(bus_idx: int, effect: AudioEffect, at_position: int = -1) - Adds an AudioEffect effect to the bus `bus_idx` at `at_position`.
- generate_bus_layout() -> AudioBusLayout - Generates an AudioBusLayout using the available buses and effects.
- get_bus_channels(bus_idx: int) -> int - Returns the number of channels of the bus at index `bus_idx`.
- get_bus_effect(bus_idx: int, effect_idx: int) -> AudioEffect - Returns the AudioEffect at position `effect_idx` in bus `bus_idx`.
- get_bus_effect_count(bus_idx: int) -> int - Returns the number of effects on the bus at `bus_idx`.
- get_bus_effect_instance(bus_idx: int, effect_idx: int, channel: int = 0) -> AudioEffectInstance - Returns the AudioEffectInstance assigned to the given bus and effect indices (and optionally channel).
- get_bus_index(bus_name: StringName) -> int - Returns the index of the bus with the name `bus_name`. Returns `-1` if no bus with the specified name exist.
- get_bus_name(bus_idx: int) -> String - Returns the name of the bus with the index `bus_idx`.
- get_bus_peak_volume_left_db(bus_idx: int, channel: int) -> float - Returns the peak volume of the left speaker at bus index `bus_idx` and channel index `channel`.
- get_bus_peak_volume_right_db(bus_idx: int, channel: int) -> float - Returns the peak volume of the right speaker at bus index `bus_idx` and channel index `channel`.
- get_bus_send(bus_idx: int) -> StringName - Returns the name of the bus that the bus at index `bus_idx` sends to.
- get_bus_volume_db(bus_idx: int) -> float - Returns the volume of the bus at index `bus_idx` in dB.
- get_bus_volume_linear(bus_idx: int) -> float - Returns the volume of the bus at index `bus_idx` as a linear value. **Note:** The returned value is equivalent to the result of `@GlobalScope.db_to_linear` on the result of `get_bus_volume_db`.
- get_driver_name() -> String - Returns the name of the current audio driver. The default usually depends on the operating system, but may be overridden via the `--audio-driver` . `--headless` also automatically sets the audio driver to `Dummy`. See also `ProjectSettings.audio/driver/driver`.
- get_input_buffer_length_frames() -> int - Returns the absolute size of the microphone input buffer. This is set to a multiple of the audio latency and can be used to estimate the minimum rate at which the frames need to be fetched.
- get_input_device_list() -> PackedStringArray - Returns the names of all audio input devices detected on the system. **Note:** `ProjectSettings.audio/driver/enable_input` must be `true` for audio input to work. See also that setting's description for caveats related to permissions and operating system privacy settings.
- get_input_frames(frames: int) -> PackedVector2Array - Returns a PackedVector2Array containing exactly `frames` audio samples from the internal microphone buffer if available, otherwise returns an empty PackedVector2Array. The buffer is filled at the rate of `get_input_mix_rate` frames per second when `set_input_device_active` has successfully been set to `true`. The samples are signed floating-point PCM values between `-1` and `1`.
- get_input_frames_available() -> int - Returns the number of frames available to read using `get_input_frames`.
- get_input_mix_rate() -> float - Returns the sample rate at the input of the AudioServer.
- get_mix_rate() -> float - Returns the sample rate at the output of the AudioServer.
- get_output_device_list() -> PackedStringArray - Returns the names of all audio output devices detected on the system.
- get_output_latency() -> float - Returns the audio driver's effective output latency. This is based on `ProjectSettings.audio/driver/output_latency`, but the exact returned value will differ depending on the operating system and audio driver. **Note:** This can be expensive; it is not recommended to call `get_output_latency` every frame.
- get_speaker_mode() -> int - Returns the speaker configuration.
- get_time_since_last_mix() -> float - Returns the relative time since the last mix occurred, in seconds.
- get_time_to_next_mix() -> float - Returns the relative time until the next mix occurs, in seconds.
- is_bus_bypassing_effects(bus_idx: int) -> bool - If `true`, the bus at index `bus_idx` is bypassing effects.
- is_bus_effect_enabled(bus_idx: int, effect_idx: int) -> bool - If `true`, the effect at index `effect_idx` on the bus at index `bus_idx` is enabled.
- is_bus_mute(bus_idx: int) -> bool - If `true`, the bus at index `bus_idx` is muted.
- is_bus_solo(bus_idx: int) -> bool - If `true`, the bus at index `bus_idx` is in solo mode.
- is_stream_registered_as_sample(stream: AudioStream) -> bool - If `true`, the stream is registered as a sample. The engine will not have to register it before playing the sample. If `false`, the stream will have to be registered before playing it. To prevent lag spikes, register the stream as sample with `register_stream_as_sample`.
- lock() - Locks the audio driver's main loop. **Note:** Remember to unlock it afterwards.
- move_bus(index: int, to_index: int) - Moves the bus from index `index` to index `to_index`.
- register_stream_as_sample(stream: AudioStream) - Forces the registration of a stream as a sample. **Note:** Lag spikes may occur when calling this method, especially on single-threaded builds. It is suggested to call this method while loading assets, where the lag spike could be masked, instead of registering the sample right before it needs to be played.
- remove_bus(index: int) - Removes the bus at index `index`.
- remove_bus_effect(bus_idx: int, effect_idx: int) - Removes the effect at index `effect_idx` from the bus at index `bus_idx`.
- set_bus_bypass_effects(bus_idx: int, enable: bool) - If `true`, the bus at index `bus_idx` is bypassing effects.
- set_bus_effect_enabled(bus_idx: int, effect_idx: int, enabled: bool) - If `true`, the effect at index `effect_idx` on the bus at index `bus_idx` is enabled.
- set_bus_layout(bus_layout: AudioBusLayout) - Overwrites the currently used AudioBusLayout.
- set_bus_mute(bus_idx: int, enable: bool) - If `true`, the bus at index `bus_idx` is muted.
- set_bus_name(bus_idx: int, name: String) - Sets the name of the bus at index `bus_idx` to `name`.
- set_bus_send(bus_idx: int, send: StringName) - Connects the output of the bus at `bus_idx` to the bus named `send`.
- set_bus_solo(bus_idx: int, enable: bool) - If `true`, the bus at index `bus_idx` is in solo mode.
- set_bus_volume_db(bus_idx: int, volume_db: float) - Sets the volume in decibels of the bus at index `bus_idx` to `volume_db`.
- set_bus_volume_linear(bus_idx: int, volume_linear: float) - Sets the volume as a linear value of the bus at index `bus_idx` to `volume_linear`. **Note:** Using this method is equivalent to calling `set_bus_volume_db` with the result of `@GlobalScope.linear_to_db` on a value.
- set_enable_tagging_used_audio_streams(enable: bool) - If set to `true`, all instances of AudioStreamPlayback will call `AudioStreamPlayback._tag_used_streams` every mix step. **Note:** This is enabled by default in the editor, as it is used by editor plugins for the audio stream previews.
- set_input_device_active(active: bool) -> int - If `active` is `true`, starts the microphone input stream specified by `input_device` or returns an error if it failed. If `active` is `false`, stops the input stream if it is running.
- swap_bus_effects(bus_idx: int, effect_idx: int, by_effect_idx: int) - Swaps the position of two effects in bus `bus_idx`.
- unlock() - Unlocks the audio driver's main loop. (After locking it, you should always unlock it.)

**Signals:**
- bus_layout_changed - Emitted when an audio bus is added, deleted, or moved.
- bus_renamed(bus_index: int, old_name: StringName, new_name: StringName) - Emitted when the audio bus at `bus_index` is renamed from `old_name` to `new_name`.

**Enums:**
**SpeakerMode:** SPEAKER_MODE_STEREO=0, SPEAKER_SURROUND_31=1, SPEAKER_SURROUND_51=2, SPEAKER_SURROUND_71=3
  - SPEAKER_MODE_STEREO: Two or fewer speakers were detected.
  - SPEAKER_SURROUND_31: A 3.1 channel surround setup was detected.
  - SPEAKER_SURROUND_51: A 5.1 channel surround setup was detected.
  - SPEAKER_SURROUND_71: A 7.1 channel surround setup was detected.
**PlaybackType:** PLAYBACK_TYPE_DEFAULT=0, PLAYBACK_TYPE_STREAM=1, PLAYBACK_TYPE_SAMPLE=2, PLAYBACK_TYPE_MAX=3
  - PLAYBACK_TYPE_DEFAULT: The playback will be considered of the type declared at `ProjectSettings.audio/general/default_playback_type`.
  - PLAYBACK_TYPE_STREAM: Force the playback to be considered as a stream.
  - PLAYBACK_TYPE_SAMPLE: Force the playback to be considered as a sample. This can provide lower latency and more stable playback (with less risk of audio crackling), at the cost of having less flexibility. **Note:** Only currently supported on the web platform. **Note:** AudioEffects are not supported when playback is considered as a sample.
  - PLAYBACK_TYPE_MAX: Represents the size of the `PlaybackType` enum.

