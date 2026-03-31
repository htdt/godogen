## TextMesh <- PrimitiveMesh

Generate a PrimitiveMesh from the text. TextMesh can be generated only when using dynamic fonts with vector glyph contours. Bitmap fonts (including bitmap data in the TrueType/OpenType containers, like color emoji fonts) are not supported. The UV layout is arranged in 4 horizontal strips, top to bottom: 40% of the height for the front face, 40% for the back face, 10% for the outer edges and 10% for the inner edges.

**Props:**
- autowrap_mode: int (TextServer.AutowrapMode) = 0
- curve_step: float = 0.5
- depth: float = 0.05
- font: Font
- font_size: int = 16
- horizontal_alignment: int (HorizontalAlignment) = 1
- justification_flags: int (TextServer.JustificationFlag) = 163
- language: String = ""
- line_spacing: float = 0.0
- offset: Vector2 = Vector2(0, 0)
- pixel_size: float = 0.01
- structured_text_bidi_override: int (TextServer.StructuredTextParser) = 0
- structured_text_bidi_override_options: Array = []
- text: String = ""
- text_direction: int (TextServer.Direction) = 0
- uppercase: bool = false
- vertical_alignment: int (VerticalAlignment) = 1
- width: float = 500.0

- **autowrap_mode**: If set to something other than `TextServer.AUTOWRAP_OFF`, the text gets wrapped inside the node's bounding rectangle. If you resize the node, it will change its height automatically to show all the text.
- **curve_step**: Step (in pixels) used to approximate Bézier curves. Lower values result in smoother curves, but is slower to generate and render. Consider adjusting this according to the font size and the typical viewing distance. **Note:** Changing this property will regenerate the mesh, which is a slow operation, especially with large font sizes and long texts.
- **depth**: Depths of the mesh, if set to `0.0` only front surface, is generated, and UV layout is changed to use full texture for the front face only.
- **font**: Font configuration used to display text.
- **font_size**: Font size of the TextMesh's text. This property works in tandem with `pixel_size`. Higher values will result in a more detailed font, regardless of `curve_step` and `pixel_size`. Consider keeping this value below 63 (inclusive) for good performance, and adjust `pixel_size` as needed to enlarge text. **Note:** Changing this property will regenerate the mesh, which is a slow operation, especially with large font sizes and long texts. To change the text's size in real-time efficiently, change the node's `Node3D.scale` instead.
- **horizontal_alignment**: Controls the text's horizontal alignment. Supports left, center, right, and fill (also known as justify).
- **justification_flags**: Line fill alignment rules.
- **language**: Language code used for line-breaking and text shaping algorithms. If left empty, the current locale is used instead.
- **line_spacing**: Additional vertical spacing between lines (in pixels), spacing is added to line descent. This value can be negative.
- **offset**: The text drawing offset (in pixels). **Note:** Changing this property will regenerate the mesh, which is a slow operation. To change the text's position in real-time efficiently, change the node's `Node3D.position` instead.
- **pixel_size**: The size of one pixel's width on the text to scale it in 3D. This property works in tandem with `font_size`. **Note:** Changing this property will regenerate the mesh, which is a slow operation, especially with large font sizes and long texts. To change the text's size in real-time efficiently, change the node's `Node3D.scale` instead.
- **structured_text_bidi_override**: Set BiDi algorithm override for the structured text.
- **structured_text_bidi_override_options**: Set additional options for BiDi override.
- **text**: The text to generate mesh from. **Note:** Due to being a Resource, it doesn't follow the rules of `Node.auto_translate_mode`. If disabling translation is desired, it should be done manually with `Object.set_message_translation`.
- **text_direction**: Base text writing direction.
- **uppercase**: If `true`, all the text displays as UPPERCASE.
- **vertical_alignment**: Controls the text's vertical alignment. Supports top, center, and bottom.
- **width**: Text width (in pixels), used for fill alignment.

