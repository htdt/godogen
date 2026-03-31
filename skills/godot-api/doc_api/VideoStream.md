## VideoStream <- Resource

Base resource type for all video streams. Classes that derive from VideoStream can all be used as resource types to play back videos in VideoStreamPlayer.

**Props:**
- file: String = ""

- **file**: The video file path or URI that this VideoStream resource handles. For VideoStreamTheora, this filename should be an Ogg Theora video file with the `.ogv` extension.

**Methods:**
- _instantiate_playback() -> VideoStreamPlayback - Called when the video starts playing, to initialize and return a subclass of VideoStreamPlayback.

