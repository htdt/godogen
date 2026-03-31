## AudioEffectEQ <- AudioEffect

An "equalizer" gives you control over the gain of frequencies in the entire spectrum, by allowing their adjustment through bands. A band is a point in the frequency spectrum, and each band means a division of the spectrum that can be adjusted. Use equalizers to compensate for existing deficiencies in the audio, make room for other elements, or remove undesirable frequencies. AudioEffectEQs are useful on the Master bus to balance the entire mix or give it more character. They are also useful when a game is run on a mobile device, to adjust the mix to that kind of speakers (it can be disabled when headphones are plugged in).

**Methods:**
- get_band_count() -> int - Returns the number of bands of the equalizer.
- get_band_gain_db(band_idx: int) -> float - Returns the band's gain at the specified index, in dB.
- set_band_gain_db(band_idx: int, volume_db: float) - Sets band's gain at the specified index, in dB.

