## AudioEffectSpectrumAnalyzerInstance <- AudioEffectInstance

The runtime part of an AudioEffectSpectrumAnalyzer, which can be used to query the magnitude of a frequency range on its host bus. An instance of this class can be obtained with `AudioServer.get_bus_effect_instance`.

**Methods:**
- get_magnitude_for_frequency_range(from_hz: float, to_hz: float, mode: int = 1) -> Vector2 - Returns the magnitude of the frequencies from `from_hz` to `to_hz` in linear energy as a Vector2. The `x` component of the return value represents the left stereo channel, and `y` represents the right channel. `mode` determines how the frequency range will be processed.

**Enums:**
**MagnitudeMode:** MAGNITUDE_AVERAGE=0, MAGNITUDE_MAX=1
  - MAGNITUDE_AVERAGE: Use the average value across the frequency range as magnitude.
  - MAGNITUDE_MAX: Use the maximum value of the frequency range as magnitude.

