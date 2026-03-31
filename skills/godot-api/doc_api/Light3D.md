## Light3D <- VisualInstance3D

Light3D is the *abstract* base class for light nodes. As it can't be instantiated, it shouldn't be used directly. Other types of light nodes inherit from it. Light3D contains the common variables and parameters used for lighting.

**Props:**
- distance_fade_begin: float = 40.0
- distance_fade_enabled: bool = false
- distance_fade_length: float = 10.0
- distance_fade_shadow: float = 50.0
- editor_only: bool = false
- light_angular_distance: float = 0.0
- light_bake_mode: int (Light3D.BakeMode) = 2
- light_color: Color = Color(1, 1, 1, 1)
- light_cull_mask: int = 4294967295
- light_energy: float = 1.0
- light_indirect_energy: float = 1.0
- light_intensity_lumens: float
- light_intensity_lux: float
- light_negative: bool = false
- light_projector: Texture2D
- light_size: float = 0.0
- light_specular: float = 1.0
- light_temperature: float
- light_volumetric_fog_energy: float = 1.0
- shadow_bias: float = 0.1
- shadow_blur: float = 1.0
- shadow_caster_mask: int = 4294967295
- shadow_enabled: bool = false
- shadow_normal_bias: float = 2.0
- shadow_opacity: float = 1.0
- shadow_reverse_cull_face: bool = false
- shadow_transmittance_bias: float = 0.05

