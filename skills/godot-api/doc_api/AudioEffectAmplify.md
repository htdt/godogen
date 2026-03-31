## AudioEffectAmplify <- AudioEffect

Increases or decreases the volume being routed through the audio bus.

**Props:**
- volume_db: float = 0.0
- volume_linear: float

- **volume_db**: Amount of amplification in dB. Positive values make the sound louder, negative values make it quieter. Value can range from -80 to 24.
- **volume_linear**: Amount of amplification as a linear value. **Note:** This member modifies `volume_db` for convenience. The returned value is equivalent to the result of `@GlobalScope.db_to_linear` on `volume_db`. Setting this member is equivalent to setting `volume_db` to the result of `@GlobalScope.linear_to_db` on a value.

