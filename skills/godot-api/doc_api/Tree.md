## Tree <- Control

A control used to show a set of internal TreeItems in a hierarchical structure. The tree items can be selected, expanded and collapsed. The tree can have multiple columns with custom controls like LineEdits, buttons and popups. It can be useful for structured displays and interactions. Trees are built via code, using TreeItem objects to create the structure. They have a single root, but multiple roots can be simulated with `hide_root`: To iterate over all the TreeItem objects in a Tree object, use `TreeItem.get_next` and `TreeItem.get_first_child` after getting the root through `get_root`. You can use `Object.free` on a TreeItem to remove it from the Tree. **Incremental search:** Like ItemList and PopupMenu, Tree supports searching within the list while the control is focused. Press a key that matches the first letter of an item's name to select the first item starting with the given letter. After that point, there are two ways to perform incremental search: 1) Press the same key again before the timeout duration to select the next item starting with the same letter. 2) Press letter keys that match the rest of the word before the timeout duration to match to select the item in question directly. Both of these actions will be reset to the beginning of the list if the timeout duration has passed since the last keystroke was registered. You can adjust the timeout duration by changing `ProjectSettings.gui/timers/incremental_search_max_interval_msec`.

**Props:**
- allow_reselect: bool = false
- allow_rmb_select: bool = false
- allow_search: bool = true
- auto_tooltip: bool = true
- clip_contents: bool = true
- column_titles_visible: bool = false
- columns: int = 1
- drop_mode_flags: int = 0
- enable_drag_unfolding: bool = true
- enable_recursive_folding: bool = true
- focus_mode: int (Control.FocusMode) = 2
- hide_folding: bool = false
- hide_root: bool = false
- scroll_hint_mode: int (Tree.ScrollHintMode) = 0
- scroll_horizontal_enabled: bool = true
- scroll_vertical_enabled: bool = true
- select_mode: int (Tree.SelectMode) = 0
- tile_scroll_hint: bool = false

- **allow_reselect**: If `true`, the currently selected cell may be selected again.
- **allow_rmb_select**: If `true`, a right mouse button click can select items.
- **allow_search**: If `true`, allows navigating the Tree with letter keys through incremental search.
- **auto_tooltip**: If `true`, tree items with no tooltip assigned display their text as their tooltip. See also `TreeItem.get_tooltip_text` and `TreeItem.get_button_tooltip_text`.
- **column_titles_visible**: If `true`, column titles are visible.
- **columns**: The number of columns. Prints an error and does not allow setting the columns during mouse selection.
- **drop_mode_flags**: The drop mode as an OR combination of flags. See `DropModeFlags` constants. Once dropping is done, reverts to `DROP_MODE_DISABLED`. Setting this during `Control._can_drop_data` is recommended. This controls the drop sections, i.e. the decision and drawing of possible drop locations based on the mouse position.
- **enable_drag_unfolding**: If `true`, tree items will unfold when hovered over during a drag-and-drop. The delay for when this happens is dictated by [theme_item dragging_unfold_wait_msec].
- **enable_recursive_folding**: If `true`, recursive folding is enabled for this Tree. Holding down [kbd]Shift[/kbd] while clicking the fold arrow or using `ui_right`/`ui_left` shortcuts collapses or uncollapses the TreeItem and all its descendants.
- **hide_folding**: If `true`, the folding arrow is hidden.
- **hide_root**: If `true`, the tree's root is hidden.
- **scroll_hint_mode**: The way which scroll hints (indicators that show that the content can still be scrolled in a certain direction) will be shown.
- **scroll_horizontal_enabled**: If `true`, enables horizontal scrolling.
- **scroll_vertical_enabled**: If `true`, enables vertical scrolling.
- **select_mode**: Allows single or multiple selection. See the `SelectMode` constants.
- **tile_scroll_hint**: If `true`, the scroll hint texture will be tiled instead of stretched. See `scroll_hint_mode`.

