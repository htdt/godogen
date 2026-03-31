## CurveTexture <- Texture2D

A 1D texture where pixel brightness corresponds to points on a unit Curve resource, either in grayscale or in red. This visual representation simplifies the task of saving curves as image files. If you need to store up to 3 curves within a single texture, use CurveXYZTexture instead. See also GradientTexture1D and GradientTexture2D.

**Props:**
- curve: Curve
- resource_local_to_scene: bool = false
- texture_mode: int (CurveTexture.TextureMode) = 0
- width: int = 256

- **curve**: The Curve that is rendered onto the texture. Should be a unit Curve.
- **texture_mode**: The format the texture should be generated with. When passing a CurveTexture as an input to a Shader, this may need to be adjusted.
- **width**: The width of the texture (in pixels). Higher values make it possible to represent high-frequency data better (such as sudden direction changes), at the cost of increased generation time and memory usage.

**Enums:**
**TextureMode:** TEXTURE_MODE_RGB=0, TEXTURE_MODE_RED=1
  - TEXTURE_MODE_RGB: Store the curve equally across the red, green and blue channels. This uses more video memory, but is more compatible with shaders that only read the green and blue values.
  - TEXTURE_MODE_RED: Store the curve only in the red channel. This saves video memory, but some custom shaders may not be able to work with this.

