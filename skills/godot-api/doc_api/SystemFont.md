## SystemFont <- Font

SystemFont loads a font from a system font with the first matching name from `font_names`. It will attempt to match font style, but it's not guaranteed. The returned font might be part of a font collection or be a variable font with OpenType "weight", "width" and/or "italic" features set. You can create FontVariation of the system font for precise control over its features. **Note:** This class is implemented on iOS, Linux, macOS and Windows, on other platforms it will fallback to default theme font.

**Props:**
- allow_system_fallback: bool = true
- antialiasing: int (TextServer.FontAntialiasing) = 1
- disable_embedded_bitmaps: bool = true
- font_italic: bool = false
- font_names: PackedStringArray = PackedStringArray()
- font_stretch: int = 100
- font_weight: int = 400
- force_autohinter: bool = false
- generate_mipmaps: bool = false
- hinting: int (TextServer.Hinting) = 1
- keep_rounding_remainders: bool = true
- modulate_color_glyphs: bool = false
- msdf_pixel_range: int = 16
- msdf_size: int = 48
- multichannel_signed_distance_field: bool = false
- oversampling: float = 0.0
- subpixel_positioning: int (TextServer.SubpixelPositioning) = 1

- **allow_system_fallback**: If set to `true`, system fonts can be automatically used as fallbacks.
- **antialiasing**: Font anti-aliasing mode.
- **disable_embedded_bitmaps**: If set to `true`, embedded font bitmap loading is disabled (bitmap-only and color fonts ignore this property).
- **font_italic**: If set to `true`, italic or oblique font is preferred.
- **font_names**: Array of font family names to search, first matching font found is used.
- **font_stretch**: Preferred font stretch amount, compared to a normal width. A percentage value between `50%` and `200%`.
- **font_weight**: Preferred weight (boldness) of the font. A value in the `100...999` range, normal font weight is `400`, bold font weight is `700`.
- **force_autohinter**: If set to `true`, auto-hinting is supported and preferred over font built-in hinting.
- **generate_mipmaps**: If set to `true`, generate mipmaps for the font textures.
- **hinting**: Font hinting mode.
- **keep_rounding_remainders**: If set to `true`, when aligning glyphs to the pixel boundaries rounding remainders are accumulated to ensure more uniform glyph distribution. This setting has no effect if subpixel positioning is enabled.
- **modulate_color_glyphs**: If set to `true`, color modulation is applied when drawing colored glyphs, otherwise it's applied to the monochrome glyphs only.
- **msdf_pixel_range**: The width of the range around the shape between the minimum and maximum representable signed distance. If using font outlines, `msdf_pixel_range` must be set to at least *twice* the size of the largest font outline. The default `msdf_pixel_range` value of `16` allows outline sizes up to `8` to look correct.
- **msdf_size**: Source font size used to generate MSDF textures. Higher values allow for more precision, but are slower to render and require more memory. Only increase this value if you notice a visible lack of precision in glyph rendering.
- **multichannel_signed_distance_field**: If set to `true`, glyphs of all sizes are rendered using single multichannel signed distance field generated from the dynamic font vector data.
- **oversampling**: If set to a positive value, overrides the oversampling factor of the viewport this font is used in. See `Viewport.oversampling`. This value doesn't override the [code skip-lint]oversampling[/code] parameter of [code skip-lint]draw_*[/code] methods.
- **subpixel_positioning**: Font glyph subpixel positioning mode. Subpixel positioning provides shaper text and better kerning for smaller font sizes, at the cost of memory usage and font rasterization speed. Use `TextServer.SUBPIXEL_POSITIONING_AUTO` to automatically enable it based on the font size.