- **distance_fade_begin**: The distance from the camera at which the light begins to fade away (in 3D units). **Note:** Only effective for OmniLight3D and SpotLight3D.
- **distance_fade_enabled**: If `true`, the light will smoothly fade away when far from the active Camera3D starting at `distance_fade_begin`. This acts as a form of level of detail (LOD). The light will fade out over `distance_fade_begin` + `distance_fade_length`, after which it will be culled and not sent to the shader at all. Use this to reduce the number of active lights in a scene and thus improve performance. **Note:** Only effective for OmniLight3D and SpotLight3D.
- **distance_fade_length**: Distance over which the light and its shadow fades. The light's energy and shadow's opacity is progressively reduced over this distance and is completely invisible at the end. **Note:** Only effective for OmniLight3D and SpotLight3D.
- **distance_fade_shadow**: The distance from the camera at which the light's shadow cuts off (in 3D units). Set this to a value lower than `distance_fade_begin` + `distance_fade_length` to further improve performance, as shadow rendering is often more expensive than light rendering itself. **Note:** Only effective for OmniLight3D and SpotLight3D, and only when `shadow_enabled` is `true`.
- **editor_only**: If `true`, the light only appears in the editor and will not be visible at runtime. If `true`, the light will never be baked in LightmapGI regardless of its `light_bake_mode`.
- **light_angular_distance**: The light's angular size in degrees. Increasing this will make shadows softer at greater distances (also called percentage-closer soft shadows, or PCSS). Only available for DirectionalLight3Ds. For reference, the Sun from the Earth is approximately `0.5`. Increasing this value above `0.0` for lights with shadows enabled will have a noticeable performance cost due to PCSS. **Note:** `light_angular_distance` is not affected by `Node3D.scale` (the light's scale or its parent's scale). **Note:** PCSS for directional lights is only supported in the Forward+ rendering method, not Mobile or Compatibility.
- **light_bake_mode**: The light's bake mode. This will affect the global illumination techniques that have an effect on the light's rendering. **Note:** Meshes' global illumination mode will also affect the global illumination rendering. See `GeometryInstance3D.gi_mode`.
- **light_color**: The light's color in nonlinear sRGB encoding. An *overbright* color can be used to achieve a result equivalent to increasing the light's `light_energy`.
- **light_cull_mask**: The light will affect objects in the selected layers. **Note:** The light cull mask is ignored by VoxelGI, SDFGI, LightmapGI, and volumetric fog. These will always render lights in a way that ignores the cull mask. See also `VisualInstance3D.layers`.
- **light_energy**: The light's strength multiplier (this is not a physical unit). For OmniLight3D and SpotLight3D, changing this value will only change the light color's intensity, not the light's radius.
- **light_indirect_energy**: Secondary multiplier used with indirect light (light bounces). Used with VoxelGI and SDFGI (see `Environment.sdfgi_enabled`). **Note:** This property is ignored if `light_energy` is equal to `0.0`, as the light won't be present at all in the GI shader.
- **light_intensity_lumens**: Used by positional lights (OmniLight3D and SpotLight3D) when `ProjectSettings.rendering/lights_and_shadows/use_physical_light_units` is `true`. Sets the intensity of the light source measured in Lumens. Lumens are a measure of luminous flux, which is the total amount of visible light emitted by a light source per unit of time. For SpotLight3Ds, we assume that the area outside the visible cone is surrounded by a perfect light absorbing material. Accordingly, the apparent brightness of the cone area does not change as the cone increases and decreases in size. A typical household lightbulb can range from around 600 lumens to 1,200 lumens, a candle is about 13 lumens, while a streetlight can be approximately 60,000 lumens.
- **light_intensity_lux**: Used by DirectionalLight3Ds when `ProjectSettings.rendering/lights_and_shadows/use_physical_light_units` is `true`. Sets the intensity of the light source measured in Lux. Lux is a measure of luminous flux per unit area, it is equal to one lumen per square meter. Lux is the measure of how much light hits a surface at a given time. On a clear sunny day a surface in direct sunlight may be approximately 100,000 lux, a typical room in a home may be approximately 50 lux, while the moonlit ground may be approximately 0.1 lux.
- **light_negative**: If `true`, the light's effect is reversed, darkening areas and casting bright shadows.
- **light_projector**: Texture2D projected by light. `shadow_enabled` must be on for the projector to work. Light projectors make the light appear as if it is shining through a colored but transparent object, almost like light shining through stained-glass. **Note:** Unlike BaseMaterial3D whose filter mode can be adjusted on a per-material basis, the filter mode for light projector textures is set globally with `ProjectSettings.rendering/textures/light_projectors/filter`. **Note:** Light projector textures are only supported in the Forward+ and Mobile rendering methods, not Compatibility.
- **light_size**: The size of the light in Godot units. Only available for OmniLight3Ds and SpotLight3Ds. Increasing this value will make the light fade out slower and shadows appear blurrier (also called percentage-closer soft shadows, or PCSS). This can be used to simulate area lights to an extent. Increasing this value above `0.0` for lights with shadows enabled will have a noticeable performance cost due to PCSS. **Note:** `light_size` is not affected by `Node3D.scale` (the light's scale or its parent's scale). **Note:** PCSS for positional lights is only supported in the Forward+ and Mobile rendering methods, not Compatibility.
- **light_specular**: The intensity of the specular blob in objects affected by the light. At `0`, the light becomes a pure diffuse light. When not baking emission, this can be used to avoid unrealistic reflections when placing lights above an emissive surface.
- **light_temperature**: Sets the color temperature of the light source, measured in Kelvin. This is used to calculate a correlated color temperature which tints the `light_color`. The sun on a cloudy day is approximately 6500 Kelvin, on a clear day it is between 5500 to 6000 Kelvin, and on a clear day at sunrise or sunset it ranges to around 1850 Kelvin.
- **light_volumetric_fog_energy**: Secondary multiplier multiplied with `light_energy` then used with the Environment's volumetric fog (if enabled). If set to `0.0`, computing volumetric fog will be skipped for this light, which can improve performance for large amounts of lights when volumetric fog is enabled. **Note:** To prevent short-lived dynamic light effects from poorly interacting with volumetric fog, lights used in those effects should have `light_volumetric_fog_energy` set to `0.0` unless `Environment.volumetric_fog_temporal_reprojection_enabled` is disabled (or unless the reprojection amount is significantly lowered).
- **shadow_bias**: Used to adjust shadow appearance. Too small a value results in self-shadowing ("shadow acne"), while too large a value causes shadows to separate from casters ("peter-panning"). Adjust as needed.
- **shadow_blur**: Blurs the edges of the shadow. Can be used to hide pixel artifacts in low-resolution shadow maps. A high value can impact performance, make shadows appear grainy and can cause other unwanted artifacts. Try to keep as near default as possible.
- **shadow_caster_mask**: The light will only cast shadows using objects in the selected layers.
- **shadow_enabled**: If `true`, the light will cast real-time shadows. This has a significant performance cost. Only enable shadow rendering when it makes a noticeable difference in the scene's appearance, and consider using `distance_fade_enabled` to hide the light when far away from the Camera3D.
- **shadow_normal_bias**: Offsets the lookup into the shadow map by the object's normal. This can be used to reduce self-shadowing artifacts without using `shadow_bias`. In practice, this value should be tweaked along with `shadow_bias` to reduce artifacts as much as possible.
- **shadow_opacity**: The opacity to use when rendering the light's shadow map. Values lower than `1.0` make the light appear through shadows. This can be used to fake global illumination at a low performance cost.
- **shadow_reverse_cull_face**: If `true`, reverses the backface culling of the mesh. This can be useful when you have a flat mesh that has a light behind it. If you need to cast a shadow on both sides of the mesh, set the mesh to use double-sided shadows with `GeometryInstance3D.SHADOW_CASTING_SETTING_DOUBLE_SIDED`.

