## SplitContainer <- Container

A container that arranges child controls horizontally or vertically and creates grabbers between them. The grabbers can be dragged around to change the size relations between the child controls.

**Props:**
- collapsed: bool = false
- drag_area_highlight_in_editor: bool = false
- drag_area_margin_begin: int = 0
- drag_area_margin_end: int = 0
- drag_area_offset: int = 0
- drag_nested_intersections: bool = false
- dragger_visibility: int (SplitContainer.DraggerVisibility) = 0
- dragging_enabled: bool = true
- split_offset: int = 0
- split_offsets: PackedInt32Array = PackedInt32Array(0)
- touch_dragger_enabled: bool = false
- vertical: bool = false

- **collapsed**: If `true`, the draggers will be disabled and the children will be sized as if all `split_offsets` were `0`.
- **drag_area_highlight_in_editor**: Highlights the drag area Rect2 so you can see where it is during development. The drag area is gold if `dragging_enabled` is `true`, and red if `false`.
- **drag_area_margin_begin**: Reduces the size of the drag area and split bar [theme_item split_bar_background] at the beginning of the container.
- **drag_area_margin_end**: Reduces the size of the drag area and split bar [theme_item split_bar_background] at the end of the container.
- **drag_area_offset**: Shifts the drag area in the axis of the container to prevent the drag area from overlapping the ScrollBar or other selectable Control of a child node.
- **drag_nested_intersections**: Adds extra draggers at the intersection of the draggers of two SplitContainers to allow dragging both at once. This must be set to `true` for both SplitContainers, and one needs to be a descendant of the other. They also must be orthogonal (their `vertical` are different) and the descendant must be next to at least one of the ancestor's draggers (within [theme_item minimum_grab_thickness]).
- **dragger_visibility**: Determines the dragger's visibility. This property does not determine whether dragging is enabled or not. Use `dragging_enabled` for that.
- **dragging_enabled**: Enables or disables split dragging.
- **split_offset**: The first element of `split_offsets`.
- **split_offsets**: Offsets for each dragger in pixels. Each one is the offset of the split between the Control nodes before and after the dragger, with `0` being the default position. The default position is based on the Control nodes expand flags and minimum sizes. See `Control.size_flags_horizontal`, `Control.size_flags_vertical`, and `Control.size_flags_stretch_ratio`. If none of the Control nodes before the dragger are expanded, the default position will be at the start of the SplitContainer. If none of the Control nodes after the dragger are expanded, the default position will be at the end of the SplitContainer. If the dragger is in between expanded Control nodes, the default position will be in the middle, based on the `Control.size_flags_stretch_ratio`s and minimum sizes. **Note:** If the split offsets cause Control nodes to overlap, the first split will take priority when resolving the positions.
- **touch_dragger_enabled**: If `true`, a touch-friendly drag handle will be enabled for better usability on smaller screens. Unlike the standard grabber, this drag handle overlaps the SplitContainer's children and does not affect their minimum separation. The standard grabber will no longer be drawn when this option is enabled.
- **vertical**: If `true`, the SplitContainer will arrange its children vertically, rather than horizontally. Can't be changed when using HSplitContainer and VSplitContainer.

**Methods:**
- clamp_split_offset(priority_index: int = 0) - Clamps the `split_offsets` values to ensure they are within valid ranges and do not overlap with each other. When overlaps occur, this method prioritizes one split offset (at index `priority_index`) by clamping any overlapping split offsets to it.
- get_drag_area_control() -> Control - Returns the drag area Control. For example, you can move a pre-configured button into the drag area Control so that it rides along with the split bar. Try setting the Button anchors to `center` prior to the `reparent()` call. **Note:** The drag area Control is drawn over the SplitContainer's children, so CanvasItem draw objects called from the Control and children added to the Control will also appear over the SplitContainer's children. Try setting `Control.mouse_filter` of custom children to `Control.MOUSE_FILTER_IGNORE` to prevent blocking the mouse from dragging if desired. **Warning:** This is a required internal node, removing and freeing it may cause a crash.
- get_drag_area_controls() -> Control[] - Returns an Array of the drag area Controls. These are the interactable Control nodes between each child. For example, this can be used to add a pre-configured button to a drag area Control so that it rides along with the split bar. Try setting the Button anchors to `center` prior to the `Node.reparent` call. **Note:** The drag area Controls are drawn over the SplitContainer's children, so CanvasItem draw objects called from a drag area and children added to it will also appear over the SplitContainer's children. Try setting `Control.mouse_filter` of custom children to `Control.MOUSE_FILTER_IGNORE` to prevent blocking the mouse from dragging if desired. **Warning:** These are required internal nodes, removing or freeing them may cause a crash.

**Signals:**
- drag_ended - Emitted when the user ends dragging.
- drag_started - Emitted when the user starts dragging.
- dragged(offset: int) - Emitted when any dragger is dragged by user.

**Enums:**
**DraggerVisibility:** DRAGGER_VISIBLE=0, DRAGGER_HIDDEN=1, DRAGGER_HIDDEN_COLLAPSED=2
  - DRAGGER_VISIBLE: The split dragger icon is always visible when [theme_item autohide] is `false`, otherwise visible only when the cursor hovers it. The size of the grabber icon determines the minimum [theme_item separation]. The dragger icon is automatically hidden if the length of the grabber icon is longer than the split bar.
  - DRAGGER_HIDDEN: The split dragger icon is never visible regardless of the value of [theme_item autohide]. The size of the grabber icon determines the minimum [theme_item separation].
  - DRAGGER_HIDDEN_COLLAPSED: The split dragger icon is not visible, and the split bar is collapsed to zero thickness.

