## AudioEffectPanner <- AudioEffect

Determines how much of the audio signal is sent to the left and right channels. This helps with audio spatialization, giving sounds distinct places in a mix. AudioStreamPlayer2D and AudioStreamPlayer3D handle panning automatically, following where the source of the sound is on the screen.

**Props:**
- pan: float = 0.0

- **pan**: Pan position. Negative values pan the sound to the left, positive pan to the right. Value can range from -1 to 1.

