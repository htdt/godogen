## ResourceImporterBitMap <- ResourceImporter

BitMap resources are typically used as click masks in TextureButton and TouchScreenButton.

**Props:**
- create_from: int = 0
- threshold: float = 0.5

- **create_from**: The data source to use for generating the bitmap. **Black & White:** Pixels whose HSV value is greater than the `threshold` will be considered as "enabled" (bit is `true`). If the pixel is lower than or equal to the threshold, it will be considered as "disabled" (bit is `false`). **Alpha:** Pixels whose alpha value is greater than the `threshold` will be considered as "enabled" (bit is `true`). If the pixel is lower than or equal to the threshold, it will be considered as "disabled" (bit is `false`).
- **threshold**: The threshold to use to determine which bits should be considered enabled or disabled. See also `create_from`.

