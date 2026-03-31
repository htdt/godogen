## CompositorEffect <- Resource

This resource defines a custom rendering effect that can be applied to Viewports through the viewports' Environment. You can implement a callback that is called during rendering at a given stage of the rendering pipeline and allows you to insert additional passes. Note that this callback happens on the rendering thread. CompositorEffect is an abstract base class and must be extended to implement specific rendering logic.

**Props:**
- access_resolved_color: bool
- access_resolved_depth: bool
- effect_callback_type: int (CompositorEffect.EffectCallbackType)
- enabled: bool
- needs_motion_vectors: bool
- needs_normal_roughness: bool
- needs_separate_specular: bool

- **access_resolved_color**: If `true` and MSAA is enabled, this will trigger a color buffer resolve before the effect is run. **Note:** In `_render_callback`, to access the resolved buffer use:
- **access_resolved_depth**: If `true` and MSAA is enabled, this will trigger a depth buffer resolve before the effect is run. **Note:** In `_render_callback`, to access the resolved buffer use:
- **effect_callback_type**: The type of effect that is implemented, determines at what stage of rendering the callback is called.
- **enabled**: If `true` this rendering effect is applied to any viewport it is added to.
- **needs_motion_vectors**: If `true` this triggers motion vectors being calculated during the opaque render state. **Note:** In `_render_callback`, to access the motion vector buffer use:
- **needs_normal_roughness**: If `true` this triggers normal and roughness data to be output during our depth pre-pass, only applicable for the Forward+ renderer. **Note:** In `_render_callback`, to access the roughness buffer use: The raw normal and roughness buffer is stored in an optimized format, different than the one available in Spatial shaders. When sampling the buffer, a conversion function must be applied. Use this function, copied from :
- **needs_separate_specular**: If `true` this triggers specular data being rendered to a separate buffer and combined after effects have been applied, only applicable for the Forward+ renderer.

**Methods:**
- _render_callback(effect_callback_type: int, render_data: RenderData) - Implement this function with your custom rendering code. `effect_callback_type` should always match the effect callback type you've specified in `effect_callback_type`. `render_data` provides access to the rendering state, it is only valid during rendering and should not be stored.

**Enums:**
**EffectCallbackType:** EFFECT_CALLBACK_TYPE_PRE_OPAQUE=0, EFFECT_CALLBACK_TYPE_POST_OPAQUE=1, EFFECT_CALLBACK_TYPE_POST_SKY=2, EFFECT_CALLBACK_TYPE_PRE_TRANSPARENT=3, EFFECT_CALLBACK_TYPE_POST_TRANSPARENT=4, EFFECT_CALLBACK_TYPE_MAX=5
  - EFFECT_CALLBACK_TYPE_PRE_OPAQUE: The callback is called before our opaque rendering pass, but after depth prepass (if applicable).
  - EFFECT_CALLBACK_TYPE_POST_OPAQUE: The callback is called after our opaque rendering pass, but before our sky is rendered.
  - EFFECT_CALLBACK_TYPE_POST_SKY: The callback is called after our sky is rendered, but before our back buffers are created (and if enabled, before subsurface scattering and/or screen space reflections).
  - EFFECT_CALLBACK_TYPE_PRE_TRANSPARENT: The callback is called before our transparent rendering pass, but after our sky is rendered and we've created our back buffers.
  - EFFECT_CALLBACK_TYPE_POST_TRANSPARENT: The callback is called after our transparent rendering pass, but before any built-in post-processing effects and output to our render target.
  - EFFECT_CALLBACK_TYPE_MAX: Represents the size of the `EffectCallbackType` enum.

