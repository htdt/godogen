## RenderSceneBuffersExtension <- RenderSceneBuffers

This class allows for a RenderSceneBuffer implementation to be made in GDExtension.

**Methods:**
- _configure(config: RenderSceneBuffersConfiguration) - Implement this in GDExtension to handle the (re)sizing of a viewport.
- _set_anisotropic_filtering_level(anisotropic_filtering_level: int) - Implement this in GDExtension to change the anisotropic filtering level.
- _set_fsr_sharpness(fsr_sharpness: float) - Implement this in GDExtension to record a new FSR sharpness value.
- _set_texture_mipmap_bias(texture_mipmap_bias: float) - Implement this in GDExtension to change the texture mipmap bias.
- _set_use_debanding(use_debanding: bool) - Implement this in GDExtension to react to the debanding flag changing.

