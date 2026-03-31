## CanvasLayer <- Node

CanvasItem-derived nodes that are direct or indirect children of a CanvasLayer will be drawn in that layer. The layer is a numeric index that defines the draw order. The default 2D scene renders with index `0`, so a CanvasLayer with index `-1` will be drawn below, and a CanvasLayer with index `1` will be drawn above. This order will hold regardless of the `CanvasItem.z_index` of the nodes within each layer. CanvasLayers can be hidden and they can also optionally follow the viewport. This makes them useful for HUDs like health bar overlays (on layers `1` and higher) or backgrounds (on layers `-1` and lower). **Note:** Embedded Windows are placed on layer `1024`. CanvasItems on layers `1025` and higher appear in front of embedded windows. **Note:** Each CanvasLayer is drawn on one specific Viewport and cannot be shared between multiple Viewports, see `custom_viewport`. When using multiple Viewports, for example in a split-screen game, you need to create an individual CanvasLayer for each Viewport you want it to be drawn on.

**Props:**
- custom_viewport: Node
- follow_viewport_enabled: bool = false
- follow_viewport_scale: float = 1.0
- layer: int = 1
- offset: Vector2 = Vector2(0, 0)
- rotation: float = 0.0
- scale: Vector2 = Vector2(1, 1)
- transform: Transform2D = Transform2D(1, 0, 0, 1, 0, 0)
- visible: bool = true

- **custom_viewport**: The custom Viewport node assigned to the CanvasLayer. If `null`, uses the default viewport instead.
- **follow_viewport_enabled**: If enabled, the CanvasLayer maintains its position in world space. If disabled, the CanvasLayer stays in a fixed position on the screen. Together with `follow_viewport_scale`, this can be used for a pseudo-3D effect.
- **follow_viewport_scale**: Scales the layer when using `follow_viewport_enabled`. Layers moving into the foreground should have increasing scales, while layers moving into the background should have decreasing scales.
- **layer**: Layer index for draw order. Lower values are drawn behind higher values. **Note:** If multiple CanvasLayers have the same layer index, CanvasItem children of one CanvasLayer are drawn behind the CanvasItem children of the other CanvasLayer. Which CanvasLayer is drawn in front is non-deterministic. **Note:** The layer index should be between `RenderingServer.CANVAS_LAYER_MIN` and `RenderingServer.CANVAS_LAYER_MAX` (inclusive). Any other value will wrap around.
- **offset**: The layer's base offset.
- **rotation**: The layer's rotation in radians.
- **scale**: The layer's scale.
- **transform**: The layer's transform.
- **visible**: If `false`, any CanvasItem under this CanvasLayer will be hidden. Unlike `CanvasItem.visible`, visibility of a CanvasLayer isn't propagated to underlying layers.

**Methods:**
- get_canvas() -> RID - Returns the RID of the canvas used by this layer.
- get_final_transform() -> Transform2D - Returns the transform from the CanvasLayers coordinate system to the Viewports coordinate system.
- hide() - Hides any CanvasItem under this CanvasLayer. This is equivalent to setting `visible` to `false`.
- show() - Shows any CanvasItem under this CanvasLayer. This is equivalent to setting `visible` to `true`.

**Signals:**
- visibility_changed - Emitted when visibility of the layer is changed. See `visible`.

