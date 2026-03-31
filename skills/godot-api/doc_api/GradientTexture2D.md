## GradientTexture2D <- Texture2D

A 2D texture that obtains colors from a Gradient to fill the texture data. This texture is able to transform a color transition into different patterns such as a linear or a radial gradient. The texture is filled by interpolating colors starting from `fill_from` to `fill_to` offsets by default, but the gradient fill can be repeated to cover the entire texture. The gradient is sampled individually for each pixel so it does not necessarily represent an exact copy of the gradient (see `width` and `height`). See also GradientTexture1D, CurveTexture and CurveXYZTexture.

**Props:**
- fill: int (GradientTexture2D.Fill) = 0
- fill_from: Vector2 = Vector2(0, 0)
- fill_to: Vector2 = Vector2(1, 0)
- gradient: Gradient
- height: int = 64
- repeat: int (GradientTexture2D.Repeat) = 0
- resource_local_to_scene: bool = false
- use_hdr: bool = false
- width: int = 64

- **fill**: The gradient's fill type.
- **fill_from**: The initial offset used to fill the texture specified in UV coordinates.
- **fill_to**: The final offset used to fill the texture specified in UV coordinates.
- **gradient**: The Gradient used to fill the texture.
- **height**: The number of vertical color samples that will be obtained from the Gradient, which also represents the texture's height.
- **repeat**: The gradient's repeat type.
- **use_hdr**: If `true`, the generated texture will support high dynamic range (`Image.FORMAT_RGBAF` format). This allows for glow effects to work if `Environment.glow_enabled` is `true`. If `false`, the generated texture will use low dynamic range; overbright colors will be clamped (`Image.FORMAT_RGBA8` format).
- **width**: The number of horizontal color samples that will be obtained from the Gradient, which also represents the texture's width.

**Enums:**
**Fill:** FILL_LINEAR=0, FILL_RADIAL=1, FILL_SQUARE=2, FILL_CONIC=3
  - FILL_LINEAR: The colors are linearly interpolated in a straight line.
  - FILL_RADIAL: The colors are linearly interpolated in a circular pattern.
  - FILL_SQUARE: The colors are linearly interpolated in a square pattern.
  - FILL_CONIC: The colors are linearly interpolated in a cone pattern.
**Repeat:** REPEAT_NONE=0, REPEAT=1, REPEAT_MIRROR=2
  - REPEAT_NONE: The gradient fill is restricted to the range defined by `fill_from` to `fill_to` offsets.
  - REPEAT: The texture is filled starting from `fill_from` to `fill_to` offsets, repeating the same pattern in both directions.
  - REPEAT_MIRROR: The texture is filled starting from `fill_from` to `fill_to` offsets, mirroring the pattern in both directions.

