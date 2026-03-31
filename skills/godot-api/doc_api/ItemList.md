## ItemList <- Control

This control provides a vertical list of selectable items that may be in a single or in multiple columns, with each item having options for text and an icon. Tooltips are supported and may be different for every item in the list. Selectable items in the list may be selected or deselected and multiple selection may be enabled. Selection with right mouse button may also be enabled to allow use of popup context menus. Items may also be "activated" by double-clicking them or by pressing [kbd]Enter[/kbd]. Item text only supports single-line strings. Newline characters (e.g. `\n`) in the string won't produce a newline. Text wrapping is enabled in `ICON_MODE_TOP` mode, but the column's width is adjusted to fully fit its content by default. You need to set `fixed_column_width` greater than zero to wrap the text. All `set_*` methods allow negative item indices, i.e. `-1` to access the last item, `-2` to select the second-to-last item, and so on. **Incremental search:** Like PopupMenu and Tree, ItemList supports searching within the list while the control is focused. Press a key that matches the first letter of an item's name to select the first item starting with the given letter. After that point, there are two ways to perform incremental search: 1) Press the same key again before the timeout duration to select the next item starting with the same letter. 2) Press letter keys that match the rest of the word before the timeout duration to match to select the item in question directly. Both of these actions will be reset to the beginning of the list if the timeout duration has passed since the last keystroke was registered. You can adjust the timeout duration by changing `ProjectSettings.gui/timers/incremental_search_max_interval_msec`.

**Props:**
- allow_reselect: bool = false
- allow_rmb_select: bool = false
- allow_search: bool = true
- auto_height: bool = false
- auto_width: bool = false
- clip_contents: bool = true
- fixed_column_width: int = 0
- fixed_icon_size: Vector2i = Vector2i(0, 0)
- focus_mode: int (Control.FocusMode) = 2
- icon_mode: int (ItemList.IconMode) = 1
- icon_scale: float = 1.0
- item_count: int = 0
- item_{index}/disabled: bool = false
- item_{index}/icon: Texture2D
- item_{index}/selectable: bool = true
- item_{index}/text: String = ""
- max_columns: int = 1
- max_text_lines: int = 1
- same_column_width: bool = false
- scroll_hint_mode: int (ItemList.ScrollHintMode) = 0
- select_mode: int (ItemList.SelectMode) = 0
- text_overrun_behavior: int (TextServer.OverrunBehavior) = 3
- tile_scroll_hint: bool = false
- wraparound_items: bool = true

- **allow_reselect**: If `true`, the currently selected item can be selected again.
- **allow_rmb_select**: If `true`, right mouse button click can select items.
- **allow_search**: If `true`, allows navigating the ItemList with letter keys through incremental search.
- **auto_height**: If `true`, the control will automatically resize the height to fit its content.
- **auto_width**: If `true`, the control will automatically resize the width to fit its content.
- **fixed_column_width**: The width all columns will be adjusted to. A value of zero disables the adjustment, each item will have a width equal to the width of its content and the columns will have an uneven width.
- **fixed_icon_size**: The size all icons will be adjusted to. If either X or Y component is not greater than zero, icon size won't be affected.
- **icon_mode**: The icon position, whether above or to the left of the text. See the `IconMode` constants.
- **icon_scale**: The scale of icon applied after `fixed_icon_size` and transposing takes effect.
- **item_count**: The number of items currently in the list.
- **item_{index}/disabled**: If `true`, the item at `index` is disabled. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **item_{index}/icon**: The icon of the item at `index`. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **item_{index}/selectable**: If `true`, the item at `index` is selectable. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **item_{index}/text**: The text of the item at `index`. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **max_columns**: Maximum columns the list will have. If greater than zero, the content will be split among the specified columns. A value of zero means unlimited columns, i.e. all items will be put in the same row.
- **max_text_lines**: Maximum lines of text allowed in each item. Space will be reserved even when there is not enough lines of text to display. **Note:** This property takes effect only when `icon_mode` is `ICON_MODE_TOP`. To make the text wrap, `fixed_column_width` should be greater than zero.
- **same_column_width**: Whether all columns will have the same width. If `true`, the width is equal to the largest column width of all columns.
- **scroll_hint_mode**: The way which scroll hints (indicators that show that the content can still be scrolled in a certain direction) will be shown.
- **select_mode**: Allows single or multiple item selection. See the `SelectMode` constants.
- **text_overrun_behavior**: The clipping behavior when the text exceeds an item's bounding rectangle.
- **tile_scroll_hint**: If `true`, the scroll hint texture will be tiled instead of stretched. See `scroll_hint_mode`.
- **wraparound_items**: If `true`, the control will automatically move items into a new row to fit its content. See also HFlowContainer for this behavior. If `false`, the control will add a horizontal scrollbar to make all items visible.

