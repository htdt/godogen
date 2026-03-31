## VisualShaderNodeCubemap <- VisualShaderNode

Translated to `texture(cubemap, vec3)` in the shader language. Returns a color vector and alpha channel as scalar.

**Props:**
- cube_map: TextureLayered
- source: int (VisualShaderNodeCubemap.Source) = 0
- texture_type: int (VisualShaderNodeCubemap.TextureType) = 0

- **cube_map**: The Cubemap texture to sample when using `SOURCE_TEXTURE` as `source`.
- **source**: Defines which source should be used for the sampling.
- **texture_type**: Defines the type of data provided by the source texture.

**Enums:**
**Source:** SOURCE_TEXTURE=0, SOURCE_PORT=1, SOURCE_MAX=2
  - SOURCE_TEXTURE: Use the Cubemap set via `cube_map`. If this is set to `source`, the `samplerCube` port is ignored.
  - SOURCE_PORT: Use the Cubemap sampler reference passed via the `samplerCube` port. If this is set to `source`, the `cube_map` texture is ignored.
  - SOURCE_MAX: Represents the size of the `Source` enum.
**TextureType:** TYPE_DATA=0, TYPE_COLOR=1, TYPE_NORMAL_MAP=2, TYPE_MAX=3
  - TYPE_DATA: No hints are added to the uniform declaration.
  - TYPE_COLOR: Adds `source_color` as hint to the uniform declaration for proper conversion from nonlinear sRGB encoding to linear encoding.
  - TYPE_NORMAL_MAP: Adds `hint_normal` as hint to the uniform declaration, which internally converts the texture for proper usage as normal map.
  - TYPE_MAX: Represents the size of the `TextureType` enum.