**Methods:**
- get_correlated_color() -> Color - Returns the Color of an idealized blackbody at the given `light_temperature`. This value is calculated internally based on the `light_temperature`. This Color is multiplied by `light_color` before being sent to the RenderingServer.
- get_param(param: int) -> float - Returns the value of the specified `Light3D.Param` parameter.
- set_param(param: int, value: float) - Sets the value of the specified `Light3D.Param` parameter.

**Enums:**
**Param:** PARAM_ENERGY=0, PARAM_INDIRECT_ENERGY=1, PARAM_VOLUMETRIC_FOG_ENERGY=2, PARAM_SPECULAR=3, PARAM_RANGE=4, PARAM_SIZE=5, PARAM_ATTENUATION=6, PARAM_SPOT_ANGLE=7, PARAM_SPOT_ATTENUATION=8, PARAM_SHADOW_MAX_DISTANCE=9, ...
  - PARAM_ENERGY: Constant for accessing `light_energy`.
  - PARAM_INDIRECT_ENERGY: Constant for accessing `light_indirect_energy`.
  - PARAM_VOLUMETRIC_FOG_ENERGY: Constant for accessing `light_volumetric_fog_energy`.
  - PARAM_SPECULAR: Constant for accessing `light_specular`.
  - PARAM_RANGE: Constant for accessing `OmniLight3D.omni_range` or `SpotLight3D.spot_range`.
  - PARAM_SIZE: Constant for accessing `light_size`.
  - PARAM_ATTENUATION: Constant for accessing `OmniLight3D.omni_attenuation` or `SpotLight3D.spot_attenuation`.
  - PARAM_SPOT_ANGLE: Constant for accessing `SpotLight3D.spot_angle`.
  - PARAM_SPOT_ATTENUATION: Constant for accessing `SpotLight3D.spot_angle_attenuation`.
  - PARAM_SHADOW_MAX_DISTANCE: Constant for accessing `DirectionalLight3D.directional_shadow_max_distance`.
  - PARAM_SHADOW_SPLIT_1_OFFSET: Constant for accessing `DirectionalLight3D.directional_shadow_split_1`.
  - PARAM_SHADOW_SPLIT_2_OFFSET: Constant for accessing `DirectionalLight3D.directional_shadow_split_2`.
  - PARAM_SHADOW_SPLIT_3_OFFSET: Constant for accessing `DirectionalLight3D.directional_shadow_split_3`.
  - PARAM_SHADOW_FADE_START: Constant for accessing `DirectionalLight3D.directional_shadow_fade_start`.
  - PARAM_SHADOW_NORMAL_BIAS: Constant for accessing `shadow_normal_bias`.
  - PARAM_SHADOW_BIAS: Constant for accessing `shadow_bias`.
  - PARAM_SHADOW_PANCAKE_SIZE: Constant for accessing `DirectionalLight3D.directional_shadow_pancake_size`.
  - PARAM_SHADOW_OPACITY: Constant for accessing `shadow_opacity`.
  - PARAM_SHADOW_BLUR: Constant for accessing `shadow_blur`.
  - PARAM_TRANSMITTANCE_BIAS: Constant for accessing `shadow_transmittance_bias`.
  - PARAM_INTENSITY: Constant for accessing `light_intensity_lumens` and `light_intensity_lux`. Only used when `ProjectSettings.rendering/lights_and_shadows/use_physical_light_units` is `true`.
  - PARAM_MAX: Represents the size of the `Param` enum.
**BakeMode:** BAKE_DISABLED=0, BAKE_STATIC=1, BAKE_DYNAMIC=2
  - BAKE_DISABLED: Light is ignored when baking. This is the fastest mode, but the light will not be taken into account when baking global illumination. This mode should generally be used for dynamic lights that change quickly, as the effect of global illumination is less noticeable on those lights. **Note:** Hiding a light does *not* affect baking LightmapGI. Hiding a light will still affect baking VoxelGI and SDFGI (see `Environment.sdfgi_enabled`).
  - BAKE_STATIC: Light is taken into account in static baking (VoxelGI, LightmapGI, SDFGI (`Environment.sdfgi_enabled`)). The light can be moved around or modified, but its global illumination will not update in real-time. This is suitable for subtle changes (such as flickering torches), but generally not large changes such as toggling a light on and off. **Note:** The light is not baked in LightmapGI if `editor_only` is `true`.
  - BAKE_DYNAMIC: Light is taken into account in dynamic baking (VoxelGI and SDFGI (`Environment.sdfgi_enabled`) only). The light can be moved around or modified with global illumination updating in real-time. The light's global illumination appearance will be slightly different compared to `BAKE_STATIC`. This has a greater performance cost compared to `BAKE_STATIC`. When using SDFGI, the update speed of dynamic lights is affected by `ProjectSettings.rendering/global_illumination/sdfgi/frames_to_update_lights`.

