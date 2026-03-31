## AudioStreamPolyphonic <- AudioStream

AudioStream that lets the user play custom streams at any time from code, simultaneously using a single player. Playback control is done via the AudioStreamPlaybackPolyphonic instance set inside the player, which can be obtained via `AudioStreamPlayer.get_stream_playback`, `AudioStreamPlayer2D.get_stream_playback` or `AudioStreamPlayer3D.get_stream_playback` methods. Obtaining the playback instance is only valid after the `stream` property is set as an AudioStreamPolyphonic in those players.

**Props:**
- polyphony: int = 32

- **polyphony**: Maximum amount of simultaneous streams that can be played.

