## AudioEffectPitchShift <- AudioEffect

Allows modulation of pitch without modifying speed. All frequencies can be raised or lowered with minimal effect on transients.

**Props:**
- fft_size: int (AudioEffectPitchShift.FFTSize) = 3
- oversampling: int = 4
- pitch_scale: float = 1.0

- **fft_size**: The size of the buffer. Higher values smooth out the effect over time, but have greater latency. The effects of this higher latency are especially noticeable on audio signals that have sudden amplitude changes.
- **oversampling**: The oversampling factor to use. Higher values result in better quality, but are more demanding on the CPU and may cause audio cracking if the CPU can't keep up.
- **pitch_scale**: The pitch scale to use. `1.0` is the default pitch and plays sounds unaffected. `pitch_scale` can range from 0 (infinitely low pitch, inaudible) to 16 (16 times higher than the initial pitch).

**Enums:**
**FFTSize:** FFT_SIZE_256=0, FFT_SIZE_512=1, FFT_SIZE_1024=2, FFT_SIZE_2048=3, FFT_SIZE_4096=4, FFT_SIZE_MAX=5
  - FFT_SIZE_256: Use a buffer of 256 samples for the Fast Fourier transform. Lowest latency, but least stable over time.
  - FFT_SIZE_512: Use a buffer of 512 samples for the Fast Fourier transform. Low latency, but less stable over time.
  - FFT_SIZE_1024: Use a buffer of 1024 samples for the Fast Fourier transform. This is a compromise between latency and stability over time.
  - FFT_SIZE_2048: Use a buffer of 2048 samples for the Fast Fourier transform. High latency, but stable over time.
  - FFT_SIZE_4096: Use a buffer of 4096 samples for the Fast Fourier transform. Highest latency, but most stable over time.
  - FFT_SIZE_MAX: Represents the size of the `FFTSize` enum.

