## VisibleOnScreenNotifier2D <- Node2D

VisibleOnScreenNotifier2D represents a rectangular region of 2D space. When any part of this region becomes visible on screen or in a viewport, it will emit a `screen_entered` signal, and likewise it will emit a `screen_exited` signal when no part of it remains visible. If you want a node to be enabled automatically when this region is visible on screen, use VisibleOnScreenEnabler2D. **Note:** VisibleOnScreenNotifier2D uses the render culling code to determine whether it's visible on screen, so it won't function unless `CanvasItem.visible` is set to `true`.

**Props:**
- rect: Rect2 = Rect2(-10, -10, 20, 20)
- show_rect: bool = true

- **rect**: The VisibleOnScreenNotifier2D's bounding rectangle.
- **show_rect**: If `true`, shows the rectangle area of `rect` in the editor with a translucent magenta fill. Unlike changing the visibility of the VisibleOnScreenNotifier2D, this does not affect the screen culling detection.

**Methods:**
- is_on_screen() -> bool - If `true`, the bounding rectangle is on the screen. **Note:** It takes one frame for the VisibleOnScreenNotifier2D's visibility to be determined once added to the scene tree, so this method will always return `false` right after it is instantiated, before the draw pass.

**Signals:**
- screen_entered - Emitted when the VisibleOnScreenNotifier2D enters the screen.
- screen_exited - Emitted when the VisibleOnScreenNotifier2D exits the screen.