**Methods:**
- add_icon_item(icon: Texture2D, selectable: bool = true) -> int - Adds an item to the item list with no text, only an icon. Returns the index of an added item.
- add_item(text: String, icon: Texture2D = null, selectable: bool = true) -> int - Adds an item to the item list with specified text. Returns the index of an added item. Specify an `icon`, or use `null` as the `icon` for a list item with no icon. If `selectable` is `true`, the list item will be selectable.
- center_on_current(center_verically: bool = true, center_horizontally: bool = true) - Ensures the currently selected item (the first selected item if multiple selection is enabled) is visible, adjusting the scroll position as necessary to place the item at the center of the list if possible. See also `ensure_current_is_visible`. Fails and prints an error if both arguments are `false`.
- clear() - Removes all items from the list.
- deselect(idx: int) - Ensures the item associated with the specified index is not selected.
- deselect_all() - Ensures there are no items selected.
- ensure_current_is_visible() - Ensures the currently selected item (the first selected item if multiple selection is enabled) is visible, adjusting the scroll position as necessary. See also `center_on_current`.
- force_update_list_size() - Forces an update to the list size based on its items. This happens automatically whenever size of the items, or other relevant settings like `auto_height`, change. The method can be used to trigger the update ahead of next drawing pass.
- get_h_scroll_bar() -> HScrollBar - Returns the horizontal scrollbar. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `CanvasItem.visible` property.
- get_item_at_position(position: Vector2, exact: bool = false) -> int - Returns the item index at the given `position`. When there is no item at that point, -1 will be returned if `exact` is `true`, and the closest item index will be returned otherwise. **Note:** The returned value is unreliable if called right after modifying the ItemList, before it redraws in the next frame.
- get_item_auto_translate_mode(idx: int) -> int - Returns item's auto translate mode.
- get_item_custom_bg_color(idx: int) -> Color - Returns the custom background color of the item specified by `idx` index.
- get_item_custom_fg_color(idx: int) -> Color - Returns the custom foreground color of the item specified by `idx` index.
- get_item_icon(idx: int) -> Texture2D - Returns the icon associated with the specified index.
- get_item_icon_modulate(idx: int) -> Color - Returns a Color modulating item's icon at the specified index.
- get_item_icon_region(idx: int) -> Rect2 - Returns the region of item's icon used. The whole icon will be used if the region has no area.
- get_item_language(idx: int) -> String - Returns item's text language code.
- get_item_metadata(idx: int) -> Variant - Returns the metadata value of the specified index.
- get_item_rect(idx: int, expand: bool = true) -> Rect2 - Returns the position and size of the item with the specified index, in the coordinate system of the ItemList node. If `expand` is `true` the last column expands to fill the rest of the row. **Note:** The returned value is unreliable if called right after modifying the ItemList, before it redraws in the next frame.
- get_item_text(idx: int) -> String - Returns the text associated with the specified index.
- get_item_text_direction(idx: int) -> int - Returns item's text base writing direction.
- get_item_tooltip(idx: int) -> String - Returns the tooltip hint associated with the specified index.
- get_selected_items() -> PackedInt32Array - Returns an array with the indexes of the selected items.
- get_v_scroll_bar() -> VScrollBar - Returns the vertical scrollbar. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `CanvasItem.visible` property.
- is_anything_selected() -> bool - Returns `true` if one or more items are selected.
- is_item_disabled(idx: int) -> bool - Returns `true` if the item at the specified index is disabled.
- is_item_icon_transposed(idx: int) -> bool - Returns `true` if the item icon will be drawn transposed, i.e. the X and Y axes are swapped.
- is_item_selectable(idx: int) -> bool - Returns `true` if the item at the specified index is selectable.
- is_item_tooltip_enabled(idx: int) -> bool - Returns `true` if the tooltip is enabled for specified item index.
- is_selected(idx: int) -> bool - Returns `true` if the item at the specified index is currently selected.
- move_item(from_idx: int, to_idx: int) - Moves item from index `from_idx` to `to_idx`.
- remove_item(idx: int) - Removes the item specified by `idx` index from the list.
- select(idx: int, single: bool = true) - Selects the item at the specified index. **Note:** This method does not trigger the item selection signal.
- set_item_auto_translate_mode(idx: int, mode: int) - Sets the auto translate mode of the item associated with the specified index. Items use `Node.AUTO_TRANSLATE_MODE_INHERIT` by default, which uses the same auto translate mode as the ItemList itself.
- set_item_custom_bg_color(idx: int, custom_bg_color: Color) - Sets the background color of the item specified by `idx` index to the specified Color.
- set_item_custom_fg_color(idx: int, custom_fg_color: Color) - Sets the foreground color of the item specified by `idx` index to the specified Color.
- set_item_disabled(idx: int, disabled: bool) - Disables (or enables) the item at the specified index. Disabled items cannot be selected and do not trigger activation signals (when double-clicking or pressing [kbd]Enter[/kbd]).
- set_item_icon(idx: int, icon: Texture2D) - Sets (or replaces) the icon's Texture2D associated with the specified index.
- set_item_icon_modulate(idx: int, modulate: Color) - Sets a modulating Color of the item associated with the specified index.
- set_item_icon_region(idx: int, rect: Rect2) - Sets the region of item's icon used. The whole icon will be used if the region has no area.
- set_item_icon_transposed(idx: int, transposed: bool) - Sets whether the item icon will be drawn transposed.
- set_item_language(idx: int, language: String) - Sets the language code of the text for the item at the given index to `language`. This is used for line-breaking and text shaping algorithms. If `language` is empty, the current locale is used.
- set_item_metadata(idx: int, metadata: Variant) - Sets a value (of any type) to be stored with the item associated with the specified index.
- set_item_selectable(idx: int, selectable: bool) - Allows or disallows selection of the item associated with the specified index.
- set_item_text(idx: int, text: String) - Sets text of the item associated with the specified index.
- set_item_text_direction(idx: int, direction: int) - Sets item's text base writing direction.
- set_item_tooltip(idx: int, tooltip: String) - Sets the tooltip hint for the item associated with the specified index.
- set_item_tooltip_enabled(idx: int, enable: bool) - Sets whether the tooltip hint is enabled for specified item index.
- sort_items_by_text() - Sorts items in the list by their text.

