## DrawableTexture2D <- Texture2D

A 2D texture that can be modified via blit calls, copying from a target texture to itself. Primarily intended to be managed in code, a user must call `setup` to initialize the state before drawing. Each `blit_rect` call takes at least a rectangle, the area to draw to, and another texture, what to be drawn. The draw calls use a Texture_Blit Shader to process and calculate the result, pixel by pixel. Users can supply their own ShaderMaterial with custom Texture_Blit shaders for more complex behaviors.

**Props:**
- resource_local_to_scene: bool = false


**Methods:**
- blit_rect(rect: Rect2i, source: Texture2D, modulate: Color = Color(1, 1, 1, 1), mipmap: int = 0, material: Material = null) - Draws to given `rect` on this texture by copying from the given `source`. A `modulate` color can be passed in for the shader to use, but defaults to White. The `mipmap` value can specify a draw to a lower mipmap level. The `material` parameter can take a ShaderMaterial with a TextureBlit Shader for custom drawing behavior.
- blit_rect_multi(rect: Rect2i, sources: Texture2D[], extra_targets: DrawableTexture2D[], modulate: Color = Color(1, 1, 1, 1), mipmap: int = 0, material: Material = null) - Draws to the given `rect` on this texture, as well as on up to 3 DrawableTexture `extra_targets`. All `extra_targets` must be the same size and DrawableFormat as the original target, otherwise the Shader may fail. Expects up to 4 Texture `sources`, but will replace missing `sources` with default Black Textures.
- generate_mipmaps() - Re-calculates the mipmaps for this texture on demand.
- get_use_mipmaps() -> bool - Returns `true` if mipmaps are set to be used on this DrawableTexture.
- set_format(format: int) - Sets the format of this DrawableTexture.
- set_height(height: int) - Sets the height of this DrawableTexture.
- set_use_mipmaps(mipmaps: bool) - Sets if mipmaps should be used on this DrawableTexture.
- set_width(width: int) - Sets the width of this DrawableTexture.
- setup(width: int, height: int, format: int, color: Color = Color(1, 1, 1, 1), use_mipmaps: bool = false) - Initializes the DrawableTexture to a White texture of the given `width`, `height`, and `format`.

**Enums:**
**DrawableFormat:** DRAWABLE_FORMAT_RGBA8=0, DRAWABLE_FORMAT_RGBA8_SRGB=1, DRAWABLE_FORMAT_RGBAH=2, DRAWABLE_FORMAT_RGBAF=3
  - DRAWABLE_FORMAT_RGBA8: OpenGL texture format RGBA with four components, each with a bitdepth of 8.
  - DRAWABLE_FORMAT_RGBA8_SRGB: OpenGL texture format RGBA with four components, each with a bitdepth of 8. When drawn to, an sRGB to linear color space conversion is performed.
  - DRAWABLE_FORMAT_RGBAH: OpenGL texture format GL_RGBA16F where there are four components, each a 16-bit "half-precision" floating-point value.
  - DRAWABLE_FORMAT_RGBAF: OpenGL texture format GL_RGBA32F where there are four components, each a 32-bit floating-point value.

