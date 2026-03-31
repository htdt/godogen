## AudioEffectBandLimitFilter <- AudioEffectFilter

A "band-limit" filter attenuates the frequencies at `AudioEffectFilter.cutoff_hz`, and allows frequencies outside the frequency threshold to pass unchanged. It is a wider and weaker version of AudioEffectNotchFilter, and is the opposite of AudioEffectBandPassFilter. This filter can be used to give more room for other sounds to play at that frequency.

