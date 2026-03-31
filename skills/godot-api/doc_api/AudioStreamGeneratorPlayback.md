## AudioStreamGeneratorPlayback <- AudioStreamPlaybackResampled

This class is meant to be used with AudioStreamGenerator to play back the generated audio in real-time.

**Methods:**
- can_push_buffer(amount: int) -> bool - Returns `true` if a buffer of the size `amount` can be pushed to the audio sample data buffer without overflowing it, `false` otherwise.
- clear_buffer() - Clears the audio sample data buffer.
- get_frames_available() -> int - Returns the number of frames that can be pushed to the audio sample data buffer without overflowing it. If the result is `0`, the buffer is full.
- get_skips() -> int - Returns the number of times the playback skipped due to a buffer underrun in the audio sample data. This value is reset at the start of the playback.
- push_buffer(frames: PackedVector2Array) -> bool - Pushes several audio data frames to the buffer. This is usually more efficient than `push_frame` in C# and compiled languages via GDExtension, but `push_buffer` may be *less* efficient in GDScript.
- push_frame(frame: Vector2) -> bool - Pushes a single audio data frame to the buffer. This is usually less efficient than `push_buffer` in C# and compiled languages via GDExtension, but `push_frame` may be *more* efficient in GDScript.

