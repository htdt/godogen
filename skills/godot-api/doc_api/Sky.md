## Sky <- Resource

The Sky class uses a Material to render a 3D environment's background and the light it emits by updating the reflection/radiance cubemaps.

**Props:**
- process_mode: int (Sky.ProcessMode) = 0
- radiance_size: int (Sky.RadianceSize) = 3
- sky_material: Material

- **process_mode**: The method for generating the radiance map from the sky. The radiance map is a cubemap with increasingly blurry versions of the sky corresponding to different levels of roughness. Radiance maps can be expensive to calculate.
- **radiance_size**: The Sky's radiance map size. The higher the radiance map size, the more detailed the lighting from the Sky will be. **Note:** Some hardware will have trouble with higher radiance sizes, especially `RADIANCE_SIZE_512` and above. Only use such high values on high-end hardware.
- **sky_material**: Material used to draw the background. Can be PanoramaSkyMaterial, ProceduralSkyMaterial, PhysicalSkyMaterial, or even a ShaderMaterial if you want to use your own custom shader.

**Enums:**
**RadianceSize:** RADIANCE_SIZE_32=0, RADIANCE_SIZE_64=1, RADIANCE_SIZE_128=2, RADIANCE_SIZE_256=3, RADIANCE_SIZE_512=4, RADIANCE_SIZE_1024=5, RADIANCE_SIZE_2048=6, RADIANCE_SIZE_MAX=7
  - RADIANCE_SIZE_32: Radiance texture size is 32×32 pixels.
  - RADIANCE_SIZE_64: Radiance texture size is 64×64 pixels.
  - RADIANCE_SIZE_128: Radiance texture size is 128×128 pixels.
  - RADIANCE_SIZE_256: Radiance texture size is 256×256 pixels.
  - RADIANCE_SIZE_512: Radiance texture size is 512×512 pixels.
  - RADIANCE_SIZE_1024: Radiance texture size is 1024×1024 pixels.
  - RADIANCE_SIZE_2048: Radiance texture size is 2048×2048 pixels.
  - RADIANCE_SIZE_MAX: Represents the size of the `RadianceSize` enum.
**ProcessMode:** PROCESS_MODE_AUTOMATIC=0, PROCESS_MODE_QUALITY=1, PROCESS_MODE_INCREMENTAL=2, PROCESS_MODE_REALTIME=3
  - PROCESS_MODE_AUTOMATIC: Automatically selects the appropriate process mode based on your sky shader. If your shader uses `TIME` or `POSITION`, this will use `PROCESS_MODE_REALTIME`. If your shader uses any of the `LIGHT_*` variables or any custom uniforms, this uses `PROCESS_MODE_INCREMENTAL`. Otherwise, this defaults to `PROCESS_MODE_QUALITY`.
  - PROCESS_MODE_QUALITY: Uses high quality importance sampling to process the radiance map. In general, this results in much higher quality than `PROCESS_MODE_REALTIME` but takes much longer to generate. This should not be used if you plan on changing the sky at runtime. If you are finding that the reflection is not blurry enough and is showing sparkles or fireflies, try increasing `ProjectSettings.rendering/reflections/sky_reflections/ggx_samples`.
  - PROCESS_MODE_INCREMENTAL: Uses the same high quality importance sampling to process the radiance map as `PROCESS_MODE_QUALITY`, but updates over several frames. The number of frames is determined by `ProjectSettings.rendering/reflections/sky_reflections/roughness_layers`. Use this when you need highest quality radiance maps, but have a sky that updates slowly.
  - PROCESS_MODE_REALTIME: Uses the fast filtering algorithm to process the radiance map. In general this results in lower quality, but substantially faster run times. If you need better quality, but still need to update the sky every frame, consider turning on `ProjectSettings.rendering/reflections/sky_reflections/fast_filter_high_quality`. **Note:** The fast filtering algorithm is limited to 256×256 cubemaps, so `radiance_size` must be set to `RADIANCE_SIZE_256`. Otherwise, a warning is printed and the overridden radiance size is ignored.