**Methods:**
- clear() - Clears the tree. This removes all items. Prints an error and does not allow clearing the tree if called during mouse selection.
- create_item(parent: TreeItem = null, index: int = -1) -> TreeItem - Creates an item in the tree and adds it as a child of `parent`, which can be either a valid TreeItem or `null`. If `parent` is `null`, the root item will be the parent, or the new item will be the root itself if the tree is empty. The new item will be the `index`-th child of parent, or it will be the last child if there are not enough siblings. Prints an error and returns `null` if called during mouse selection, or if the `parent` does not belong to this tree.
- deselect_all() - Deselects all tree items (rows and columns). In `SELECT_MULTI` mode also removes selection cursor.
- edit_selected(force_edit: bool = false) -> bool - Edits the selected tree item as if it was clicked. Either the item must be set editable with `TreeItem.set_editable` or `force_edit` must be `true`. Returns `true` if the item could be edited. Fails if no item is selected.
- ensure_cursor_is_visible() - Makes the currently focused cell visible. This will scroll the tree if necessary. In `SELECT_ROW` mode, this will not do horizontal scrolling, as all the cells in the selected row is focused logically. **Note:** Despite the name of this method, the focus cursor itself is only visible in `SELECT_MULTI` mode.
- get_button_id_at_position(position: Vector2) -> int - Returns the button ID at `position`, or -1 if no button is there.
- get_column_at_position(position: Vector2) -> int - Returns the column index at `position`, or -1 if no item is there.
- get_column_expand_ratio(column: int) -> int - Returns the expand ratio assigned to the column.
- get_column_title(column: int) -> String - Returns the column's title.
- get_column_title_alignment(column: int) -> int - Returns the column title alignment.
- get_column_title_direction(column: int) -> int - Returns column title base writing direction.
- get_column_title_language(column: int) -> String - Returns column title language code.
- get_column_title_tooltip_text(column: int) -> String - Returns the column title's tooltip text.
- get_column_width(column: int) -> int - Returns the column's width in pixels.
- get_custom_popup_rect() -> Rect2 - Returns the rectangle for custom popups. Helper to create custom cell controls that display a popup. See `TreeItem.set_cell_mode`.
- get_drop_section_at_position(position: Vector2) -> int - Returns the drop section at `position`, or -100 if no item is there. Values -1, 0, or 1 will be returned for the "above item", "on item", and "below item" drop sections, respectively. See `DropModeFlags` for a description of each drop section. To get the item which the returned drop section is relative to, use `get_item_at_position`.
- get_edited() -> TreeItem - Returns the currently edited item. Can be used with `item_edited` to get the item that was modified.
- get_edited_column() -> int - Returns the column for the currently edited item.
- get_item_area_rect(item: TreeItem, column: int = -1, button_index: int = -1) -> Rect2 - Returns the rectangle area for the specified TreeItem. If `column` is specified, only get the position and size of that column, otherwise get the rectangle containing all columns. If a button index is specified, the rectangle of that button will be returned.
- get_item_at_position(position: Vector2) -> TreeItem - Returns the tree item at the specified position (relative to the tree origin position).
- get_next_selected(from: TreeItem) -> TreeItem - Returns the next selected TreeItem after the given one, or `null` if the end is reached. If `from` is `null`, this returns the first selected item.
- get_pressed_button() -> int - Returns the last pressed button's index.
- get_root() -> TreeItem - Returns the tree's root item, or `null` if the tree is empty.
- get_scroll() -> Vector2 - Returns the current scrolling position.
- get_selected() -> TreeItem - Returns the currently focused item, or `null` if no item is focused. In `SELECT_ROW` and `SELECT_SINGLE` modes, the focused item is same as the selected item. In `SELECT_MULTI` mode, the focused item is the item under the focus cursor, not necessarily selected. To get the currently selected item(s), use `get_next_selected`.
- get_selected_column() -> int - Returns the currently focused column, or -1 if no column is focused. In `SELECT_SINGLE` mode, the focused column is the selected column. In `SELECT_ROW` mode, the focused column is always 0 if any item is selected. In `SELECT_MULTI` mode, the focused column is the column under the focus cursor, and there are not necessarily any column selected. To tell whether a column of an item is selected, use `TreeItem.is_selected`.
- is_column_clipping_content(column: int) -> bool - Returns `true` if the column has enabled clipping (see `set_column_clip_content`).
- is_column_expanding(column: int) -> bool - Returns `true` if the column has enabled expanding (see `set_column_expand`).
- scroll_to_item(item: TreeItem, center_on_item: bool = false) - Causes the Tree to jump to the specified TreeItem.
- set_column_clip_content(column: int, enable: bool) - Allows to enable clipping for column's content, making the content size ignored.
- set_column_custom_minimum_width(column: int, min_width: int) - Overrides the calculated minimum width of a column. It can be set to `0` to restore the default behavior. Columns that have the "Expand" flag will use their "min_width" in a similar fashion to `Control.size_flags_stretch_ratio`.
- set_column_expand(column: int, expand: bool) - If `true`, the column will have the "Expand" flag of Control. Columns that have the "Expand" flag will use their expand ratio in a similar fashion to `Control.size_flags_stretch_ratio` (see `set_column_expand_ratio`).
- set_column_expand_ratio(column: int, ratio: int) - Sets the relative expand ratio for a column. See `set_column_expand`.
- set_column_title(column: int, title: String) - Sets the title of a column.
- set_column_title_alignment(column: int, title_alignment: int) - Sets the column title alignment. Note that `@GlobalScope.HORIZONTAL_ALIGNMENT_FILL` is not supported for column titles.
- set_column_title_direction(column: int, direction: int) - Sets column title base writing direction.
- set_column_title_language(column: int, language: String) - Sets the language code of the given `column`'s title to `language`. This is used for line-breaking and text shaping algorithms. If `language` is empty, the current locale is used.
- set_column_title_tooltip_text(column: int, tooltip_text: String) - Sets the column title's tooltip text.
- set_selected(item: TreeItem, column: int) - Selects the specified TreeItem and column.

