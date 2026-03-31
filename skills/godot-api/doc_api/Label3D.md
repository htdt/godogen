## Label3D <- GeometryInstance3D

A node for displaying plain text in 3D space. By adjusting various properties of this node, you can configure things such as the text's appearance and whether it always faces the camera.

**Props:**
- alpha_antialiasing_edge: float = 0.0
- alpha_antialiasing_mode: int (BaseMaterial3D.AlphaAntiAliasing) = 0
- alpha_cut: int (Label3D.AlphaCutMode) = 0
- alpha_hash_scale: float = 1.0
- alpha_scissor_threshold: float = 0.5
- autowrap_mode: int (TextServer.AutowrapMode) = 0
- autowrap_trim_flags: int (TextServer.LineBreakFlag) = 192
- billboard: int (BaseMaterial3D.BillboardMode) = 0
- cast_shadow: int (GeometryInstance3D.ShadowCastingSetting) = 0
- double_sided: bool = true
- fixed_size: bool = false
- font: Font
- font_size: int = 32
- gi_mode: int (GeometryInstance3D.GIMode) = 0
- horizontal_alignment: int (HorizontalAlignment) = 1
- justification_flags: int (TextServer.JustificationFlag) = 163
- language: String = ""
- line_spacing: float = 0.0
- modulate: Color = Color(1, 1, 1, 1)
- no_depth_test: bool = false
- offset: Vector2 = Vector2(0, 0)
- outline_modulate: Color = Color(0, 0, 0, 1)
- outline_render_priority: int = -1
- outline_size: int = 12
- pixel_size: float = 0.005
- render_priority: int = 0
- shaded: bool = false
- structured_text_bidi_override: int (TextServer.StructuredTextParser) = 0
- structured_text_bidi_override_options: Array = []
- text: String = ""
- text_direction: int (TextServer.Direction) = 0
- texture_filter: int (BaseMaterial3D.TextureFilter) = 3
- uppercase: bool = false
- vertical_alignment: int (VerticalAlignment) = 1
- width: float = 500.0

- **alpha_antialiasing_edge**: Threshold at which antialiasing will be applied on the alpha channel.
- **alpha_antialiasing_mode**: The type of alpha antialiasing to apply.
- **alpha_cut**: The alpha cutting mode to use for the sprite.
- **alpha_hash_scale**: The hashing scale for Alpha Hash. Recommended values between `0` and `2`.
- **alpha_scissor_threshold**: Threshold at which the alpha scissor will discard values.
- **autowrap_mode**: If set to something other than `TextServer.AUTOWRAP_OFF`, the text gets wrapped inside the node's bounding rectangle. If you resize the node, it will change its height automatically to show all the text.
- **autowrap_trim_flags**: Autowrap space trimming flags. See `TextServer.BREAK_TRIM_START_EDGE_SPACES` and `TextServer.BREAK_TRIM_END_EDGE_SPACES` for more info.
- **billboard**: The billboard mode to use for the label.
- **double_sided**: If `true`, text can be seen from the back as well, if `false`, it is invisible when looking at it from behind.
- **fixed_size**: If `true`, the label is rendered at the same size regardless of distance. The label's size on screen is the same as if the camera was `1.0` units away from the label's origin, regardless of the actual distance from the camera. The Camera3D's field of view (or `Camera3D.size` when in orthogonal/frustum mode) still affects the size the label is drawn at.
- **font**: Font configuration used to display text.
- **font_size**: Font size of the Label3D's text. To make the font look more detailed when up close, increase `font_size` while decreasing `pixel_size` at the same time. Higher font sizes require more time to render new characters, which can cause stuttering during gameplay.
- **horizontal_alignment**: Controls the text's horizontal alignment. Supports left, center, right, and fill (also known as justify).
- **justification_flags**: Line fill alignment rules.
- **language**: Language code used for line-breaking and text shaping algorithms. If left empty, the current locale is used instead.
- **line_spacing**: Additional vertical spacing between lines (in pixels), spacing is added to line descent. This value can be negative.
- **modulate**: Text Color of the Label3D.
- **no_depth_test**: If `true`, depth testing is disabled and the object will be drawn in render order.
- **offset**: The text drawing offset (in pixels).
- **outline_modulate**: The tint of text outline.
- **outline_render_priority**: Sets the render priority for the text outline. Higher priority objects will be sorted in front of lower priority objects. **Note:** This only applies if `alpha_cut` is set to `ALPHA_CUT_DISABLED` (default value). **Note:** This only applies to sorting of transparent objects. This will not impact how transparent objects are sorted relative to opaque objects. This is because opaque objects are not sorted, while transparent objects are sorted from back to front (subject to priority).
- **outline_size**: Text outline size.
- **pixel_size**: The size of one pixel's width on the label to scale it in 3D. To make the font look more detailed when up close, increase `font_size` while decreasing `pixel_size` at the same time.
- **render_priority**: Sets the render priority for the text. Higher priority objects will be sorted in front of lower priority objects. **Note:** This only applies if `alpha_cut` is set to `ALPHA_CUT_DISABLED` (default value). **Note:** This only applies to sorting of transparent objects. This will not impact how transparent objects are sorted relative to opaque objects. This is because opaque objects are not sorted, while transparent objects are sorted from back to front (subject to priority).
- **shaded**: If `true`, the Light3D in the Environment has effects on the label.
- **structured_text_bidi_override**: Set BiDi algorithm override for the structured text.
- **structured_text_bidi_override_options**: Set additional options for BiDi override.
- **text**: The text to display on screen.
- **text_direction**: Base text writing direction.
- **texture_filter**: Filter flags for the texture.
- **uppercase**: If `true`, all the text displays as UPPERCASE.
- **vertical_alignment**: Controls the text's vertical alignment. Supports top, center, and bottom.
- **width**: Text width (in pixels), used for autowrap and fill alignment.

