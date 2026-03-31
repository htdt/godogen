## FlowContainer <- Container

A container that arranges its child controls horizontally or vertically and wraps them around at the borders. This is similar to how text in a book wraps around when no more words can fit on a line.

**Props:**
- alignment: int (FlowContainer.AlignmentMode) = 0
- last_wrap_alignment: int (FlowContainer.LastWrapAlignmentMode) = 0
- reverse_fill: bool = false
- vertical: bool = false

- **alignment**: The alignment of the container's children (must be one of `ALIGNMENT_BEGIN`, `ALIGNMENT_CENTER`, or `ALIGNMENT_END`).
- **last_wrap_alignment**: The wrap behavior of the last, partially filled row or column (must be one of `LAST_WRAP_ALIGNMENT_INHERIT`, `LAST_WRAP_ALIGNMENT_BEGIN`, `LAST_WRAP_ALIGNMENT_CENTER`, or `LAST_WRAP_ALIGNMENT_END`).
- **reverse_fill**: If `true`, reverses fill direction. Horizontal FlowContainers will fill rows bottom to top, vertical FlowContainers will fill columns right to left. When using a vertical FlowContainer with a right to left `Control.layout_direction`, columns will fill left to right instead.
- **vertical**: If `true`, the FlowContainer will arrange its children vertically, rather than horizontally. Can't be changed when using HFlowContainer and VFlowContainer.

**Methods:**
- get_line_count() -> int - Returns the current line count.

**Enums:**
**AlignmentMode:** ALIGNMENT_BEGIN=0, ALIGNMENT_CENTER=1, ALIGNMENT_END=2
  - ALIGNMENT_BEGIN: The child controls will be arranged at the beginning of the container, i.e. top if orientation is vertical, left if orientation is horizontal (right for RTL layout).
  - ALIGNMENT_CENTER: The child controls will be centered in the container.
  - ALIGNMENT_END: The child controls will be arranged at the end of the container, i.e. bottom if orientation is vertical, right if orientation is horizontal (left for RTL layout).
**LastWrapAlignmentMode:** LAST_WRAP_ALIGNMENT_INHERIT=0, LAST_WRAP_ALIGNMENT_BEGIN=1, LAST_WRAP_ALIGNMENT_CENTER=2, LAST_WRAP_ALIGNMENT_END=3
  - LAST_WRAP_ALIGNMENT_INHERIT: The last partially filled row or column will wrap aligned to the previous row or column in accordance with `alignment`.
  - LAST_WRAP_ALIGNMENT_BEGIN: The last partially filled row or column will wrap aligned to the beginning of the previous row or column.
  - LAST_WRAP_ALIGNMENT_CENTER: The last partially filled row or column will wrap aligned to the center of the previous row or column.
  - LAST_WRAP_ALIGNMENT_END: The last partially filled row or column will wrap aligned to the end of the previous row or column.

