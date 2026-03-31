## Container <- Control

Base class for all GUI containers. A Container automatically arranges its child controls in a certain way. This class can be inherited to make custom container types.

**Props:**
- accessibility_region: bool = false
- mouse_filter: int (Control.MouseFilter) = 1

- **accessibility_region**: If `true`, this container is marked as a region for accessibility. Use `Control.accessibility_name` to give the region a descriptive name. Screen readers can navigate between regions using landmark navigation.

**Methods:**
- _get_allowed_size_flags_horizontal() -> PackedInt32Array - Implement to return a list of allowed horizontal `Control.SizeFlags` for child nodes. This doesn't technically prevent the usages of any other size flags, if your implementation requires that. This only limits the options available to the user in the Inspector dock. **Note:** Having no size flags is equal to having `Control.SIZE_SHRINK_BEGIN`. As such, this value is always implicitly allowed.
- _get_allowed_size_flags_vertical() -> PackedInt32Array - Implement to return a list of allowed vertical `Control.SizeFlags` for child nodes. This doesn't technically prevent the usages of any other size flags, if your implementation requires that. This only limits the options available to the user in the Inspector dock. **Note:** Having no size flags is equal to having `Control.SIZE_SHRINK_BEGIN`. As such, this value is always implicitly allowed.
- fit_child_in_rect(child: Control, rect: Rect2) - Fit a child control in a given rect. This is mainly a helper for creating custom container classes.
- queue_sort() - Queue resort of the contained children. This is called automatically anyway, but can be called upon request.

**Signals:**
- pre_sort_children - Emitted when children are going to be sorted.
- sort_children - Emitted when sorting the children is needed.

**Enums:**
**Constants:** NOTIFICATION_PRE_SORT_CHILDREN=50, NOTIFICATION_SORT_CHILDREN=51
  - NOTIFICATION_PRE_SORT_CHILDREN: Notification just before children are going to be sorted, in case there's something to process beforehand.
  - NOTIFICATION_SORT_CHILDREN: Notification for when sorting the children, it must be obeyed immediately.

