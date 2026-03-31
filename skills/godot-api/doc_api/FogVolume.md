## FogVolume <- VisualInstance3D

FogVolumes are used to add localized fog into the global volumetric fog effect. FogVolumes can also remove volumetric fog from specific areas if using a FogMaterial with a negative `FogMaterial.density`. Performance of FogVolumes is directly related to their relative size on the screen and the complexity of their attached FogMaterial. It is best to keep FogVolumes relatively small and simple where possible. **Note:** FogVolumes only have a visible effect if `Environment.volumetric_fog_enabled` is `true`. If you don't want fog to be globally visible (but only within FogVolume nodes), set `Environment.volumetric_fog_density` to `0.0`.

**Props:**
- material: Material
- shape: int (RenderingServer.FogVolumeShape) = 3
- size: Vector3 = Vector3(2, 2, 2)

- **material**: The Material used by the FogVolume. Can be either a built-in FogMaterial or a custom ShaderMaterial.
- **shape**: The shape of the FogVolume. This can be set to either `RenderingServer.FOG_VOLUME_SHAPE_ELLIPSOID`, `RenderingServer.FOG_VOLUME_SHAPE_CONE`, `RenderingServer.FOG_VOLUME_SHAPE_CYLINDER`, `RenderingServer.FOG_VOLUME_SHAPE_BOX` or `RenderingServer.FOG_VOLUME_SHAPE_WORLD`.
- **size**: The size of the FogVolume when `shape` is `RenderingServer.FOG_VOLUME_SHAPE_ELLIPSOID`, `RenderingServer.FOG_VOLUME_SHAPE_CONE`, `RenderingServer.FOG_VOLUME_SHAPE_CYLINDER` or `RenderingServer.FOG_VOLUME_SHAPE_BOX`. **Note:** Thin fog volumes may appear to flicker when the camera moves or rotates. This can be alleviated by increasing `ProjectSettings.rendering/environment/volumetric_fog/volume_depth` (at a performance cost) or by decreasing `Environment.volumetric_fog_length` (at no performance cost, but at the cost of lower fog range). Alternatively, the FogVolume can be made thicker and use a lower density in the `material`. **Note:** If `shape` is `RenderingServer.FOG_VOLUME_SHAPE_CONE` or `RenderingServer.FOG_VOLUME_SHAPE_CYLINDER`, the cone/cylinder will be adjusted to fit within the size. Non-uniform scaling of cone/cylinder shapes via the `size` property is not supported, but you can scale the FogVolume node instead.

