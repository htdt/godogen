## AudioEffectLimiter <- AudioEffect

A "limiter" is an audio effect designed to stop audio signals from exceeding a specified volume threshold level, and usually works by decreasing the volume or soft-clipping the audio. Adding one in the Master bus is always recommended to prevent clipping when the volume goes above 0 dB. Soft clipping starts to decrease the peaks a little below the volume threshold level and progressively increases its effect as the input volume increases such that the threshold level is never exceeded. If hard clipping is desired, consider `AudioEffectDistortion.MODE_CLIP`.

**Props:**
- ceiling_db: float = -0.1
- soft_clip_db: float = 2.0
- soft_clip_ratio: float = 10.0
- threshold_db: float = 0.0

- **ceiling_db**: The waveform's maximum allowed value, in dB. Value can range from -20 to -0.1.
- **soft_clip_db**: Modifies the volume of the limited waves, in dB. Value can range from 0 to 6.
- **soft_clip_ratio**: This property has no effect on the audio. Use AudioEffectHardLimiter instead, as this Limiter effect is deprecated.
- **threshold_db**: The volume threshold level from which the limiter begins to be active, in dB. Value can range from -30 to 0.

