## RenderSceneBuffersConfiguration <- RefCounted

This configuration object is created and populated by the render engine on a viewport change and used to (re)configure a RenderSceneBuffers object.

**Props:**
- anisotropic_filtering_level: int (RenderingServer.ViewportAnisotropicFiltering) = 2
- fsr_sharpness: float = 0.0
- internal_size: Vector2i = Vector2i(0, 0)
- msaa_3d: int (RenderingServer.ViewportMSAA) = 0
- render_target: RID = RID()
- scaling_3d_mode: int (RenderingServer.ViewportScaling3DMode) = 255
- screen_space_aa: int (RenderingServer.ViewportScreenSpaceAA) = 0
- target_size: Vector2i = Vector2i(0, 0)
- texture_mipmap_bias: float = 0.0
- view_count: int = 1

- **anisotropic_filtering_level**: Level of the anisotropic filter.
- **fsr_sharpness**: FSR Sharpness applicable if FSR upscaling is used.
- **internal_size**: The size of the 3D render buffer used for rendering.
- **msaa_3d**: The MSAA mode we're using for 3D rendering.
- **render_target**: The render target associated with these buffer.
- **scaling_3d_mode**: The requested scaling mode with which we upscale/downscale if `internal_size` and `target_size` are not equal.
- **screen_space_aa**: The requested screen space AA applied in post processing.
- **target_size**: The target (upscale) size if scaling is used.
- **texture_mipmap_bias**: Bias applied to mipmaps.
- **view_count**: The number of views we're rendering.

