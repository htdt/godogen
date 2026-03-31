## AudioEffectReverb <- AudioEffect

A "reverb" effect plays the input audio back continuously, decaying over a period of time. It simulates sounds in different kinds of spaces, ranging from small rooms, to big caverns. See also AudioEffectDelay for a non-blurry type of echo.

**Props:**
- damping: float = 0.5
- dry: float = 1.0
- hipass: float = 0.0
- predelay_feedback: float = 0.4
- predelay_msec: float = 150.0
- room_size: float = 0.8
- spread: float = 1.0
- wet: float = 0.5

- **damping**: Defines how reflective the imaginary room's walls are. The more reflective, the more high frequency content the reverb has. Value can range from 0 to 1.
- **dry**: The volume ratio of the original audio. At 0, only the modified audio is outputted. Value can range from 0 to 1.
- **hipass**: High-pass filter allows frequencies higher than a certain cutoff threshold and attenuates frequencies lower than the cutoff threshold. Value can range from 0 to 1.
- **predelay_feedback**: Gain of early reflection copies. At higher values, early reflection copies are louder and ring out for longer. Value can range from 0 to 1.
- **predelay_msec**: Time between the original audio and the early reflections of the reverb signal, in milliseconds. Value can range from 20 to 500.
- **room_size**: Dimensions of simulated room. Bigger means more echoes. Value can range from 0 to 1.
- **spread**: Widens or narrows the stereo image of the reverb tail. At 1, it fully widens. Value can range from 0 to 1.
- **wet**: The volume ratio of the modified audio. At 0, only the original audio is outputted. Value can range from 0 to 1.

