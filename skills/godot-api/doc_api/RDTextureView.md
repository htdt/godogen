## RDTextureView <- RefCounted

This object is used by RenderingDevice.

**Props:**
- format_override: int (RenderingDevice.DataFormat) = 232
- swizzle_a: int (RenderingDevice.TextureSwizzle) = 6
- swizzle_b: int (RenderingDevice.TextureSwizzle) = 5
- swizzle_g: int (RenderingDevice.TextureSwizzle) = 4
- swizzle_r: int (RenderingDevice.TextureSwizzle) = 3

- **format_override**: Optional override for the data format to return sampled values in. The corresponding RDTextureFormat must have had this added as a shareable format. The default value of `RenderingDevice.DATA_FORMAT_MAX` does not override the format.
- **swizzle_a**: The channel to sample when sampling the alpha channel.
- **swizzle_b**: The channel to sample when sampling the blue color channel.
- **swizzle_g**: The channel to sample when sampling the green color channel.
- **swizzle_r**: The channel to sample when sampling the red color channel.

