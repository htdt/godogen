## StyleBox <- Resource

StyleBox is an abstract base class for drawing stylized boxes for UI elements. It is used for panels, buttons, LineEdit backgrounds, Tree backgrounds, etc. and also for testing a transparency mask for pointer signals. If mask test fails on a StyleBox assigned as mask to a control, clicks and motion signals will go through it to the one below. **Note:** For control nodes that have *Theme Properties*, the `focus` StyleBox is displayed over the `normal`, `hover` or `pressed` StyleBox. This makes the `focus` StyleBox more reusable across different nodes.

**Props:**
- content_margin_bottom: float = -1.0
- content_margin_left: float = -1.0
- content_margin_right: float = -1.0
- content_margin_top: float = -1.0

- **content_margin_bottom**: The bottom margin for the contents of this style box. Increasing this value reduces the space available to the contents from the bottom. If this value is negative, it is ignored and a child-specific margin is used instead. For example, for StyleBoxFlat, the border thickness (if any) is used instead. It is up to the code using this style box to decide what these contents are: for example, a Button respects this content margin for the textual contents of the button. `get_margin` should be used to fetch this value as consumer instead of reading these properties directly. This is because it correctly respects negative values and the fallback mentioned above.
- **content_margin_left**: The left margin for the contents of this style box. Increasing this value reduces the space available to the contents from the left. Refer to `content_margin_bottom` for extra considerations.
- **content_margin_right**: The right margin for the contents of this style box. Increasing this value reduces the space available to the contents from the right. Refer to `content_margin_bottom` for extra considerations.
- **content_margin_top**: The top margin for the contents of this style box. Increasing this value reduces the space available to the contents from the top. Refer to `content_margin_bottom` for extra considerations.

**Methods:**
- _draw(to_canvas_item: RID, rect: Rect2)
- _get_draw_rect(rect: Rect2) -> Rect2
- _get_minimum_size() -> Vector2 - Virtual method to be implemented by the user. Returns a custom minimum size that the stylebox must respect when drawing. By default `get_minimum_size` only takes content margins into account. This method can be overridden to add another size restriction. A combination of the default behavior and the output of this method will be used, to account for both sizes.
- _test_mask(point: Vector2, rect: Rect2) -> bool
- draw(canvas_item: RID, rect: Rect2) - Draws this stylebox using a canvas item identified by the given RID. The RID value can either be the result of `CanvasItem.get_canvas_item` called on an existing CanvasItem-derived node, or directly from creating a canvas item in the RenderingServer with `RenderingServer.canvas_item_create`.
- get_content_margin(margin: int) -> float - Returns the default margin of the specified `Side`.
- get_current_item_drawn() -> CanvasItem - Returns the CanvasItem that handles its `CanvasItem.NOTIFICATION_DRAW` or `CanvasItem._draw` callback at this moment.
- get_margin(margin: int) -> float - Returns the content margin offset for the specified `Side`. Positive values reduce size inwards, unlike Control's margin values.
- get_minimum_size() -> Vector2 - Returns the minimum size that this stylebox can be shrunk to.
- get_offset() -> Vector2 - Returns the "offset" of a stylebox. This helper function returns a value equivalent to `Vector2(style.get_margin(MARGIN_LEFT), style.get_margin(MARGIN_TOP))`.
- set_content_margin(margin: int, offset: float) - Sets the default value of the specified `Side` to `offset` pixels.
- set_content_margin_all(offset: float) - Sets the default margin to `offset` pixels for all sides.
- test_mask(point: Vector2, rect: Rect2) -> bool - Test a position in a rectangle, return whether it passes the mask test.

