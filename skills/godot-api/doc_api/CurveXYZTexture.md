## CurveXYZTexture <- Texture2D

A 1D texture where the red, green, and blue color channels correspond to points on 3 unit Curve resources. Compared to using separate CurveTextures, this further simplifies the task of saving curves as image files. If you only need to store one curve within a single texture, use CurveTexture instead. See also GradientTexture1D and GradientTexture2D.

**Props:**
- curve_x: Curve
- curve_y: Curve
- curve_z: Curve
- resource_local_to_scene: bool = false
- width: int = 256

- **curve_x**: The Curve that is rendered onto the texture's red channel. Should be a unit Curve.
- **curve_y**: The Curve that is rendered onto the texture's green channel. Should be a unit Curve.
- **curve_z**: The Curve that is rendered onto the texture's blue channel. Should be a unit Curve.
- **width**: The width of the texture (in pixels). Higher values make it possible to represent high-frequency data better (such as sudden direction changes), at the cost of increased generation time and memory usage.

