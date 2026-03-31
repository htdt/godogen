## AudioEffectSpectrumAnalyzer <- AudioEffect

Calculates a Fourier Transform of the audio signal. This effect does not alter the audio. Can be used for creating real-time audio visualizations, like a spectrogram. This resource configures an AudioEffectSpectrumAnalyzerInstance, which performs the actual analysis at runtime. An instance should be obtained with `AudioServer.get_bus_effect_instance` to make use of this effect.

**Props:**
- buffer_length: float = 2.0
- fft_size: int (AudioEffectSpectrumAnalyzer.FFTSize) = 2

- **buffer_length**: The length of the buffer to keep, in seconds. Higher values keep data around for longer, but require more memory. Value can range from 0.1 to 4.
- **fft_size**: The size of the buffer. Higher values smooth out the spectrum analysis over time, but have greater latency. The effects of this higher latency are especially noticeable with sudden amplitude changes.

**Enums:**
**FFTSize:** FFT_SIZE_256=0, FFT_SIZE_512=1, FFT_SIZE_1024=2, FFT_SIZE_2048=3, FFT_SIZE_4096=4, FFT_SIZE_MAX=5
  - FFT_SIZE_256: Use a buffer of 256 samples for the Fast Fourier transform. Lowest latency, but least stable over time.
  - FFT_SIZE_512: Use a buffer of 512 samples for the Fast Fourier transform. Low latency, but less stable over time.
  - FFT_SIZE_1024: Use a buffer of 1024 samples for the Fast Fourier transform. This is a compromise between latency and stability over time.
  - FFT_SIZE_2048: Use a buffer of 2048 samples for the Fast Fourier transform. High latency, but stable over time.
  - FFT_SIZE_4096: Use a buffer of 4096 samples for the Fast Fourier transform. Highest latency, but most stable over time.
  - FFT_SIZE_MAX: Represents the size of the `FFTSize` enum.

