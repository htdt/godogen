## AudioEffectDistortion <- AudioEffect

A "distortion" effect modifies the waveform via a nonlinear mathematical function (see available ones in `Mode`), based on the amplitude of the waveform's samples. **Note:** In a nonlinear function, an input sample at *x* amplitude value, will either have its amplitude increased or decreased to a *y* value, based on the function value at *x*, which is why even at the same `drive`, the output sound will vary depending on the input's volume. To change the volume while maintaining the output waveform, use `post_gain`. In this effect, each type is a different nonlinear function. The different types available are: clip, atan, lofi (bitcrush), overdrive, and waveshape. Every distortion type available here is symmetric: negative amplitude values are affected the same way as positive ones. Although distortion will always change frequency content, usually by introducing high harmonics, different distortion types offer a range of sound qualities; from "soft" and "warm", to "crunchy" and "abrasive". For games, it can help simulate sound coming from some saturated device or speaker very efficiently. It can also help the audio stand out in a mix, by introducing higher frequencies and increasing the volume. **Note:** Although usually imperceptible, an enabled distortion effect still changes the sound even when `drive` is set to 0. This is not a bug. If this behavior is undesirable, consider disabling the effect using `AudioServer.set_bus_effect_enabled`.

**Props:**
- drive: float = 0.0
- keep_hf_hz: float = 16000.0
- mode: int (AudioEffectDistortion.Mode) = 0
- post_gain: float = 0.0
- pre_gain: float = 0.0

- **drive**: Distortion intensity. Controls how much of the input audio is affected by the distortion curve by moving from a linear function to a nonlinear one. Value can range from 0 to 1.
- **keep_hf_hz**: High-pass filter, in Hz. Frequencies higher than this value will not be affected by the distortion. Value can range from 1 to 20000.
- **mode**: Distortion type. Changes the nonlinear function used to distort the waveform. See `Mode`.
- **post_gain**: Gain after the effect, in dB. Value can range from -80 to 24.
- **pre_gain**: Gain before the effect, in dB. Value can range from -60 to 60.

**Enums:**
**Mode:** MODE_CLIP=0, MODE_ATAN=1, MODE_LOFI=2, MODE_OVERDRIVE=3, MODE_WAVESHAPE=4
  - MODE_CLIP: Flattens the waveform at 0 dB in a sharp manner. `drive` increases amplitude of samples exponentially. This mode functions as a hard clipper if `drive` is set to 0, and is the only mode that clips audio signals at 0 dB.
  - MODE_ATAN: Flattens the waveform in a smooth manner, following an arctangent curve. The audio decreases in volume, before flattening peaks to `PI * 4.0` (linear value), if it was normalized beforehand.
  - MODE_LOFI: Decreases audio bit depth to achieve a low-resolution audio signal, going from 16-bit to 2-bit. Can be used to emulate the sound of early digital audio devices.
  - MODE_OVERDRIVE: Emulates the warm distortion produced by a field effect transistor, which is commonly used in solid-state musical instrument amplifiers. `drive` has no effect in this mode.
  - MODE_WAVESHAPE: Flattens the waveform in a smooth manner, until it reaches a sharp peak at `drive = 1`, following a generic absolute sigmoid function.

