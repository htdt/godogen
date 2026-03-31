## GeometryInstance3D <- VisualInstance3D

Base node for geometry-based visual instances. Shares some common functionality like visibility and custom materials.

**Props:**
- cast_shadow: int (GeometryInstance3D.ShadowCastingSetting) = 1
- custom_aabb: AABB = AABB(0, 0, 0, 0, 0, 0)
- extra_cull_margin: float = 0.0
- gi_lightmap_scale: int (GeometryInstance3D.LightmapScale) = 0
- gi_lightmap_texel_scale: float = 1.0
- gi_mode: int (GeometryInstance3D.GIMode) = 1
- ignore_occlusion_culling: bool = false
- lod_bias: float = 1.0
- material_overlay: Material
- material_override: Material
- transparency: float = 0.0
- visibility_range_begin: float = 0.0
- visibility_range_begin_margin: float = 0.0
- visibility_range_end: float = 0.0
- visibility_range_end_margin: float = 0.0
- visibility_range_fade_mode: int (GeometryInstance3D.VisibilityRangeFadeMode) = 0

- **cast_shadow**: The mode used to cast shadows from this instance.
- **custom_aabb**: Overrides the bounding box of this node with a custom one. This can be used to avoid the expensive AABB recalculation that happens when a skeleton is used with a MeshInstance3D or to have precise control over the MeshInstance3D's bounding box. To use the default AABB, set value to an AABB with all fields set to `0.0`. To avoid frustum culling, set `custom_aabb` to a very large AABB that covers your entire game world such as `AABB(-10000, -10000, -10000, 20000, 20000, 20000)`. To disable all forms of culling (including occlusion and layer culling), call `RenderingServer.instance_set_ignore_culling` on the GeometryInstance3D's RID.
- **extra_cull_margin**: The extra distance added to the GeometryInstance3D's bounding box (AABB) to increase its cull box.
- **gi_lightmap_scale**: The texel density to use for lightmapping in LightmapGI.
- **gi_lightmap_texel_scale**: The texel density to use for lightmapping in LightmapGI. Greater scale values provide higher resolution in the lightmap, which can result in sharper shadows for lights that have both direct and indirect light baked. However, greater scale values will also increase the space taken by the mesh in the lightmap texture, which increases the memory, storage, and bake time requirements. When using a single mesh at different scales, consider adjusting this value to keep the lightmap texel density consistent across meshes. For example, doubling `gi_lightmap_texel_scale` doubles the lightmap texture resolution for this object *on each axis*, so it will *quadruple* the texel count.
- **gi_mode**: The global illumination mode to use for the whole geometry. To avoid inconsistent results, use a mode that matches the purpose of the mesh during gameplay (static/dynamic). **Note:** Lights' bake mode will also affect the global illumination rendering. See `Light3D.light_bake_mode`.
- **ignore_occlusion_culling**: If `true`, disables occlusion culling for this instance. Useful for gizmos that must be rendered even when occlusion culling is in use. **Note:** `ignore_occlusion_culling` does not affect frustum culling (which is what happens when an object is not visible given the camera's angle). To avoid frustum culling, set `custom_aabb` to a very large AABB that covers your entire game world such as `AABB(-10000, -10000, -10000, 20000, 20000, 20000)`.
- **lod_bias**: Changes how quickly the mesh transitions to a lower level of detail. A value of 0 will force the mesh to its lowest level of detail, a value of 1 will use the default settings, and larger values will keep the mesh in a higher level of detail at farther distances. Useful for testing level of detail transitions in the editor.
- **material_overlay**: The material overlay for the whole geometry. If a material is assigned to this property, it will be rendered on top of any other active material for all the surfaces.
- **material_override**: The material override for the whole geometry. If a material is assigned to this property, it will be used instead of any material set in any material slot of the mesh.
- **transparency**: The transparency applied to the whole geometry (as a multiplier of the materials' existing transparency). `0.0` is fully opaque, while `1.0` is fully transparent. Values greater than `0.0` (exclusive) will force the geometry's materials to go through the transparent pipeline, which is slower to render and can exhibit rendering issues due to incorrect transparency sorting. However, unlike using a transparent material, setting `transparency` to a value greater than `0.0` (exclusive) will *not* disable shadow rendering. In spatial shaders, `1.0 - transparency` is set as the default value of the `ALPHA` built-in. **Note:** `transparency` is clamped between `0.0` and `1.0`, so this property cannot be used to make transparent materials more opaque than they originally are. **Note:** Only supported when using the Forward+ rendering method. When using the Mobile or Compatibility rendering method, `transparency` is ignored and is considered as always being `0.0`.
- **visibility_range_begin**: Starting distance from which the GeometryInstance3D will be visible, taking `visibility_range_begin_margin` into account as well. The default value of 0 is used to disable the range check.
- **visibility_range_begin_margin**: Margin for the `visibility_range_begin` threshold. The GeometryInstance3D will only change its visibility state when it goes over or under the `visibility_range_begin` threshold by this amount. If `visibility_range_fade_mode` is `VISIBILITY_RANGE_FADE_DISABLED`, this acts as a hysteresis distance. If `visibility_range_fade_mode` is `VISIBILITY_RANGE_FADE_SELF` or `VISIBILITY_RANGE_FADE_DEPENDENCIES`, this acts as a fade transition distance and must be set to a value greater than `0.0` for the effect to be noticeable.
- **visibility_range_end**: Distance from which the GeometryInstance3D will be hidden, taking `visibility_range_end_margin` into account as well. The default value of 0 is used to disable the range check.
- **visibility_range_end_margin**: Margin for the `visibility_range_end` threshold. The GeometryInstance3D will only change its visibility state when it goes over or under the `visibility_range_end` threshold by this amount. If `visibility_range_fade_mode` is `VISIBILITY_RANGE_FADE_DISABLED`, this acts as a hysteresis distance. If `visibility_range_fade_mode` is `VISIBILITY_RANGE_FADE_SELF` or `VISIBILITY_RANGE_FADE_DEPENDENCIES`, this acts as a fade transition distance and must be set to a value greater than `0.0` for the effect to be noticeable.
- **visibility_range_fade_mode**: Controls which instances will be faded when approaching the limits of the visibility range.

**Methods:**
- get_instance_shader_parameter(name: StringName) -> Variant - Get the value of a shader parameter as set on this instance.
- set_instance_shader_parameter(name: StringName, value: Variant) - Set the value of a shader uniform for this instance only (). See also `ShaderMaterial.set_shader_parameter` to assign a uniform on all instances using the same ShaderMaterial. **Note:** For a shader uniform to be assignable on a per-instance basis, it *must* be defined with `instance uniform ...` rather than `uniform ...` in the shader code. **Note:** `name` is case-sensitive and must match the name of the uniform in the code exactly (not the capitalized name in the inspector). **Note:** Per-instance shader uniforms are only available in Spatial and CanvasItem shaders, but not for Fog, Sky, or Particles shaders.

**Enums:**
**ShadowCastingSetting:** SHADOW_CASTING_SETTING_OFF=0, SHADOW_CASTING_SETTING_ON=1, SHADOW_CASTING_SETTING_DOUBLE_SIDED=2, SHADOW_CASTING_SETTING_SHADOWS_ONLY=3
  - SHADOW_CASTING_SETTING_OFF: Will not cast any shadows. Use this to improve performance for small geometry that is unlikely to cast noticeable shadows (such as debris).
  - SHADOW_CASTING_SETTING_ON: Will cast shadows from all visible faces in the GeometryInstance3D. Will take culling into account, so faces not being rendered will not be taken into account when shadow casting.
  - SHADOW_CASTING_SETTING_DOUBLE_SIDED: Will cast shadows from all visible faces in the GeometryInstance3D. Will not take culling into account, so all faces will be taken into account when shadow casting.
  - SHADOW_CASTING_SETTING_SHADOWS_ONLY: Will only show the shadows casted from this object. In other words, the actual mesh will not be visible, only the shadows casted from the mesh will be.
**GIMode:** GI_MODE_DISABLED=0, GI_MODE_STATIC=1, GI_MODE_DYNAMIC=2
  - GI_MODE_DISABLED: Disabled global illumination mode. Use for dynamic objects that do not contribute to global illumination (such as characters). When using VoxelGI and SDFGI, the geometry will *receive* indirect lighting and reflections but the geometry will not be considered in GI baking.
  - GI_MODE_STATIC: Baked global illumination mode. Use for static objects that contribute to global illumination (such as level geometry). This GI mode is effective when using VoxelGI, SDFGI and LightmapGI.
  - GI_MODE_DYNAMIC: Dynamic global illumination mode. Use for dynamic objects that contribute to global illumination. This GI mode is only effective when using VoxelGI, but it has a higher performance impact than `GI_MODE_STATIC`. When using other GI methods, this will act the same as `GI_MODE_DISABLED`. When using LightmapGI, the object will receive indirect lighting using lightmap probes instead of using the baked lightmap texture.
**LightmapScale:** LIGHTMAP_SCALE_1X=0, LIGHTMAP_SCALE_2X=1, LIGHTMAP_SCALE_4X=2, LIGHTMAP_SCALE_8X=3, LIGHTMAP_SCALE_MAX=4
  - LIGHTMAP_SCALE_1X: The standard texel density for lightmapping with LightmapGI.
  - LIGHTMAP_SCALE_2X: Multiplies texel density by 2× for lightmapping with LightmapGI. To ensure consistency in texel density, use this when scaling a mesh by a factor between 1.5 and 3.0.
  - LIGHTMAP_SCALE_4X: Multiplies texel density by 4× for lightmapping with LightmapGI. To ensure consistency in texel density, use this when scaling a mesh by a factor between 3.0 and 6.0.
  - LIGHTMAP_SCALE_8X: Multiplies texel density by 8× for lightmapping with LightmapGI. To ensure consistency in texel density, use this when scaling a mesh by a factor greater than 6.0.
  - LIGHTMAP_SCALE_MAX: Represents the size of the `LightmapScale` enum.
**VisibilityRangeFadeMode:** VISIBILITY_RANGE_FADE_DISABLED=0, VISIBILITY_RANGE_FADE_SELF=1, VISIBILITY_RANGE_FADE_DEPENDENCIES=2
  - VISIBILITY_RANGE_FADE_DISABLED: Will not fade itself nor its visibility dependencies, hysteresis will be used instead. This is the fastest approach to manual LOD, but it can result in noticeable LOD transitions depending on how the LOD meshes are authored. See `visibility_range_begin` and `Node3D.visibility_parent` for more information.
  - VISIBILITY_RANGE_FADE_SELF: Will fade-out itself when reaching the limits of its own visibility range. This is slower than `VISIBILITY_RANGE_FADE_DISABLED`, but it can provide smoother transitions. The fading range is determined by `visibility_range_begin_margin` and `visibility_range_end_margin`. **Note:** Only supported when using the Forward+ rendering method. When using the Mobile or Compatibility rendering method, this mode acts like `VISIBILITY_RANGE_FADE_DISABLED` but with hysteresis disabled.
  - VISIBILITY_RANGE_FADE_DEPENDENCIES: Will fade-in its visibility dependencies (see `Node3D.visibility_parent`) when reaching the limits of its own visibility range. This is slower than `VISIBILITY_RANGE_FADE_DISABLED`, but it can provide smoother transitions. The fading range is determined by `visibility_range_begin_margin` and `visibility_range_end_margin`. **Note:** Only supported when using the Forward+ rendering method. When using the Mobile or Compatibility rendering method, this mode acts like `VISIBILITY_RANGE_FADE_DISABLED` but with hysteresis disabled.

