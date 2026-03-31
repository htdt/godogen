## AudioEffectFilter <- AudioEffect

A "filter" controls the gain of frequencies, using `cutoff_hz` as a frequency threshold. Filters can help to give room for each sound, and create interesting effects. There are different types of filter that inherit this class: Shelf filters: AudioEffectLowShelfFilter and AudioEffectHighShelfFilter Band-pass and notch filters: AudioEffectBandPassFilter, AudioEffectBandLimitFilter, and AudioEffectNotchFilter Low/high-pass filters: AudioEffectLowPassFilter and AudioEffectHighPassFilter

**Props:**
- cutoff_hz: float = 2000.0
- db: int (AudioEffectFilter.FilterDB) = 0
- gain: float = 1.0
- resonance: float = 0.5

- **cutoff_hz**: Frequency threshold for the filter, in Hz. Value can range from 1 to 20500.
- **db**: Steepness of the cutoff curve in dB per octave (twice the frequency above `cutoff_hz`, or half the frequency below `cutoff_hz`), also known as the "order" of the filter. Higher orders have a more aggressive cutoff.
- **gain**: Gain of the frequencies affected by the filter. This property is only available for AudioEffectLowShelfFilter and AudioEffectHighShelfFilter. Value can range from 0 to 4.
- **resonance**: Gain at or directly next to the `cutoff_hz` frequency threshold. Value can range from 0 to 1. Its exact behavior depends on the selected filter type: - For shelf filters, it accentuates or masks the order by increasing frequencies right next to the `cutoff_hz` frequency and decreasing frequencies on the opposite side. - For the band-pass and notch filters, it widens or narrows the filter at the `cutoff_hz` frequency threshold. - For low/high-pass filters, it increases or decreases frequencies at the `cutoff_hz` frequency threshold.

**Enums:**
**FilterDB:** FILTER_6DB=0, FILTER_12DB=1, FILTER_18DB=2, FILTER_24DB=3
  - FILTER_6DB: Cutting off at 6 dB per octave. One octave is twice the frequency above `cutoff_hz`, or half the frequency below `cutoff_hz`.
  - FILTER_12DB: Cutting off at 12 dB per octave. One octave is twice the frequency above `cutoff_hz`, or half the frequency below `cutoff_hz`.
  - FILTER_18DB: Cutting off at 18 dB per octave. One octave is twice the frequency above `cutoff_hz`, or half the frequency below `cutoff_hz`.
  - FILTER_24DB: Cutting off at 24 dB per octave. One octave is twice the frequency above `cutoff_hz`, or half the frequency below `cutoff_hz`.

