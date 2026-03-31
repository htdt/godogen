## AudioEffectDelay <- AudioEffect

A "delay" effect plays the input audio signal back after a period of time. Each repetition is called a "delay tap" or simply "tap". Delay taps may be played back multiple times to create the sound of a repeating, decaying echo. Delay effects range from a subtle echo to a pronounced blending of previous sounds with new sounds. See also AudioEffectReverb for a blurry, continuous echo.

**Props:**
- dry: float = 1.0
- feedback_active: bool = false
- feedback_delay_ms: float = 340.0
- feedback_level_db: float = -6.0
- feedback_lowpass: float = 16000.0
- tap1_active: bool = true
- tap1_delay_ms: float = 250.0
- tap1_level_db: float = -6.0
- tap1_pan: float = 0.2
- tap2_active: bool = true
- tap2_delay_ms: float = 500.0
- tap2_level_db: float = -12.0
- tap2_pan: float = -0.4

- **dry**: The volume ratio of the original audio. Value can range from 0 to 1.
- **feedback_active**: If `true`, feedback is enabled, repeating taps after they are played.
- **feedback_delay_ms**: Feedback delay time in milliseconds. Value can range from 0 to 1500.
- **feedback_level_db**: Gain for feedback, in dB. Value can range from -60 to 0.
- **feedback_lowpass**: Low-pass filter for feedback, in Hz. Frequencies above this value are filtered out. Value can range from 1 to 16000.
- **tap1_active**: If `true`, the first tap will be enabled.
- **tap1_delay_ms**: First tap delay time in milliseconds, compared to the original audio. Value can range from 0 to 1500.
- **tap1_level_db**: Gain for the first tap, in dB. Value can range from -60 to 0.
- **tap1_pan**: Pan position for the first tap. Negative values pan the sound to the left, positive pan to the right. Value can range from -1 to 1.
- **tap2_active**: If `true`, the second tap will be enabled.
- **tap2_delay_ms**: Second tap delay time in milliseconds, compared to the original audio. Value can range from 0 to 1500.
- **tap2_level_db**: Gain for the second tap, in dB. Value can range from -60 to 0.
- **tap2_pan**: Pan position for the second tap. Negative values pan the sound to the left, positive pan to the right. Value can range from -1 to 1.

