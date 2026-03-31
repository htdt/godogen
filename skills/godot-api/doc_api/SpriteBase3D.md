## SpriteBase3D <- GeometryInstance3D

A node that displays 2D texture information in a 3D environment. See also Sprite3D where many other properties are defined.

**Props:**
- alpha_antialiasing_edge: float = 0.0
- alpha_antialiasing_mode: int (BaseMaterial3D.AlphaAntiAliasing) = 0
- alpha_cut: int (SpriteBase3D.AlphaCutMode) = 0
- alpha_hash_scale: float = 1.0
- alpha_scissor_threshold: float = 0.5
- axis: int (Vector3.Axis) = 2
- billboard: int (BaseMaterial3D.BillboardMode) = 0
- centered: bool = true
- double_sided: bool = true
- fixed_size: bool = false
- flip_h: bool = false
- flip_v: bool = false
- modulate: Color = Color(1, 1, 1, 1)
- no_depth_test: bool = false
- offset: Vector2 = Vector2(0, 0)
- pixel_size: float = 0.01
- render_priority: int = 0
- shaded: bool = false
- texture_filter: int (BaseMaterial3D.TextureFilter) = 3
- transparent: bool = true

- **alpha_antialiasing_edge**: Threshold at which antialiasing will be applied on the alpha channel.
- **alpha_antialiasing_mode**: The type of alpha antialiasing to apply.
- **alpha_cut**: The alpha cutting mode to use for the sprite.
- **alpha_hash_scale**: The hashing scale for Alpha Hash. Recommended values between `0` and `2`.
- **alpha_scissor_threshold**: Threshold at which the alpha scissor will discard values.
- **axis**: The direction in which the front of the texture faces.
- **billboard**: The billboard mode to use for the sprite. **Note:** When billboarding is enabled and the material also casts shadows, billboards will face **the** camera in the scene when rendering shadows. In scenes with multiple cameras, the intended shadow cannot be determined and this will result in undefined behavior. See for details.
- **centered**: If `true`, texture will be centered.
- **double_sided**: If `true`, texture can be seen from the back as well, if `false`, it is invisible when looking at it from behind.
- **fixed_size**: If `true`, the texture is rendered at the same size regardless of distance. The texture's size on screen is the same as if the camera was `1.0` units away from the texture's origin, regardless of the actual distance from the camera. The Camera3D's field of view (or `Camera3D.size` when in orthogonal/frustum mode) still affects the size the sprite is drawn at.
- **flip_h**: If `true`, texture is flipped horizontally.
- **flip_v**: If `true`, texture is flipped vertically.
- **modulate**: A color value used to *multiply* the texture's colors. Can be used for mood-coloring or to simulate the color of ambient light. **Note:** Unlike `CanvasItem.modulate` for 2D, colors with values above `1.0` (overbright) are not supported. **Note:** If a `GeometryInstance3D.material_override` is defined on the SpriteBase3D, the material override must be configured to take vertex colors into account for albedo. Otherwise, the color defined in `modulate` will be ignored. For a BaseMaterial3D, `BaseMaterial3D.vertex_color_use_as_albedo` must be `true`. For a ShaderMaterial, `ALBEDO *= COLOR.rgb;` must be inserted in the shader's `fragment()` function.
- **no_depth_test**: If `true`, depth testing is disabled and the object will be drawn in render order.
- **offset**: The texture's drawing offset. **Note:** When you increase `offset`.y in Sprite3D, the sprite moves upward in world space (i.e., +Y is up).
- **pixel_size**: The size of one pixel's width on the sprite to scale it in 3D.
- **render_priority**: Sets the render priority for the sprite. Higher priority objects will be sorted in front of lower priority objects. **Note:** This only applies if `alpha_cut` is set to `ALPHA_CUT_DISABLED` (default value). **Note:** This only applies to sorting of transparent objects. This will not impact how transparent objects are sorted relative to opaque objects. This is because opaque objects are not sorted, while transparent objects are sorted from back to front (subject to priority).
- **shaded**: If `true`, the Light3D in the Environment has effects on the sprite.
- **texture_filter**: Filter flags for the texture. **Note:** Linear filtering may cause artifacts around the edges, which are especially noticeable on opaque textures. To prevent this, use textures with transparent or identical colors around the edges.
- **transparent**: If `true`, the texture's transparency and the opacity are used to make those parts of the sprite invisible.

**Methods:**
- generate_triangle_mesh() -> TriangleMesh - Returns a TriangleMesh with the sprite's vertices following its current configuration (such as its `axis` and `pixel_size`).
- get_draw_flag(flag: int) -> bool - Returns the value of the specified flag.
- get_item_rect() -> Rect2 - Returns the rectangle representing this sprite.
- set_draw_flag(flag: int, enabled: bool) - If `true`, the specified flag will be enabled.

**Enums:**
**DrawFlags:** FLAG_TRANSPARENT=0, FLAG_SHADED=1, FLAG_DOUBLE_SIDED=2, FLAG_DISABLE_DEPTH_TEST=3, FLAG_FIXED_SIZE=4, FLAG_MAX=5
  - FLAG_TRANSPARENT: If set, the texture's transparency and the opacity are used to make those parts of the sprite invisible.
  - FLAG_SHADED: If set, lights in the environment affect the sprite.
  - FLAG_DOUBLE_SIDED: If set, texture can be seen from the back as well. If not, the texture is invisible when looking at it from behind.
  - FLAG_DISABLE_DEPTH_TEST: Disables the depth test, so this object is drawn on top of all others. However, objects drawn after it in the draw order may cover it.
  - FLAG_FIXED_SIZE: Label is scaled by depth so that it always appears the same size on screen.
  - FLAG_MAX: Represents the size of the `DrawFlags` enum.
**AlphaCutMode:** ALPHA_CUT_DISABLED=0, ALPHA_CUT_DISCARD=1, ALPHA_CUT_OPAQUE_PREPASS=2, ALPHA_CUT_HASH=3
  - ALPHA_CUT_DISABLED: This mode performs standard alpha blending. It can display translucent areas, but transparency sorting issues may be visible when multiple transparent materials are overlapping.
  - ALPHA_CUT_DISCARD: This mode only allows fully transparent or fully opaque pixels. Harsh edges will be visible unless some form of screen-space antialiasing is enabled (see `ProjectSettings.rendering/anti_aliasing/quality/screen_space_aa`). On the bright side, this mode doesn't suffer from transparency sorting issues when multiple transparent materials are overlapping. This mode is also known as *alpha testing* or *1-bit transparency*.
  - ALPHA_CUT_OPAQUE_PREPASS: This mode draws fully opaque pixels in the depth prepass. This is slower than `ALPHA_CUT_DISABLED` or `ALPHA_CUT_DISCARD`, but it allows displaying translucent areas and smooth edges while using proper sorting.
  - ALPHA_CUT_HASH: This mode draws cuts off all values below a spatially-deterministic threshold, the rest will remain opaque.

