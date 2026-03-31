## AudioStreamGenerator <- AudioStream

AudioStreamGenerator is a type of audio stream that does not play back sounds on its own; instead, it expects a script to generate audio data for it. See also AudioStreamGeneratorPlayback. Here's a sample on how to use it to generate a sine wave: In the example above, the "AudioStreamPlayer" node must use an AudioStreamGenerator as its stream. The `fill_buffer` function provides audio data for approximating a sine wave. See also AudioEffectSpectrumAnalyzer for performing real-time audio spectrum analysis. **Note:** Due to performance constraints, this class is best used from C# or from a compiled language via GDExtension. If you still want to use this class from GDScript, consider using a lower `mix_rate` such as 11,025 Hz or 22,050 Hz.

**Props:**
- buffer_length: float = 0.5
- mix_rate: float = 44100.0
- mix_rate_mode: int (AudioStreamGenerator.AudioStreamGeneratorMixRate) = 2

- **buffer_length**: The length of the buffer to generate (in seconds). Lower values result in less latency, but require the script to generate audio data faster, resulting in increased CPU usage and more risk for audio cracking if the CPU can't keep up.
- **mix_rate**: The sample rate to use (in Hz). Higher values are more demanding for the CPU to generate, but result in better quality. In games, common sample rates in use are `11025`, `16000`, `22050`, `32000`, `44100`, and `48000`. According to the , there is no quality difference to human hearing when going past 40,000 Hz (since most humans can only hear up to ~20,000 Hz, often less). If you are generating lower-pitched sounds such as voices, lower sample rates such as `32000` or `22050` may be usable with no loss in quality. **Note:** AudioStreamGenerator is not automatically resampling input data, to produce expected result `mix_rate_mode` should match the sampling rate of input data. **Note:** If you are using AudioEffectCapture as the source of your data, set `mix_rate_mode` to `MIX_RATE_INPUT` or `MIX_RATE_OUTPUT` to automatically match current AudioServer mixing rate.
- **mix_rate_mode**: Mixing rate mode. If set to `MIX_RATE_CUSTOM`, `mix_rate` is used, otherwise current AudioServer mixing rate is used.

**Enums:**
**AudioStreamGeneratorMixRate:** MIX_RATE_OUTPUT=0, MIX_RATE_INPUT=1, MIX_RATE_CUSTOM=2, MIX_RATE_MAX=3
  - MIX_RATE_OUTPUT: Current AudioServer output mixing rate.
  - MIX_RATE_INPUT: Current AudioServer input mixing rate.
  - MIX_RATE_CUSTOM: Custom mixing rate, specified by `mix_rate`.
  - MIX_RATE_MAX: Maximum value for the mixing rate mode enum.