**Signals:**
- button_clicked(item: TreeItem, column: int, id: int, mouse_button_index: int) - Emitted when a button on the tree was pressed (see `TreeItem.add_button`).
- cell_selected - Emitted when a cell is selected.
- check_propagated_to_item(item: TreeItem, column: int) - Emitted when `TreeItem.propagate_check` is called. Connect to this signal to process the items that are affected when `TreeItem.propagate_check` is invoked. The order that the items affected will be processed is as follows: the item that invoked the method, children of that item, and finally parents of that item.
- column_title_clicked(column: int, mouse_button_index: int) - Emitted when a column's title is clicked with either `MOUSE_BUTTON_LEFT` or `MOUSE_BUTTON_RIGHT`.
- custom_item_clicked(mouse_button_index: int) - Emitted when an item with `TreeItem.CELL_MODE_CUSTOM` is clicked with a mouse button.
- custom_popup_edited(arrow_clicked: bool) - Emitted when a cell with the `TreeItem.CELL_MODE_CUSTOM` is clicked to be edited.
- empty_clicked(click_position: Vector2, mouse_button_index: int) - Emitted when a mouse button is clicked in the empty space of the tree.
- item_activated - Emitted when an item is double-clicked, or selected with a `ui_accept` input event (e.g. using [kbd]Enter[/kbd] or [kbd]Space[/kbd] on the keyboard).
- item_collapsed(item: TreeItem) - Emitted when an item is expanded or collapsed by clicking on the folding arrow or through code. **Note:** Despite its name, this signal is also emitted when an item is expanded.
- item_edited - Emitted when an item is edited.
- item_icon_double_clicked - Emitted when an item's icon is double-clicked. For a signal that emits when any part of the item is double-clicked, see `item_activated`.
- item_mouse_selected(mouse_position: Vector2, mouse_button_index: int) - Emitted when an item is selected with a mouse button.
- item_selected - Emitted when an item is selected.
- multi_selected(item: TreeItem, column: int, selected: bool) - Emitted instead of `item_selected` if `select_mode` is set to `SELECT_MULTI`.
- nothing_selected - Emitted when a left mouse button click does not select any item.

**Enums:**
**SelectMode:** SELECT_SINGLE=0, SELECT_ROW=1, SELECT_MULTI=2
  - SELECT_SINGLE: Allows selection of a single cell at a time. From the perspective of items, only a single item is allowed to be selected. And there is only one column selected in the selected item. The focus cursor is always hidden in this mode, but it is positioned at the current selection, making the currently selected item the currently focused item.
  - SELECT_ROW: Allows selection of a single row at a time. From the perspective of items, only a single items is allowed to be selected. And all the columns are selected in the selected item. The focus cursor is always hidden in this mode, but it is positioned at the first column of the current selection, making the currently selected item the currently focused item.
  - SELECT_MULTI: Allows selection of multiple cells at the same time. From the perspective of items, multiple items are allowed to be selected. And there can be multiple columns selected in each selected item. The focus cursor is visible in this mode, the item or column under the cursor is not necessarily selected.
**DropModeFlags:** DROP_MODE_DISABLED=0, DROP_MODE_ON_ITEM=1, DROP_MODE_INBETWEEN=2
  - DROP_MODE_DISABLED: Disables all drop sections, but still allows to detect the "on item" drop section by `get_drop_section_at_position`. **Note:** This is the default flag, it has no effect when combined with other flags.
  - DROP_MODE_ON_ITEM: Enables the "on item" drop section. This drop section covers the entire item. When combined with `DROP_MODE_INBETWEEN`, this drop section halves the height and stays centered vertically.
  - DROP_MODE_INBETWEEN: Enables "above item" and "below item" drop sections. The "above item" drop section covers the top half of the item, and the "below item" drop section covers the bottom half. When combined with `DROP_MODE_ON_ITEM`, these drop sections halves the height and stays on top / bottom accordingly.
**ScrollHintMode:** SCROLL_HINT_MODE_DISABLED=0, SCROLL_HINT_MODE_BOTH=1, SCROLL_HINT_MODE_TOP=2, SCROLL_HINT_MODE_BOTTOM=3
  - SCROLL_HINT_MODE_DISABLED: Scroll hints will never be shown.
  - SCROLL_HINT_MODE_BOTH: Scroll hints will be shown at the top and bottom.
  - SCROLL_HINT_MODE_TOP: Only the top scroll hint will be shown.
  - SCROLL_HINT_MODE_BOTTOM: Only the bottom scroll hint will be shown.

