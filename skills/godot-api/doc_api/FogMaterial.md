## FogMaterial <- Material

A Material resource that can be used by FogVolumes to draw volumetric effects. If you need more advanced effects, use a custom .

**Props:**
- albedo: Color = Color(1, 1, 1, 1)
- density: float = 1.0
- density_texture: Texture3D
- edge_fade: float = 0.1
- emission: Color = Color(0, 0, 0, 1)
- height_falloff: float = 0.0

- **albedo**: The single-scattering Color of the FogVolume. Internally, `albedo` is converted into single-scattering, which is additively blended with other FogVolumes and the `Environment.volumetric_fog_albedo`.
- **density**: The density of the FogVolume. Denser objects are more opaque, but may suffer from under-sampling artifacts that look like stripes. Negative values can be used to subtract fog from other FogVolumes or global volumetric fog. **Note:** Due to limited precision, `density` values between `-0.001` and `0.001` (exclusive) act like `0.0`. This does not apply to `Environment.volumetric_fog_density`.
- **density_texture**: The 3D texture that is used to scale the `density` of the FogVolume. This can be used to vary fog density within the FogVolume with any kind of static pattern. For animated effects, consider using a custom .
- **edge_fade**: The hardness of the edges of the FogVolume. A higher value will result in softer edges, while a lower value will result in harder edges.
- **emission**: The Color of the light emitted by the FogVolume. Emitted light will not cast light or shadows on other objects, but can be useful for modulating the Color of the FogVolume independently from light sources.
- **height_falloff**: The rate by which the height-based fog decreases in density as height increases in world space. A high falloff will result in a sharp transition, while a low falloff will result in a smoother transition. A value of `0.0` results in uniform-density fog. The height threshold is determined by the height of the associated FogVolume.

