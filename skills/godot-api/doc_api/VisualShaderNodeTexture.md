## VisualShaderNodeTexture <- VisualShaderNode

Performs a lookup operation on the provided texture, with support for multiple texture sources to choose from.

**Props:**
- source: int (VisualShaderNodeTexture.Source) = 0
- texture: Texture2D
- texture_type: int (VisualShaderNodeTexture.TextureType) = 0

- **source**: Determines the source for the lookup.
- **texture**: The source texture, if needed for the selected `source`.
- **texture_type**: Specifies the type of the texture if `source` is set to `SOURCE_TEXTURE`.

**Enums:**
**Source:** SOURCE_TEXTURE=0, SOURCE_SCREEN=1, SOURCE_2D_TEXTURE=2, SOURCE_2D_NORMAL=3, SOURCE_DEPTH=4, SOURCE_PORT=5, SOURCE_3D_NORMAL=6, SOURCE_ROUGHNESS=7, SOURCE_MAX=8
  - SOURCE_TEXTURE: Use the texture given as an argument for this function.
  - SOURCE_SCREEN: Use the current viewport's texture as the source.
  - SOURCE_2D_TEXTURE: Use the texture from this shader's texture built-in (e.g. a texture of a Sprite2D).
  - SOURCE_2D_NORMAL: Use the texture from this shader's normal map built-in.
  - SOURCE_DEPTH: Use the depth texture captured during the depth prepass. Only available when the depth prepass is used (i.e. in spatial shaders and in the forward_plus or gl_compatibility renderers).
  - SOURCE_PORT: Use the texture provided in the input port for this function.
  - SOURCE_3D_NORMAL: Use the normal buffer captured during the depth prepass. Only available when the normal-roughness buffer is available (i.e. in spatial shaders and in the forward_plus renderer).
  - SOURCE_ROUGHNESS: Use the roughness buffer captured during the depth prepass. Only available when the normal-roughness buffer is available (i.e. in spatial shaders and in the forward_plus renderer).
  - SOURCE_MAX: Represents the size of the `Source` enum.
**TextureType:** TYPE_DATA=0, TYPE_COLOR=1, TYPE_NORMAL_MAP=2, TYPE_MAX=3
  - TYPE_DATA: No hints are added to the uniform declaration.
  - TYPE_COLOR: Adds `source_color` as hint to the uniform declaration for proper conversion from nonlinear sRGB encoding to linear encoding.
  - TYPE_NORMAL_MAP: Adds `hint_normal` as hint to the uniform declaration, which internally converts the texture for proper usage as normal map.
  - TYPE_MAX: Represents the size of the `TextureType` enum.

