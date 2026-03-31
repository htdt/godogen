## ResourceImporterBMFont <- ResourceImporter

The BMFont format is a format created by the program. Many BMFont-compatible programs also exist, like . Compared to ResourceImporterImageFont, ResourceImporterBMFont supports bitmap fonts with varying glyph widths/heights. See also ResourceImporterDynamicFont.

**Props:**
- compress: bool = true
- fallbacks: Array = []
- scaling_mode: int = 2

- **compress**: If `true`, uses lossless compression for the resulting font.
- **fallbacks**: List of font fallbacks to use if a glyph isn't found in this bitmap font. Fonts at the beginning of the array are attempted first.
- **scaling_mode**: Font scaling mode.

