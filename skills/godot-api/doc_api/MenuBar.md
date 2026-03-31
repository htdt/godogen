## MenuBar <- Control

A horizontal menu bar that creates a menu for each PopupMenu child. New items are created by adding PopupMenus to this node. Item title is determined by `Window.title`, or node name if `Window.title` is empty. Item title can be overridden using `set_menu_title`.

**Props:**
- flat: bool = false
- focus_mode: int (Control.FocusMode) = 3
- language: String = ""
- prefer_global_menu: bool = true
- start_index: int = -1
- switch_on_hover: bool = true
- text_direction: int (Control.TextDirection) = 0

- **flat**: Flat MenuBar don't display item decoration.
- **language**: Language code used for line-breaking and text shaping algorithms. If left empty, the current locale is used instead.
- **prefer_global_menu**: If `true`, MenuBar will use system global menu when supported. **Note:** If `true` and global menu is supported, this node is not displayed, has zero size, and all its child nodes except PopupMenus are inaccessible. **Note:** This property overrides the value of the `PopupMenu.prefer_native_menu` property of the child nodes.
- **start_index**: Position order in the global menu to insert MenuBar items at. All menu items in the MenuBar are always inserted as a continuous range. Menus with lower `start_index` are inserted first. Menus with `start_index` equal to `-1` are inserted last.
- **switch_on_hover**: If `true`, when the cursor hovers above menu item, it will close the current PopupMenu and open the other one.
- **text_direction**: Base text writing direction.

**Methods:**
- get_menu_count() -> int - Returns number of menu items.
- get_menu_popup(menu: int) -> PopupMenu - Returns PopupMenu associated with menu item.
- get_menu_title(menu: int) -> String - Returns menu item title.
- get_menu_tooltip(menu: int) -> String - Returns menu item tooltip.
- is_menu_disabled(menu: int) -> bool - Returns `true` if the menu item is disabled.
- is_menu_hidden(menu: int) -> bool - Returns `true` if the menu item is hidden.
- is_native_menu() -> bool - Returns `true` if the current system's global menu is supported and used by this MenuBar.
- set_disable_shortcuts(disabled: bool) - If `true`, shortcuts are disabled and cannot be used to trigger the button.
- set_menu_disabled(menu: int, disabled: bool) - If `true`, menu item is disabled.
- set_menu_hidden(menu: int, hidden: bool) - If `true`, menu item is hidden.
- set_menu_title(menu: int, title: String) - Sets menu item title.
- set_menu_tooltip(menu: int, tooltip: String) - Sets menu item tooltip.

