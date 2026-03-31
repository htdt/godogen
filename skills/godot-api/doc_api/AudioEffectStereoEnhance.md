## AudioEffectStereoEnhance <- AudioEffect

Adjusts gain of the left and right channels, and makes mono sounds stereo through phase shifting.

**Props:**
- pan_pullout: float = 1.0
- surround: float = 0.0
- time_pullout_ms: float = 0.0

- **pan_pullout**: Gain of the side channels, if they exist. A value of 0 will downmix stereo to mono. Value can range from 0 to 4.
- **surround**: Widens the stereo image through phase shifting in conjunction with `time_pullout_ms`. Just pans sound to the left channel if `time_pullout_ms` is 0. Value can range from 0 to 1.
- **time_pullout_ms**: Widens the stereo image through phase shifting in conjunction with `surround`. Just delays the right channel if `surround` is 0. Value is in milliseconds, and can range from 0 to 50.

