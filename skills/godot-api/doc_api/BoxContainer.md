## BoxContainer <- Container

A container that arranges its child controls horizontally or vertically, rearranging them automatically when their minimum size changes.

**Props:**
- alignment: int (BoxContainer.AlignmentMode) = 0
- vertical: bool = false

- **alignment**: The alignment of the container's children (must be one of `ALIGNMENT_BEGIN`, `ALIGNMENT_CENTER`, or `ALIGNMENT_END`).
- **vertical**: If `true`, the BoxContainer will arrange its children vertically, rather than horizontally. Can't be changed when using HBoxContainer and VBoxContainer.

**Methods:**
- add_spacer(begin: bool) -> Control - Adds a Control node to the box as a spacer. If `begin` is `true`, it will insert the Control node in front of all other children.

**Enums:**
**AlignmentMode:** ALIGNMENT_BEGIN=0, ALIGNMENT_CENTER=1, ALIGNMENT_END=2
  - ALIGNMENT_BEGIN: The child controls will be arranged at the beginning of the container, i.e. top if orientation is vertical, left if orientation is horizontal (right for RTL layout).
  - ALIGNMENT_CENTER: The child controls will be centered in the container.
  - ALIGNMENT_END: The child controls will be arranged at the end of the container, i.e. bottom if orientation is vertical, right if orientation is horizontal (left for RTL layout).

