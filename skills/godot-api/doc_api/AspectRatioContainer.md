## AspectRatioContainer <- Container

A container type that arranges its child controls in a way that preserves their proportions automatically when the container is resized. Useful when a container has a dynamic size and the child nodes must adjust their sizes accordingly without losing their aspect ratios.

**Props:**
- alignment_horizontal: int (AspectRatioContainer.AlignmentMode) = 1
- alignment_vertical: int (AspectRatioContainer.AlignmentMode) = 1
- ratio: float = 1.0
- stretch_mode: int (AspectRatioContainer.StretchMode) = 2

- **alignment_horizontal**: Specifies the horizontal relative position of child controls.
- **alignment_vertical**: Specifies the vertical relative position of child controls.
- **ratio**: The aspect ratio to enforce on child controls. This is the width divided by the height. The ratio depends on the `stretch_mode`.
- **stretch_mode**: The stretch mode used to align child controls.

**Enums:**
**StretchMode:** STRETCH_WIDTH_CONTROLS_HEIGHT=0, STRETCH_HEIGHT_CONTROLS_WIDTH=1, STRETCH_FIT=2, STRETCH_COVER=3
  - STRETCH_WIDTH_CONTROLS_HEIGHT: The height of child controls is automatically adjusted based on the width of the container.
  - STRETCH_HEIGHT_CONTROLS_WIDTH: The width of child controls is automatically adjusted based on the height of the container.
  - STRETCH_FIT: The bounding rectangle of child controls is automatically adjusted to fit inside the container while keeping the aspect ratio.
  - STRETCH_COVER: The width and height of child controls is automatically adjusted to make their bounding rectangle cover the entire area of the container while keeping the aspect ratio. When the bounding rectangle of child controls exceed the container's size and `Control.clip_contents` is enabled, this allows to show only the container's area restricted by its own bounding rectangle.
**AlignmentMode:** ALIGNMENT_BEGIN=0, ALIGNMENT_CENTER=1, ALIGNMENT_END=2
  - ALIGNMENT_BEGIN: Aligns child controls with the beginning (left or top) of the container.
  - ALIGNMENT_CENTER: Aligns child controls with the center of the container.
  - ALIGNMENT_END: Aligns child controls with the end (right or bottom) of the container.

