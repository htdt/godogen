## AudioEffectNotchFilter <- AudioEffectFilter

A "notch" filter attenuates frequencies at `AudioEffectFilter.cutoff_hz` and allows frequencies outside the frequency threshold to pass unchanged. It is a narrower and stronger version of AudioEffectBandLimitFilter, and is the opposite of AudioEffectBandPassFilter. This filter can be used to give more room for other sounds to play at that frequency. Because of how much it attenuates frequencies, it can also be used to completely remove undesired frequencies.

