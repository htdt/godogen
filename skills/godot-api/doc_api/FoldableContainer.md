## FoldableContainer <- Container

A container that can be expanded/collapsed, with a title that can be filled with controls, such as buttons. This is also called an accordion. The title can be positioned at the top or bottom of the container. The container can be expanded or collapsed by clicking the title or by pressing `ui_accept` when focused. Child control nodes are hidden when the container is collapsed. Ignores non-control children. A FoldableContainer can be grouped with other FoldableContainers so that only one of them can be opened at a time; see `foldable_group` and FoldableGroup.

**Props:**
- focus_mode: int (Control.FocusMode) = 2
- foldable_group: FoldableGroup
- folded: bool = false
- language: String = ""
- mouse_filter: int (Control.MouseFilter) = 0
- title: String = ""
- title_alignment: int (HorizontalAlignment) = 0
- title_position: int (FoldableContainer.TitlePosition) = 0
- title_text_direction: int (Control.TextDirection) = 0
- title_text_overrun_behavior: int (TextServer.OverrunBehavior) = 0

- **foldable_group**: The FoldableGroup associated with the container. When multiple FoldableContainer nodes share the same group, only one of them is allowed to be unfolded.
- **folded**: If `true`, the container will become folded and will hide all its children.
- **language**: Language code used for text shaping algorithms. If left empty, the current locale is used instead.
- **title**: The container's title text.
- **title_alignment**: Title's horizontal text alignment.
- **title_position**: Title's position.
- **title_text_direction**: Title text writing direction.
- **title_text_overrun_behavior**: Defines the behavior of the title when the text is longer than the available space.

**Methods:**
- add_title_bar_control(control: Control) - Adds a Control that will be placed next to the container's title, obscuring the clickable area. Prime usage is adding Button nodes, but it can be any Control. The control will be added as a child of this container and removed from previous parent if necessary. The controls will be placed aligned to the right, with the first added control being the leftmost one.
- expand() - Expands the container and emits `folding_changed`.
- fold() - Folds the container and emits `folding_changed`.
- remove_title_bar_control(control: Control) - Removes a Control added with `add_title_bar_control`. The node is not freed automatically, you need to use `Node.queue_free`.

**Signals:**
- folding_changed(is_folded: bool) - Emitted when the container is folded/expanded.

**Enums:**
**TitlePosition:** POSITION_TOP=0, POSITION_BOTTOM=1
  - POSITION_TOP: Makes the title appear at the top of the container.
  - POSITION_BOTTOM: Makes the title appear at the bottom of the container. Also makes all StyleBoxes flipped vertically.

