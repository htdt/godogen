## AudioStreamPlaybackResampled <- AudioStreamPlayback

Playback class used to mix an AudioStream's audio samples to `AudioServer.get_mix_rate` using cubic interpolation.

**Methods:**
- _get_stream_sampling_rate() -> float - Returns an AudioStream's sample rate, in Hz. Used to perform resampling.
- _mix_resampled(dst_buffer: AudioFrame*, frame_count: int) -> int - Called by `begin_resample` to mix an AudioStream to `AudioServer.get_mix_rate`. Uses `_get_stream_sampling_rate` as the source sample rate. Returns the number of mixed frames.
- begin_resample() - Called when an AudioStream is played. Clears the cubic interpolation history and starts mixing by calling `_mix_resampled`.

