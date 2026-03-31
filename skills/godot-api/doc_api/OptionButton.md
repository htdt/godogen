## OptionButton <- Button

OptionButton is a type of button that brings up a dropdown with selectable items when pressed. The item selected becomes the "current" item and is displayed as the button text. See also BaseButton which contains common properties and methods associated with this node. **Note:** The IDs used for items are limited to signed 32-bit integers, not the full 64 bits of [int]. These have a range of `-2^31` to `2^31 - 1`, that is, `-2147483648` to `2147483647`. **Note:** The `Button.text` and `Button.icon` properties are set automatically based on the selected item. They shouldn't be changed manually.

**Props:**
- action_mode: int (BaseButton.ActionMode) = 0
- alignment: int (HorizontalAlignment) = 0
- allow_reselect: bool = false
- enable_search_bar_on_item_count: int = 0
- fit_to_longest_item: bool = true
- item_count: int = 0
- popup/item_{index}/disabled: bool = false
- popup/item_{index}/icon: Texture2D
- popup/item_{index}/id: int = 0
- popup/item_{index}/separator: bool = false
- popup/item_{index}/text: String = ""
- selected: int = -1
- toggle_mode: bool = true

- **allow_reselect**: If `true`, the currently selected item can be selected again.
- **enable_search_bar_on_item_count**: Enables the PopupMenu search bar if the item count is greater than `0`.
- **fit_to_longest_item**: If `true`, minimum size will be determined by the longest item's text, instead of the currently selected one's. **Note:** For performance reasons, the minimum size doesn't update immediately when adding, removing or modifying items.
- **item_count**: The number of items to select from.
- **popup/item_{index}/disabled**: If `true`, the item at `index` is disabled. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **popup/item_{index}/icon**: The icon of the item at `index`. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **popup/item_{index}/id**: The ID of the item at `index`. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **popup/item_{index}/separator**: If `true`, the item at `index` is a separator. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **popup/item_{index}/text**: The text of the item at `index`. **Note:** `index` is a value in the `0 .. item_count - 1` range.
- **selected**: The index of the currently selected item, or `-1` if no item is selected.

**Methods:**
- add_icon_item(texture: Texture2D, label: String, id: int = -1) - Adds an item, with a `texture` icon, text `label` and (optionally) `id`. If no `id` is passed, the item index will be used as the item's ID. New items are appended at the end. **Note:** The item will be selected if there are no other items.
- add_item(label: String, id: int = -1) - Adds an item, with text `label` and (optionally) `id`. If no `id` is passed, the item index will be used as the item's ID. New items are appended at the end. **Note:** The item will be selected if there are no other items.
- add_separator(text: String = "") - Adds a separator to the list of items. Separators help to group items, and can optionally be given a `text` header. A separator also gets an index assigned, and is appended at the end of the item list.
- clear() - Clears all the items in the OptionButton.
- get_item_auto_translate_mode(idx: int) -> int - Returns the auto translate mode of the item at index `idx`.
- get_item_icon(idx: int) -> Texture2D - Returns the icon of the item at index `idx`.
- get_item_id(idx: int) -> int - Returns the ID of the item at index `idx`.
- get_item_index(id: int) -> int - Returns the index of the item with the given `id`.
- get_item_metadata(idx: int) -> Variant - Retrieves the metadata of an item. Metadata may be any type and can be used to store extra information about an item, such as an external string ID.
- get_item_text(idx: int) -> String - Returns the text of the item at index `idx`.
- get_item_tooltip(idx: int) -> String - Returns the tooltip of the item at index `idx`.
- get_popup() -> PopupMenu - Returns the PopupMenu contained in this button. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `Window.visible` property.
- get_selectable_item(from_last: bool = false) -> int - Returns the index of the first item which is not disabled, or marked as a separator. If `from_last` is `true`, the items will be searched in reverse order. Returns `-1` if no item is found.
- get_selected_id() -> int - Returns the ID of the selected item, or `-1` if no item is selected.
- get_selected_metadata() -> Variant - Gets the metadata of the selected item. Metadata for items can be set using `set_item_metadata`.
- has_selectable_items() -> bool - Returns `true` if this button contains at least one item which is not disabled, or marked as a separator.
- is_item_disabled(idx: int) -> bool - Returns `true` if the item at index `idx` is disabled.
- is_item_separator(idx: int) -> bool - Returns `true` if the item at index `idx` is marked as a separator.
- is_search_bar_enabled() -> bool - Returns `true` if the search bar is enabled.
- remove_item(idx: int) - Removes the item at index `idx`.
- select(idx: int) - Selects an item by index and makes it the current item. This will work even if the item is disabled. Passing `-1` as the index deselects any currently selected item.
- set_disable_shortcuts(disabled: bool) - If `true`, shortcuts are disabled and cannot be used to trigger the button.
- set_item_auto_translate_mode(idx: int, mode: int) - Sets the auto translate mode of the item at index `idx`. Items use `Node.AUTO_TRANSLATE_MODE_INHERIT` by default, which uses the same auto translate mode as the OptionButton itself.
- set_item_disabled(idx: int, disabled: bool) - Sets whether the item at index `idx` is disabled. Disabled items are drawn differently in the dropdown and are not selectable by the user. If the current selected item is set as disabled, it will remain selected.
- set_item_icon(idx: int, texture: Texture2D) - Sets the icon of the item at index `idx`.
- set_item_id(idx: int, id: int) - Sets the ID of the item at index `idx`.
- set_item_metadata(idx: int, metadata: Variant) - Sets the metadata of an item. Metadata may be of any type and can be used to store extra information about an item, such as an external string ID.
- set_item_text(idx: int, text: String) - Sets the text of the item at index `idx`.
- set_item_tooltip(idx: int, tooltip: String) - Sets the tooltip of the item at index `idx`.
- show_popup() - Adjusts popup position and sizing for the OptionButton, then shows the PopupMenu. Prefer this over using `get_popup().popup()`.

**Signals:**
- item_focused(index: int) - Emitted when the user navigates to an item using the `ProjectSettings.input/ui_up` or `ProjectSettings.input/ui_down` input actions. The index of the item selected is passed as argument.
- item_selected(index: int) - Emitted when the current item has been changed by the user. The index of the item selected is passed as argument. `allow_reselect` must be enabled to reselect an item.

