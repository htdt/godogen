## VisualShaderNodeTextureParameter <- VisualShaderNodeParameter

Performs a lookup operation on the texture provided as a uniform for the shader.

**Props:**
- color_default: int (VisualShaderNodeTextureParameter.ColorDefault) = 0
- texture_filter: int (VisualShaderNodeTextureParameter.TextureFilter) = 0
- texture_repeat: int (VisualShaderNodeTextureParameter.TextureRepeat) = 0
- texture_source: int (VisualShaderNodeTextureParameter.TextureSource) = 0
- texture_type: int (VisualShaderNodeTextureParameter.TextureType) = 0

- **color_default**: Sets the default color if no texture is assigned to the uniform.
- **texture_filter**: Sets the texture filtering mode.
- **texture_repeat**: Sets the texture repeating mode.
- **texture_source**: Sets the texture source mode. Used for reading from the screen, depth, or normal_roughness texture.
- **texture_type**: Defines the type of data provided by the source texture.

**Enums:**
**TextureType:** TYPE_DATA=0, TYPE_COLOR=1, TYPE_NORMAL_MAP=2, TYPE_ANISOTROPY=3, TYPE_MAX=4
  - TYPE_DATA: No hints are added to the uniform declaration.
  - TYPE_COLOR: Adds `source_color` as hint to the uniform declaration for proper conversion from nonlinear sRGB encoding to linear encoding.
  - TYPE_NORMAL_MAP: Adds `hint_normal` as hint to the uniform declaration, which internally converts the texture for proper usage as normal map.
  - TYPE_ANISOTROPY: Adds `hint_anisotropy` as hint to the uniform declaration to use for a flowmap.
  - TYPE_MAX: Represents the size of the `TextureType` enum.
**ColorDefault:** COLOR_DEFAULT_WHITE=0, COLOR_DEFAULT_BLACK=1, COLOR_DEFAULT_TRANSPARENT=2, COLOR_DEFAULT_MAX=3
  - COLOR_DEFAULT_WHITE: Defaults to fully opaque white color.
  - COLOR_DEFAULT_BLACK: Defaults to fully opaque black color.
  - COLOR_DEFAULT_TRANSPARENT: Defaults to fully transparent black color.
  - COLOR_DEFAULT_MAX: Represents the size of the `ColorDefault` enum.
**TextureFilter:** FILTER_DEFAULT=0, FILTER_NEAREST=1, FILTER_LINEAR=2, FILTER_NEAREST_MIPMAP=3, FILTER_LINEAR_MIPMAP=4, FILTER_NEAREST_MIPMAP_ANISOTROPIC=5, FILTER_LINEAR_MIPMAP_ANISOTROPIC=6, FILTER_MAX=7
  - FILTER_DEFAULT: Sample the texture using the filter determined by the node this shader is attached to.
  - FILTER_NEAREST: The texture filter reads from the nearest pixel only. This makes the texture look pixelated from up close, and grainy from a distance (due to mipmaps not being sampled).
  - FILTER_LINEAR: The texture filter blends between the nearest 4 pixels. This makes the texture look smooth from up close, and grainy from a distance (due to mipmaps not being sampled).
  - FILTER_NEAREST_MIPMAP: The texture filter reads from the nearest pixel and blends between the nearest 2 mipmaps (or uses the nearest mipmap if `ProjectSettings.rendering/textures/default_filters/use_nearest_mipmap_filter` is `true`). This makes the texture look pixelated from up close, and smooth from a distance. Use this for non-pixel art textures that may be viewed at a low scale (e.g. due to Camera2D zoom or sprite scaling), as mipmaps are important to smooth out pixels that are smaller than on-screen pixels.
  - FILTER_LINEAR_MIPMAP: The texture filter blends between the nearest 4 pixels and between the nearest 2 mipmaps (or uses the nearest mipmap if `ProjectSettings.rendering/textures/default_filters/use_nearest_mipmap_filter` is `true`). This makes the texture look smooth from up close, and smooth from a distance. Use this for non-pixel art textures that may be viewed at a low scale (e.g. due to Camera2D zoom or sprite scaling), as mipmaps are important to smooth out pixels that are smaller than on-screen pixels.
  - FILTER_NEAREST_MIPMAP_ANISOTROPIC: The texture filter reads from the nearest pixel and blends between 2 mipmaps (or uses the nearest mipmap if `ProjectSettings.rendering/textures/default_filters/use_nearest_mipmap_filter` is `true`) based on the angle between the surface and the camera view. This makes the texture look pixelated from up close, and smooth from a distance. Anisotropic filtering improves texture quality on surfaces that are almost in line with the camera, but is slightly slower. The anisotropic filtering level can be changed by adjusting `ProjectSettings.rendering/textures/default_filters/anisotropic_filtering_level`. **Note:** This texture filter is rarely useful in 2D projects. `FILTER_NEAREST_MIPMAP` is usually more appropriate in this case.
  - FILTER_LINEAR_MIPMAP_ANISOTROPIC: The texture filter blends between the nearest 4 pixels and blends between 2 mipmaps (or uses the nearest mipmap if `ProjectSettings.rendering/textures/default_filters/use_nearest_mipmap_filter` is `true`) based on the angle between the surface and the camera view. This makes the texture look smooth from up close, and smooth from a distance. Anisotropic filtering improves texture quality on surfaces that are almost in line with the camera, but is slightly slower. The anisotropic filtering level can be changed by adjusting `ProjectSettings.rendering/textures/default_filters/anisotropic_filtering_level`. **Note:** This texture filter is rarely useful in 2D projects. `FILTER_LINEAR_MIPMAP` is usually more appropriate in this case.
  - FILTER_MAX: Represents the size of the `TextureFilter` enum.
**TextureRepeat:** REPEAT_DEFAULT=0, REPEAT_ENABLED=1, REPEAT_DISABLED=2, REPEAT_MAX=3
  - REPEAT_DEFAULT: Sample the texture using the repeat mode determined by the node this shader is attached to.
  - REPEAT_ENABLED: Texture will repeat normally.
  - REPEAT_DISABLED: Texture will not repeat.
  - REPEAT_MAX: Represents the size of the `TextureRepeat` enum.
**TextureSource:** SOURCE_NONE=0, SOURCE_SCREEN=1, SOURCE_DEPTH=2, SOURCE_NORMAL_ROUGHNESS=3, SOURCE_MAX=4
  - SOURCE_NONE: The texture source is not specified in the shader.
  - SOURCE_SCREEN: The texture source is the screen texture which captures all opaque objects drawn this frame.
  - SOURCE_DEPTH: The texture source is the depth texture from the depth prepass.
  - SOURCE_NORMAL_ROUGHNESS: The texture source is the normal-roughness buffer from the depth prepass.
  - SOURCE_MAX: Represents the size of the `TextureSource` enum.

