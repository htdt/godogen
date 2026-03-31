## AudioEffectChorus <- AudioEffect

A "chorus" effect creates multiple copies of the original audio (called "voices") with variations in pitch, and layers on top of the original, giving the impression that the sound comes from multiple sources. This creates spectral and spatial movement. Each voice is played a short period of time after the original audio, controlled by `delay`. An internal low-frequency oscillator (LFO) controls their pitch, and `depth` controls the LFO's maximum amount. In the real world, this kind of effect is found in pianos, choirs, and instrument ensembles. This effect can also be used to widen mono audio and make digital sounds have a more natural or analog quality.

**Props:**
- dry: float = 1.0
- voice/1/cutoff_hz: float = 8000.0
- voice/1/delay_ms: float = 15.0
- voice/1/depth_ms: float = 2.0
- voice/1/level_db: float = 0.0
- voice/1/pan: float = -0.5
- voice/1/rate_hz: float = 0.8
- voice/2/cutoff_hz: float = 8000.0
- voice/2/delay_ms: float = 20.0
- voice/2/depth_ms: float = 3.0
- voice/2/level_db: float = 0.0
- voice/2/pan: float = 0.5
- voice/2/rate_hz: float = 1.2
- voice/3/cutoff_hz: float
- voice/3/delay_ms: float
- voice/3/depth_ms: float
- voice/3/level_db: float
- voice/3/pan: float
- voice/3/rate_hz: float
- voice/4/cutoff_hz: float
- voice/4/delay_ms: float
- voice/4/depth_ms: float
- voice/4/level_db: float
- voice/4/pan: float
- voice/4/rate_hz: float
- voice_count: int = 2
- wet: float = 0.5

- **dry**: The volume ratio of the original audio. Value can range from 0 to 1.
- **voice/1/cutoff_hz**: The frequency threshold of the voice's low-pass filter in Hz.
- **voice/1/delay_ms**: The delay of the voice in milliseconds, compared to the original audio.
- **voice/1/depth_ms**: The depth of the voice's low-frequency oscillator in milliseconds.
- **voice/1/level_db**: The gain of the voice in dB.
- **voice/1/pan**: The pan position of the voice.
- **voice/1/rate_hz**: The rate of the voice's low-frequency oscillator in Hz.
- **voice/2/cutoff_hz**: The frequency threshold of the voice's low-pass filter in Hz.
- **voice/2/delay_ms**: The delay of the voice in milliseconds, compared to the original audio.
- **voice/2/depth_ms**: The depth of the voice's low-frequency oscillator in milliseconds.
- **voice/2/level_db**: The gain of the voice in dB.
- **voice/2/pan**: The pan position of the voice.
- **voice/2/rate_hz**: The rate of the voice's low-frequency oscillator in Hz.
- **voice/3/cutoff_hz**: The frequency threshold of the voice's low-pass filter in Hz.
- **voice/3/delay_ms**: The delay of the voice in milliseconds, compared to the original audio.
- **voice/3/depth_ms**: The depth of the voice's low-frequency oscillator in milliseconds.
- **voice/3/level_db**: The gain of the voice in dB.
- **voice/3/pan**: The pan position of the voice.
- **voice/3/rate_hz**: The rate of the voice's low-frequency oscillator in Hz.
- **voice/4/cutoff_hz**: The frequency threshold of the voice's low-pass filter in Hz.
- **voice/4/delay_ms**: The delay of the voice in milliseconds, compared to the original audio.
- **voice/4/depth_ms**: The depth of the voice's low-frequency oscillator in milliseconds.
- **voice/4/level_db**: The gain of the voice in dB.
- **voice/4/pan**: The pan position of the voice.
- **voice/4/rate_hz**: The rate of the voice's low-frequency oscillator in Hz.
- **voice_count**: The number of voices in the effect. Value can range from 1 to 4.
- **wet**: The volume ratio of all voices. Value can range from 0 to 1.

**Methods:**
- get_voice_cutoff_hz(voice_idx: int) -> float - Returns the frequency threshold of a given `voice_idx`'s low-pass filter in Hz. Frequencies above this value are removed from the voice.
- get_voice_delay_ms(voice_idx: int) -> float - Returns the delay of a given `voice_idx` in milliseconds, compared to the original audio.
- get_voice_depth_ms(voice_idx: int) -> float - Returns the depth of a given `voice_idx`'s low-frequency oscillator in milliseconds.
- get_voice_level_db(voice_idx: int) -> float - Returns the gain of a given `voice_idx` in dB.
- get_voice_pan(voice_idx: int) -> float - Returns the pan position of a given `voice_idx`. Negative values mean the left channel, positive mean the right.
- get_voice_rate_hz(voice_idx: int) -> float - Returns the rate of a given `voice_idx`'s low-frequency oscillator in Hz.
- set_voice_cutoff_hz(voice_idx: int, cutoff_hz: float) - Sets the frequency threshold of a given `voice_idx`'s low-pass filter in Hz. Frequencies above `cutoff_hz` are removed from `voice_idx`. Value can range from 1 to 20500.
- set_voice_delay_ms(voice_idx: int, delay_ms: float) - Sets the delay of a given `voice_idx` in milliseconds, compared to the original audio. Value can range from 0 to 50.
- set_voice_depth_ms(voice_idx: int, depth_ms: float) - Sets the depth of a given `voice_idx`'s low-frequency oscillator in milliseconds. Value can range from 0 to 20.
- set_voice_level_db(voice_idx: int, level_db: float) - Sets the gain of a given `voice_idx` in dB. Value can range from -60 to 24.
- set_voice_pan(voice_idx: int, pan: float) - Sets the pan position of a given `voice_idx`. Negative values pan the sound to the left, positive pan to the right. Value can range from -1 to 1.
- set_voice_rate_hz(voice_idx: int, rate_hz: float) - Sets the rate of a given `voice_idx`'s low-frequency oscillator in Hz. Value can range from 0.1 to 20.

