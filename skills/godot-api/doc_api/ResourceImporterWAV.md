## ResourceImporterWAV <- ResourceImporter

WAV is an uncompressed format, which can provide higher quality compared to Ogg Vorbis and MP3. It also has the lowest CPU cost to decode. This means high numbers of WAV sounds can be played at the same time, even on low-end devices. By default, Godot imports WAV files using the lossy Quite OK Audio compression. You may change this by setting the `compress/mode` property.

**Props:**
- compress/mode: int = 2
- edit/loop_begin: int = 0
- edit/loop_end: int = -1
- edit/loop_mode: int = 0
- edit/normalize: bool = false
- edit/trim: bool = false
- force/8_bit: bool = false
- force/max_rate: bool = false
- force/max_rate_hz: float = 44100
- force/mono: bool = false

- **compress/mode**: The compression mode to use on import. - **PCM (Uncompressed):** Imports audio data without any form of compression, preserving the highest possible quality. It has the lowest CPU cost, but the highest memory usage. - **IMA ADPCM:** Applies fast, lossy compression during import, noticeably decreasing the quality, but with low CPU cost and memory usage. Does not support seeking and only Forward loop mode is supported. - **:** Also applies lossy compression on import, having a slightly higher CPU cost compared to IMA ADPCM, but much higher quality and the lowest memory usage.
- **edit/loop_begin**: The begin loop point to use when `edit/loop_mode` is **Forward**, **Ping-Pong**, or **Backward**. This is set in samples after the beginning of the audio file.
- **edit/loop_end**: The end loop point to use when `edit/loop_mode` is **Forward**, **Ping-Pong**, or **Backward**. This is set in samples after the beginning of the audio file. A value of `-1` uses the end of the audio file as the end loop point.
- **edit/loop_mode**: Controls how audio should loop. - **Detect From WAV:** Uses loop information from the WAV metadata. - **Disabled:** Don't loop audio, even if the metadata indicates the file playback should loop. - **Forward:** Standard audio looping. Plays the audio forward from the beginning to `edit/loop_end`, then returns to `edit/loop_begin` and repeats. - **Ping-Pong:** Plays the audio forward until `edit/loop_end`, then backwards to `edit/loop_begin`, repeating this cycle. - **Backward:** Plays the audio backwards from `edit/loop_end` to `edit/loop_begin`, then repeats. **Note:** In AudioStreamPlayer, the `AudioStreamPlayer.finished` signal won't be emitted for looping audio when it reaches the end of the audio file, as the audio will keep playing indefinitely.
- **edit/normalize**: If `true`, normalize the audio volume so that its peak volume is equal to 0 dB. When enabled, normalization will make audio sound louder depending on its original peak volume.
- **edit/trim**: If `true`, automatically trim the beginning and end of the audio if it's lower than -50 dB after normalization (see `edit/normalize`). This prevents having files with silence at the beginning or end, which increases their size unnecessarily and adds latency to the moment they are played back. A fade-in/fade-out period of 500 samples is also used during trimming to avoid audible pops.
- **force/8_bit**: If `true`, forces the imported audio to use 8-bit quantization if the source file is 16-bit or higher. Enabling this is generally not recommended, as 8-bit quantization decreases audio quality significantly. If you need smaller file sizes, consider using Ogg Vorbis or MP3 audio instead.
- **force/max_rate**: If set to a value greater than `0`, forces the audio's sample rate to be reduced to a value lower than or equal to the value specified in `force/max_rate_hz`. This can decrease file size noticeably on certain sounds, without impacting quality depending on the actual sound's contents. See for more information.
- **force/max_rate_hz**: The frequency to limit the imported audio sample to (in Hz). Only effective if `force/max_rate` is `true`.
- **force/mono**: If `true`, forces the imported audio to be mono if the source file is stereo. This decreases the file size by 50% by merging the two channels into one.

