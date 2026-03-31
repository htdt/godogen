## Light2D <- Node2D

Casts light in a 2D environment. A light is defined as a color, an energy value, a mode (see constants), and various other parameters (range and shadows-related).

**Props:**
- blend_mode: int (Light2D.BlendMode) = 0
- color: Color = Color(1, 1, 1, 1)
- editor_only: bool = false
- enabled: bool = true
- energy: float = 1.0
- range_item_cull_mask: int = 1
- range_layer_max: int = 0
- range_layer_min: int = 0
- range_z_max: int = 1024
- range_z_min: int = -1024
- shadow_color: Color = Color(0, 0, 0, 0)
- shadow_enabled: bool = false
- shadow_filter: int (Light2D.ShadowFilter) = 0
- shadow_filter_smooth: float = 0.0
- shadow_item_cull_mask: int = 1

- **blend_mode**: The Light2D's blend mode.
- **color**: The Light2D's Color.
- **editor_only**: If `true`, Light2D will only appear when editing the scene.
- **enabled**: If `true`, Light2D will emit light.
- **energy**: The Light2D's energy value. The larger the value, the stronger the light.
- **range_item_cull_mask**: The layer mask. Only objects with a matching `CanvasItem.light_mask` will be affected by the Light2D. See also `shadow_item_cull_mask`, which affects which objects can cast shadows. **Note:** `range_item_cull_mask` is ignored by DirectionalLight2D, which will always light a 2D node regardless of the 2D node's `CanvasItem.light_mask`.
- **range_layer_max**: Maximum layer value of objects that are affected by the Light2D.
- **range_layer_min**: Minimum layer value of objects that are affected by the Light2D.
- **range_z_max**: Maximum `z` value of objects that are affected by the Light2D.
- **range_z_min**: Minimum `z` value of objects that are affected by the Light2D.
- **shadow_color**: Color of shadows cast by the Light2D.
- **shadow_enabled**: If `true`, the Light2D will cast shadows.
- **shadow_filter**: Shadow filter type.
- **shadow_filter_smooth**: Smoothing value for shadows. Higher values will result in softer shadows, at the cost of visible streaks that can appear in shadow rendering. `shadow_filter_smooth` only has an effect if `shadow_filter` is `SHADOW_FILTER_PCF5` or `SHADOW_FILTER_PCF13`.
- **shadow_item_cull_mask**: The shadow mask. Used with LightOccluder2D to cast shadows. Only occluders with a matching `CanvasItem.light_mask` will cast shadows. See also `range_item_cull_mask`, which affects which objects can *receive* the light.

**Methods:**
- get_height() -> float - Returns the light's height, which is used in 2D normal mapping. See `PointLight2D.height` and `DirectionalLight2D.height`.
- set_height(height: float) - Sets the light's height, which is used in 2D normal mapping. See `PointLight2D.height` and `DirectionalLight2D.height`.

**Enums:**
**ShadowFilter:** SHADOW_FILTER_NONE=0, SHADOW_FILTER_PCF5=1, SHADOW_FILTER_PCF13=2
  - SHADOW_FILTER_NONE: No filter applies to the shadow map. This provides hard shadow edges and is the fastest to render. See `shadow_filter`.
  - SHADOW_FILTER_PCF5: Percentage closer filtering (5 samples) applies to the shadow map. This is slower compared to hard shadow rendering. See `shadow_filter`.
  - SHADOW_FILTER_PCF13: Percentage closer filtering (13 samples) applies to the shadow map. This is the slowest shadow filtering mode, and should be used sparingly. See `shadow_filter`.
**BlendMode:** BLEND_MODE_ADD=0, BLEND_MODE_SUB=1, BLEND_MODE_MIX=2
  - BLEND_MODE_ADD: Adds the value of pixels corresponding to the Light2D to the values of pixels under it. This is the common behavior of a light.
  - BLEND_MODE_SUB: Subtracts the value of pixels corresponding to the Light2D to the values of pixels under it, resulting in inversed light effect.
  - BLEND_MODE_MIX: Mix the value of pixels corresponding to the Light2D to the values of pixels under it by linear interpolation.

