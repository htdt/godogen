## ProgressBar <- Range

A control used for visual representation of a percentage. Shows the fill percentage in the center. Can also be used to show indeterminate progress. For more fill modes, use TextureProgressBar instead.

**Props:**
- editor_preview_indeterminate: bool
- fill_mode: int = 0
- indeterminate: bool = false
- show_percentage: bool = true

- **editor_preview_indeterminate**: If `false`, the `indeterminate` animation will be paused in the editor.
- **fill_mode**: The fill direction. See `FillMode` for possible values.
- **indeterminate**: When set to `true`, the progress bar indicates that something is happening with an animation, but does not show the fill percentage or value.
- **show_percentage**: If `true`, the fill percentage is displayed on the bar.

**Enums:**
**FillMode:** FILL_BEGIN_TO_END=0, FILL_END_TO_BEGIN=1, FILL_TOP_TO_BOTTOM=2, FILL_BOTTOM_TO_TOP=3
  - FILL_BEGIN_TO_END: The progress bar fills from begin to end horizontally, according to the language direction. If `Control.is_layout_rtl` returns `false`, it fills from left to right, and if it returns `true`, it fills from right to left.
  - FILL_END_TO_BEGIN: The progress bar fills from end to begin horizontally, according to the language direction. If `Control.is_layout_rtl` returns `false`, it fills from right to left, and if it returns `true`, it fills from left to right.
  - FILL_TOP_TO_BOTTOM: The progress fills from top to bottom.
  - FILL_BOTTOM_TO_TOP: The progress fills from bottom to top.

