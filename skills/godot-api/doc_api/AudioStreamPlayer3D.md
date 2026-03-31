## AudioStreamPlayer3D <- Node3D

Plays audio with positional sound effects, based on the relative position of the audio listener. Positional effects include distance attenuation, directionality, and the Doppler effect. For greater realism, a low-pass filter is applied to distant sounds. This can be disabled by setting `attenuation_filter_cutoff_hz` to `20500`. By default, audio is heard from the camera position. This can be changed by adding an AudioListener3D node to the scene and enabling it by calling `AudioListener3D.make_current` on it. See also AudioStreamPlayer to play a sound non-positionally. **Note:** Hiding an AudioStreamPlayer3D node does not disable its audio output. To temporarily disable an AudioStreamPlayer3D's audio output, set `volume_db` to a very low value like `-100` (which isn't audible to human hearing).

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

- **area_mask**: Determines which Area3D layers affect the sound for reverb and audio bus effects. Areas can be used to redirect AudioStreams so that they play in a certain audio bus. An example of how you might use this is making a "water" area so that sounds played in the water are redirected through an audio bus to make them sound like they are being played underwater.
- **attenuation_filter_cutoff_hz**: The cutoff frequency of the attenuation low-pass filter, in Hz. A sound above this frequency is attenuated more than a sound below this frequency. To disable this effect, set this to `20500` as this frequency is above the human hearing limit.
- **attenuation_filter_db**: Amount how much the filter affects the loudness, in decibels.
- **attenuation_model**: Decides if audio should get quieter with distance linearly, quadratically, logarithmically, or not be affected by distance, effectively disabling attenuation.
- **autoplay**: If `true`, audio plays when the AudioStreamPlayer3D node is added to scene tree.
- **bus**: The bus on which this audio is playing. **Note:** When setting this property, keep in mind that no validation is performed to see if the given name matches an existing bus. This is because audio bus layouts might be loaded after this property is set. If this given name can't be resolved at runtime, it will fall back to `"Master"`.
- **doppler_tracking**: Decides in which step the Doppler effect should be calculated. **Note:** If `doppler_tracking` is not `DOPPLER_TRACKING_DISABLED` but the current Camera3D/AudioListener3D has doppler tracking disabled, the Doppler effect will be heard but will not take the movement of the current listener into account. If accurate Doppler effect is desired, doppler tracking should be enabled on both the AudioStreamPlayer3D and the current Camera3D/AudioListener3D.
- **emission_angle_degrees**: The angle in which the audio reaches a listener unattenuated.
- **emission_angle_enabled**: If `true`, the audio should be attenuated according to the direction of the sound.
- **emission_angle_filter_attenuation_db**: Attenuation factor used if listener is outside of `emission_angle_degrees` and `emission_angle_enabled` is set, in decibels.
- **max_db**: Sets the absolute maximum of the sound level, in decibels.
- **max_distance**: The distance past which the sound can no longer be heard at all. Only has an effect if set to a value greater than `0.0`. `max_distance` works in tandem with `unit_size`. However, unlike `unit_size` whose behavior depends on the `attenuation_model`, `max_distance` always works in a linear fashion. This can be used to prevent the AudioStreamPlayer3D from requiring audio mixing when the listener is far away, which saves CPU resources.
- **max_polyphony**: The maximum number of sounds this node can play at the same time. Playing additional sounds after this value is reached will cut off the oldest sounds.
- **panning_strength**: Scales the panning strength for this node by multiplying the base `ProjectSettings.audio/general/3d_panning_strength` by this factor. If the product is `0.0` then stereo panning is disabled and the volume is the same for all channels. If the product is `1.0` then one of the channels will be muted when the sound is located exactly to the left (or right) of the listener. Two speaker stereo arrangements implement the where the volume is cosine of half the azimuth angle to the ear. For other speaker arrangements such as the 5.1 and 7.1 the SPCAP (Speaker-Placement Correction Amplitude) algorithm is implemented.
- **pitch_scale**: The pitch and the tempo of the audio, as a multiplier of the audio sample's sample rate.
- **playback_type**: The playback type of the stream player. If set other than to the default value, it will force that playback type.
- **playing**: If `true`, audio is playing or is queued to be played (see `play`).
- **stream**: The AudioStream resource to be played.
- **stream_paused**: If `true`, the playback is paused. You can resume it by setting `stream_paused` to `false`.
- **unit_size**: The factor for the attenuation effect. Higher values make the sound audible over a larger distance.
- **volume_db**: The base sound level before attenuation, in decibels.
- **volume_linear**: The base sound level before attenuation, as a linear value. **Note:** This member modifies `volume_db` for convenience. The returned value is equivalent to the result of `@GlobalScope.db_to_linear` on `volume_db`. Setting this member is equivalent to setting `volume_db` to the result of `@GlobalScope.linear_to_db` on a value.

**Methods:**
- get_playback_position() -> float - Returns the position in the AudioStream.
- get_stream_playback() -> AudioStreamPlayback - Returns the AudioStreamPlayback object associated with this AudioStreamPlayer3D.
- has_stream_playback() -> bool - Returns whether the AudioStreamPlayer can return the AudioStreamPlayback object or not.
- play(from_position: float = 0.0) - Queues the audio to play on the next physics frame, from the given position `from_position`, in seconds.
- seek(to_position: float) - Sets the position from which audio will be played, in seconds.
- stop() - Stops the audio.

**Signals:**
- finished - Emitted when the audio stops playing.

**Enums:**
**AttenuationModel:** ATTENUATION_INVERSE_DISTANCE=0, ATTENUATION_INVERSE_SQUARE_DISTANCE=1, ATTENUATION_LOGARITHMIC=2, ATTENUATION_DISABLED=3
  - ATTENUATION_INVERSE_DISTANCE: Attenuation of loudness according to linear distance.
  - ATTENUATION_INVERSE_SQUARE_DISTANCE: Attenuation of loudness according to squared distance.
  - ATTENUATION_LOGARITHMIC: Attenuation of loudness according to logarithmic distance.
  - ATTENUATION_DISABLED: No attenuation of loudness according to distance. The sound will still be heard positionally, unlike an AudioStreamPlayer. `ATTENUATION_DISABLED` can be combined with a `max_distance` value greater than `0.0` to achieve linear attenuation clamped to a sphere of a defined size.
**DopplerTracking:** DOPPLER_TRACKING_DISABLED=0, DOPPLER_TRACKING_IDLE_STEP=1, DOPPLER_TRACKING_PHYSICS_STEP=2
  - DOPPLER_TRACKING_DISABLED: Disables doppler tracking.
  - DOPPLER_TRACKING_IDLE_STEP: Executes doppler tracking during process frames (see `Node.NOTIFICATION_INTERNAL_PROCESS`).
  - DOPPLER_TRACKING_PHYSICS_STEP: Executes doppler tracking during physics frames (see `Node.NOTIFICATION_INTERNAL_PHYSICS_PROCESS`).

