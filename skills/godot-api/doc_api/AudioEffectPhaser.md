## AudioEffectPhaser <- AudioEffect

A "phaser" effect creates a copy of the original audio that phase-rotates differently across the entire frequency spectrum, with the use of a series of all-pass filter stages (6 in this effect). This copy modulates with a low-frequency oscillator and combines with the original audio, resulting in peaks and troughs that sweep across the spectrum. This effect can be used to create a "glassy" or "bubbly" sound.

**Props:**
- depth: float = 1.0
- feedback: float = 0.7
- range_max_hz: float = 1600.0
- range_min_hz: float = 440.0
- rate_hz: float = 0.5

- **depth**: Intensity of the effect. Value can range from 0.1 to 4.0.
- **feedback**: The volume ratio of the filtered audio that is fed back to the all-pass filters. The higher the value, the sharper and louder the peak filters created by the effect. Value can range from 0.1 to 0.9.
- **range_max_hz**: Determines the maximum frequency affected by the low-frequency oscillator modulations, in Hz. Value can range from 10 to 10000.
- **range_min_hz**: Determines the minimum frequency affected by the low-frequency oscillator modulations, in Hz. Value can range from 10 to 10000.
- **rate_hz**: Adjusts the rate in Hz at which the effect sweeps up and down across the frequency range. Value can range from 0.01 to 20.

