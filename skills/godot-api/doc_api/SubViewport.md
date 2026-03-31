## SubViewport <- Viewport

SubViewport Isolates a rectangular region of a scene to be displayed independently. This can be used, for example, to display UI in 3D space. **Note:** SubViewport is a Viewport that isn't a Window, i.e. it doesn't draw anything by itself. To display anything, SubViewport must have a non-zero size and be either put inside a SubViewportContainer or assigned to a ViewportTexture. **Note:** InputEvents are not passed to a standalone SubViewport by default. To ensure InputEvent propagation, a SubViewport can be placed inside of a SubViewportContainer.

**Props:**
- render_target_clear_mode: int (SubViewport.ClearMode) = 0
- render_target_update_mode: int (SubViewport.UpdateMode) = 2
- size: Vector2i = Vector2i(512, 512)
- size_2d_override: Vector2i = Vector2i(0, 0)
- size_2d_override_stretch: bool = false
- view_count: int = 1

- **render_target_clear_mode**: The clear mode when the sub-viewport is used as a render target. **Note:** This property is intended for 2D usage.
- **render_target_update_mode**: The update mode when the sub-viewport is used as a render target.
- **size**: The width and height of the sub-viewport. Must be set to a value greater than or equal to 2 pixels on both dimensions. Otherwise, nothing will be displayed. **Note:** If the parent node is a SubViewportContainer and its `SubViewportContainer.stretch` is `true`, the viewport size cannot be changed manually.
- **size_2d_override**: The 2D size override of the sub-viewport. If either the width or height is `0`, the override is disabled.
- **size_2d_override_stretch**: If `true`, the 2D size override affects stretch as well.
- **view_count**: The number of view layers we are rendering to. Set this to `2` to enable stereo rendering.

**Enums:**
**ClearMode:** CLEAR_MODE_ALWAYS=0, CLEAR_MODE_NEVER=1, CLEAR_MODE_ONCE=2
  - CLEAR_MODE_ALWAYS: Always clear the render target before drawing.
  - CLEAR_MODE_NEVER: Never clear the render target.
  - CLEAR_MODE_ONCE: Clear the render target on the next frame, then switch to `CLEAR_MODE_NEVER`.
**UpdateMode:** UPDATE_DISABLED=0, UPDATE_ONCE=1, UPDATE_WHEN_VISIBLE=2, UPDATE_WHEN_PARENT_VISIBLE=3, UPDATE_ALWAYS=4
  - UPDATE_DISABLED: Do not update the render target.
  - UPDATE_ONCE: Update the render target once, then switch to `UPDATE_DISABLED`.
  - UPDATE_WHEN_VISIBLE: Update the render target only when it is visible. This is the default value.
  - UPDATE_WHEN_PARENT_VISIBLE: Update the render target only when its parent is visible.
  - UPDATE_ALWAYS: Always update the render target.

