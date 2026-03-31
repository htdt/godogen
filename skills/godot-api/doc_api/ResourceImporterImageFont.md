## ResourceImporterImageFont <- ResourceImporter

This image-based workflow can be easier to use than ResourceImporterBMFont, but it requires all glyphs to have the same width and height, glyph advances and drawing offsets can be customized. This makes ResourceImporterImageFont most suited to fixed-width fonts. See also ResourceImporterDynamicFont.

**Props:**
- ascent: int = 0
- character_margin: Rect2i = Rect2i(0, 0, 0, 0)
- character_ranges: PackedStringArray = PackedStringArray()
- columns: int = 1
- compress: bool = true
- descent: int = 0
- fallbacks: Array = []
- image_margin: Rect2i = Rect2i(0, 0, 0, 0)
- kerning_pairs: PackedStringArray = PackedStringArray()
- rows: int = 1
- scaling_mode: int = 2

- **ascent**: Font ascent (number of pixels above the baseline). If set to `0`, half of the character height is used.
- **character_margin**: Margin applied around every imported glyph. If your font image contains guides (in the form of lines between glyphs) or if spacing between characters appears incorrect, try adjusting `character_margin`.
- **character_ranges**: The character ranges to import from the font image. This is an array that maps each position on the image (in tile coordinates, not pixels). The font atlas is traversed from left to right and top to bottom. Characters can be specified with decimal numbers (126), hexadecimal numbers (`0x007e` or `U+007e`), or between single quotes (`'~'`). Ranges can be specified with a hyphen between characters. For example, `0-127` represents the full ASCII range. It can also be written as `0x0000-0x007f` (or `U+0000-U+007f`). As another example, `' '-'~'` is equivalent to `32-126` and represents the range of printable (visible) ASCII characters. For any range, the character advance and offset can be customized by appending three space-separated integer values (additional advance, x offset, y offset) to the end. For example `'a'-'b' 4 5 2` sets the advance to `char_width + 4` and offset to `Vector2(5, 2)` for both `a` and `b` characters. **Note:** The overall number of characters must not exceed the number of `columns` multiplied by `rows`. Otherwise, the font will fail to import.
- **columns**: Number of columns in the font image. See also `rows`.
- **compress**: If `true`, uses lossless compression for the resulting font.
- **descent**: Font descent (number of pixels below the baseline). If set to `0`, half of the character height is used.
- **fallbacks**: List of font fallbacks to use if a glyph isn't found in this bitmap font. Fonts at the beginning of the array are attempted first.
- **image_margin**: Margin to cut on the sides of the entire image. This can be used to cut parts of the image that contain attribution information or similar.
- **kerning_pairs**: Kerning pairs for the font. Kerning pair adjust the spacing between two characters. Each string consist of three space separated values: "from" string, "to" string and integer offset. Each combination form the two string for a kerning pair, e.g, `ab cd -3` will create kerning pairs `ac`, `ad`, `bc`, and `bd` with offset `-3`. `\uXXXX` escape sequences can be used to add Unicode characters.
- **rows**: Number of rows in the font image. See also `columns`.
- **scaling_mode**: Font scaling mode.