**Methods:**
- generate_triangle_mesh() -> TriangleMesh - Returns a TriangleMesh with the label's vertices following its current configuration (such as its `pixel_size`).
- get_draw_flag(flag: int) -> bool - Returns the value of the specified flag.
- set_draw_flag(flag: int, enabled: bool) - If `true`, the specified `flag` will be enabled.

**Enums:**
**DrawFlags:** FLAG_SHADED=0, FLAG_DOUBLE_SIDED=1, FLAG_DISABLE_DEPTH_TEST=2, FLAG_FIXED_SIZE=3, FLAG_MAX=4
  - FLAG_SHADED: If set, lights in the environment affect the label.
  - FLAG_DOUBLE_SIDED: If set, text can be seen from the back as well. If not, the text is invisible when looking at it from behind.
  - FLAG_DISABLE_DEPTH_TEST: Disables the depth test, so this object is drawn on top of all others. However, objects drawn after it in the draw order may cover it.
  - FLAG_FIXED_SIZE: Label is scaled by depth so that it always appears the same size on screen.
  - FLAG_MAX: Represents the size of the `DrawFlags` enum.
**AlphaCutMode:** ALPHA_CUT_DISABLED=0, ALPHA_CUT_DISCARD=1, ALPHA_CUT_OPAQUE_PREPASS=2, ALPHA_CUT_HASH=3
  - ALPHA_CUT_DISABLED: This mode performs standard alpha blending. It can display translucent areas, but transparency sorting issues may be visible when multiple transparent materials are overlapping. `GeometryInstance3D.cast_shadow` has no effect when this transparency mode is used; the Label3D will never cast shadows.
  - ALPHA_CUT_DISCARD: This mode only allows fully transparent or fully opaque pixels. Harsh edges will be visible unless some form of screen-space antialiasing is enabled (see `ProjectSettings.rendering/anti_aliasing/quality/screen_space_aa`). This mode is also known as *alpha testing* or *1-bit transparency*. **Note:** This mode might have issues with anti-aliased fonts and outlines, try adjusting `alpha_scissor_threshold` or using MSDF font. **Note:** When using text with overlapping glyphs (e.g., cursive scripts), this mode might have transparency sorting issues between the main text and the outline.
  - ALPHA_CUT_OPAQUE_PREPASS: This mode draws fully opaque pixels in the depth prepass. This is slower than `ALPHA_CUT_DISABLED` or `ALPHA_CUT_DISCARD`, but it allows displaying translucent areas and smooth edges while using proper sorting. **Note:** When using text with overlapping glyphs (e.g., cursive scripts), this mode might have transparency sorting issues between the main text and the outline.
  - ALPHA_CUT_HASH: This mode draws cuts off all values below a spatially-deterministic threshold, the rest will remain opaque.

