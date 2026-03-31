## VideoStreamPlayer <- Control

A control used for playback of VideoStream resources. Supported video formats are (`.ogv`, VideoStreamTheora) and any format exposed via a GDExtension plugin. **Warning:** On Web, video playback *will* perform poorly due to missing architecture-specific assembly optimizations.

**Props:**
- audio_track: int = 0
- autoplay: bool = false
- buffering_msec: int = 500
- bus: StringName = &"Master"
- expand: bool = false
- loop: bool = false
- paused: bool = false
- speed_scale: float = 1.0
- stream: VideoStream
- stream_position: float
- volume: float
- volume_db: float = 0.0

- **audio_track**: The embedded audio track to play.
- **autoplay**: If `true`, playback starts when the scene loads.
- **buffering_msec**: Amount of time in milliseconds to store in buffer while playing.
- **bus**: Audio bus to use for sound playback.
- **expand**: If `true`, the video scales to the control size. Otherwise, the control minimum size will be automatically adjusted to match the video stream's dimensions.
- **loop**: If `true`, the video restarts when it reaches its end.
- **paused**: If `true`, the video is paused.
- **speed_scale**: The stream's current speed scale. `1.0` is the normal speed, while `2.0` is double speed and `0.5` is half speed. A speed scale of `0.0` pauses the video, similar to setting `paused` to `true`.
- **stream**: The assigned video stream. See description for supported formats.
- **stream_position**: The current position of the stream, in seconds.
- **volume**: Audio volume as a linear value.
- **volume_db**: Audio volume in dB.

**Methods:**
- get_stream_length() -> float - The length of the current stream, in seconds.
- get_stream_name() -> String - Returns the video stream's name, or `"<No Stream>"` if no video stream is assigned.
- get_video_texture() -> Texture2D - Returns the current frame as a Texture2D.
- is_playing() -> bool - Returns `true` if the video is playing. **Note:** The video is still considered playing if paused during playback.
- play() - Starts the video playback from the beginning. If the video is paused, this will not unpause the video.
- stop() - Stops the video playback and sets the stream position to 0. **Note:** Although the stream position will be set to 0, the first frame of the video stream won't become the current frame.

**Signals:**
- finished - Emitted when playback is finished.

