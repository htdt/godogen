## VideoStreamPlayback <- Resource

This class is intended to be overridden by video decoder extensions with custom implementations of VideoStream.

**Methods:**
- _get_channels() -> int - Returns the number of audio channels.
- _get_length() -> float - Returns the video duration in seconds, if known, or 0 if unknown.
- _get_mix_rate() -> int - Returns the audio sample rate used for mixing.
- _get_playback_position() -> float - Return the current playback timestamp. Called in response to the `VideoStreamPlayer.stream_position` getter.
- _get_texture() -> Texture2D - Allocates a Texture2D in which decoded video frames will be drawn.
- _is_paused() -> bool - Returns the paused status, as set by `_set_paused`.
- _is_playing() -> bool - Returns the playback state, as determined by calls to `_play` and `_stop`.
- _play() - Called in response to `VideoStreamPlayer.autoplay` or `VideoStreamPlayer.play`. Note that manual playback may also invoke `_stop` multiple times before this method is called. `_is_playing` should return `true` once playing.
- _seek(time: float) - Seeks to `time` seconds. Called in response to the `VideoStreamPlayer.stream_position` setter.
- _set_audio_track(idx: int) - Select the audio track `idx`. Called when playback starts, and in response to the `VideoStreamPlayer.audio_track` setter.
- _set_paused(paused: bool) - Set the paused status of video playback. `_is_paused` must return `paused`. Called in response to the `VideoStreamPlayer.paused` setter.
- _stop() - Stops playback. May be called multiple times before `_play`, or in response to `VideoStreamPlayer.stop`. `_is_playing` should return `false` once stopped.
- _update(delta: float) - Ticks video playback for `delta` seconds. Called every frame as long as both `_is_paused` and `_is_playing` return `true`.
- mix_audio(num_frames: int, buffer: PackedFloat32Array = PackedFloat32Array(), offset: int = 0) -> int - Render `num_frames` audio frames (of `_get_channels` floats each) from `buffer`, starting from index `offset` in the array. Returns the number of audio frames rendered, or -1 on error.

