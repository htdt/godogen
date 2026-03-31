## CharFXTransform <- RefCounted

By setting various properties on this object, you can control how individual characters will be displayed in a RichTextEffect.

**Props:**
- color: Color = Color(0, 0, 0, 1)
- elapsed_time: float = 0.0
- env: Dictionary = {}
- font: RID = RID()
- glyph_count: int = 0
- glyph_flags: int = 0
- glyph_index: int = 0
- offset: Vector2 = Vector2(0, 0)
- outline: bool = false
- range: Vector2i = Vector2i(0, 0)
- relative_index: int = 0
- transform: Transform2D = Transform2D(1, 0, 0, 1, 0, 0)
- visible: bool = true

- **color**: The color the character will be drawn with.
- **elapsed_time**: The time elapsed since the RichTextLabel was added to the scene tree (in seconds). Time stops when the RichTextLabel is paused (see `Node.process_mode`). Resets when the text in the RichTextLabel is changed. **Note:** Time still passes while the RichTextLabel is hidden.
- **env**: Contains the arguments passed in the opening BBCode tag. By default, arguments are strings; if their contents match a type such as [bool], [int] or [float], they will be converted automatically. Color codes in the form `#rrggbb` or `#rgb` will be converted to an opaque Color. String arguments may not contain spaces, even if they're quoted. If present, quotes will also be present in the final string. For example, the opening BBCode tag `[example foo=hello bar=true baz=42 color=#ffffff]` will map to the following Dictionary:
- **font**: TextServer RID of the font used to render glyph, this value can be used with `TextServer.font_*` methods to retrieve font information. **Note:** Read-only. Setting this property won't affect drawing.
- **glyph_count**: Number of glyphs in the grapheme cluster. This value is set in the first glyph of a cluster. **Note:** Read-only. Setting this property won't affect drawing.
- **glyph_flags**: Glyph flags. See `TextServer.GraphemeFlag` for more info. **Note:** Read-only. Setting this property won't affect drawing.
- **glyph_index**: Glyph index specific to the `font`. If you want to replace this glyph, use `TextServer.font_get_glyph_index` with `font` to get a new glyph index for a single character.
- **offset**: The position offset the character will be drawn with (in pixels).
- **outline**: If `true`, FX transform is called for outline drawing. **Note:** Read-only. Setting this property won't affect drawing.
- **range**: Absolute character range in the string, corresponding to the glyph. **Note:** Read-only. Setting this property won't affect drawing.
- **relative_index**: The character offset of the glyph, relative to the current RichTextEffect custom block. **Note:** Read-only. Setting this property won't affect drawing.
- **transform**: The current transform of the current glyph. It can be overridden (for example, by driving the position and rotation from a curve). You can also alter the existing value to apply transforms on top of other effects.
- **visible**: If `true`, the character will be drawn. If `false`, the character will be hidden. Characters around hidden characters will reflow to take the space of hidden characters. If this is not desired, set their `color` to `Color(1, 1, 1, 0)` instead.