**Signals:**
- empty_clicked(at_position: Vector2, mouse_button_index: int) - Emitted when any mouse click is issued within the rect of the list but on empty space. `at_position` is the click position in this control's local coordinate system.
- item_activated(index: int) - Emitted when specified list item is activated via double-clicking or by pressing [kbd]Enter[/kbd].
- item_clicked(index: int, at_position: Vector2, mouse_button_index: int) - Emitted when specified list item has been clicked with any mouse button. `at_position` is the click position in this control's local coordinate system.
- item_selected(index: int) - Emitted when specified item has been selected. Only applicable in single selection mode. `allow_reselect` must be enabled to reselect an item.
- multi_selected(index: int, selected: bool) - Emitted when a multiple selection is altered on a list allowing multiple selection.

**Enums:**
**IconMode:** ICON_MODE_TOP=0, ICON_MODE_LEFT=1
  - ICON_MODE_TOP: Icon is drawn above the text.
  - ICON_MODE_LEFT: Icon is drawn to the left of the text.
**SelectMode:** SELECT_SINGLE=0, SELECT_MULTI=1, SELECT_TOGGLE=2
  - SELECT_SINGLE: Only allow selecting a single item.
  - SELECT_MULTI: Allows selecting multiple items by holding [kbd]Ctrl[/kbd] or [kbd]Shift[/kbd].
  - SELECT_TOGGLE: Allows selecting multiple items by toggling them on and off.
**ScrollHintMode:** SCROLL_HINT_MODE_DISABLED=0, SCROLL_HINT_MODE_BOTH=1, SCROLL_HINT_MODE_TOP=2, SCROLL_HINT_MODE_BOTTOM=3
  - SCROLL_HINT_MODE_DISABLED: Scroll hints will never be shown.
  - SCROLL_HINT_MODE_BOTH: Scroll hints will be shown at the top and bottom.
  - SCROLL_HINT_MODE_TOP: Only the top scroll hint will be shown.
  - SCROLL_HINT_MODE_BOTTOM: Only the bottom scroll hint will be shown.

