## TabContainer <- Container

Arranges child controls into a tabbed view, creating a tab for each one. The active tab's corresponding control is made visible, while all other child controls are hidden. Ignores non-control children. **Note:** The drawing of the clickable tabs is handled by this node; TabBar is not needed.

**Props:**
- all_tabs_in_front: bool = false
- clip_tabs: bool = true
- current_tab: int = -1
- deselect_enabled: bool = false
- drag_to_rearrange_enabled: bool = false
- switch_on_drag_hover: bool = true
- tab_alignment: int (TabBar.AlignmentMode) = 0
- tab_focus_mode: int (Control.FocusMode) = 2
- tab_{index}/disabled: bool = false
- tab_{index}/hidden: bool = false
- tab_{index}/icon: Texture2D
- tab_{index}/title: String = ""
- tabs_position: int (TabContainer.TabPosition) = 0
- tabs_rearrange_group: int = -1
- tabs_visible: bool = true
- use_hidden_tabs_for_min_size: bool = false

- **all_tabs_in_front**: If `true`, all tabs are drawn in front of the panel. If `false`, inactive tabs are drawn behind the panel.
- **clip_tabs**: If `true`, tabs overflowing this node's width will be hidden, displaying two navigation buttons instead. Otherwise, this node's minimum size is updated so that all tabs are visible.
- **current_tab**: The current tab index. When set, this index's Control node's `visible` property is set to `true` and all others are set to `false`. A value of `-1` means that no tab is selected.
- **deselect_enabled**: If `true`, all tabs can be deselected so that no tab is selected. Click on the `current_tab` to deselect it. Only the tab header will be shown if no tabs are selected.
- **drag_to_rearrange_enabled**: If `true`, tabs can be rearranged with mouse drag.
- **switch_on_drag_hover**: If `true`, hovering over a tab while dragging something will switch to that tab. Does not have effect when hovering another tab to rearrange.
- **tab_alignment**: The position at which tabs will be placed.
- **tab_focus_mode**: The focus access mode for the internal TabBar node.
- **tab_{index}/disabled**: If `true`, the tab at `index` is disabled. **Note:** `index` is a value in the `0 .. get_tab_count() - 1` range.
- **tab_{index}/hidden**: If `true`, the tab at `index` is hidden. **Note:** `index` is a value in the `0 .. get_tab_count() - 1` range.
- **tab_{index}/icon**: The title text of the tab at `index`. **Note:** `index` is a value in the `0 .. get_tab_count() - 1` range.
- **tab_{index}/title**: The tooltip text of the tab at `index`. **Note:** `index` is a value in the `0 .. get_tab_count() - 1` range.
- **tabs_position**: The horizontal alignment of the tabs.
- **tabs_rearrange_group**: TabContainers with the same rearrange group ID will allow dragging the tabs between them. Enable drag with `drag_to_rearrange_enabled`. Setting this to `-1` will disable rearranging between TabContainers.
- **tabs_visible**: If `true`, tabs are visible. If `false`, tabs' content and titles are hidden.
- **use_hidden_tabs_for_min_size**: If `true`, child Control nodes that are hidden have their minimum size take into account in the total, instead of only the currently visible one.

**Methods:**
- get_current_tab_control() -> Control - Returns the child Control node located at the active tab index.
- get_popup() -> Popup - Returns the Popup node instance if one has been set already with `set_popup`. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `Window.visible` property.
- get_previous_tab() -> int - Returns the previously active tab index.
- get_tab_bar() -> TabBar - Returns the TabBar contained in this container. **Warning:** This is a required internal node, removing and freeing it or editing its tabs may cause a crash. If you wish to edit the tabs, use the methods provided in TabContainer.
- get_tab_button_icon(tab_idx: int) -> Texture2D - Returns the button icon from the tab at index `tab_idx`.
- get_tab_control(tab_idx: int) -> Control - Returns the Control node from the tab at index `tab_idx`.
- get_tab_count() -> int - Returns the number of tabs.
- get_tab_icon(tab_idx: int) -> Texture2D - Returns the Texture2D for the tab at index `tab_idx` or `null` if the tab has no Texture2D.
- get_tab_icon_max_width(tab_idx: int) -> int - Returns the maximum allowed width of the icon for the tab at index `tab_idx`.
- get_tab_idx_at_point(point: Vector2) -> int - Returns the index of the tab at local coordinates `point`. Returns `-1` if the point is outside the control boundaries or if there's no tab at the queried position.
- get_tab_idx_from_control(control: Control) -> int - Returns the index of the tab tied to the given `control`. The control must be a child of the TabContainer.
- get_tab_metadata(tab_idx: int) -> Variant - Returns the metadata value set to the tab at index `tab_idx` using `set_tab_metadata`. If no metadata was previously set, returns `null` by default.
- get_tab_title(tab_idx: int) -> String - Returns the title of the tab at index `tab_idx`. Tab titles default to the name of the indexed child node, but this can be overridden with `set_tab_title`.
- get_tab_tooltip(tab_idx: int) -> String - Returns the tooltip text of the tab at index `tab_idx`.
- is_tab_disabled(tab_idx: int) -> bool - Returns `true` if the tab at index `tab_idx` is disabled.
- is_tab_hidden(tab_idx: int) -> bool - Returns `true` if the tab at index `tab_idx` is hidden.
- select_next_available() -> bool - Selects the first available tab with greater index than the currently selected. Returns `true` if tab selection changed.
- select_previous_available() -> bool - Selects the first available tab with lower index than the currently selected. Returns `true` if tab selection changed.
- set_popup(popup: Node) - If set on a Popup node instance, a popup menu icon appears in the top-right corner of the TabContainer (setting it to `null` will make it go away). Clicking it will expand the Popup node.
- set_tab_button_icon(tab_idx: int, icon: Texture2D) - Sets the button icon from the tab at index `tab_idx`.
- set_tab_disabled(tab_idx: int, disabled: bool) - If `disabled` is `true`, disables the tab at index `tab_idx`, making it non-interactable.
- set_tab_hidden(tab_idx: int, hidden: bool) - If `hidden` is `true`, hides the tab at index `tab_idx`, making it disappear from the tab area.
- set_tab_icon(tab_idx: int, icon: Texture2D) - Sets an icon for the tab at index `tab_idx`.
- set_tab_icon_max_width(tab_idx: int, width: int) - Sets the maximum allowed width of the icon for the tab at index `tab_idx`. This limit is applied on top of the default size of the icon and on top of [theme_item icon_max_width]. The height is adjusted according to the icon's ratio.
- set_tab_metadata(tab_idx: int, metadata: Variant) - Sets the metadata value for the tab at index `tab_idx`, which can be retrieved later using `get_tab_metadata`.
- set_tab_title(tab_idx: int, title: String) - Sets a custom title for the tab at index `tab_idx` (tab titles default to the name of the indexed child node). Set it back to the child's name to make the tab default to it again.
- set_tab_tooltip(tab_idx: int, tooltip: String) - Sets a custom tooltip text for tab at index `tab_idx`. **Note:** By default, if the `tooltip` is empty and the tab text is truncated (not all characters fit into the tab), the title will be displayed as a tooltip. To hide the tooltip, assign `" "` as the `tooltip` text.

**Signals:**
- active_tab_rearranged(idx_to: int) - Emitted when the active tab is rearranged via mouse drag. See `drag_to_rearrange_enabled`.
- pre_popup_pressed - Emitted when the TabContainer's Popup button is clicked. See `set_popup` for details.
- tab_button_pressed(tab: int) - Emitted when the user clicks on the button icon on this tab.
- tab_changed(tab: int) - Emitted when switching to another tab.
- tab_clicked(tab: int) - Emitted when a tab is clicked, even if it is the current tab.
- tab_hovered(tab: int) - Emitted when a tab is hovered by the mouse.
- tab_selected(tab: int) - Emitted when a tab is selected via click, directional input, or script, even if it is the current tab.

**Enums:**
**TabPosition:** POSITION_TOP=0, POSITION_BOTTOM=1, POSITION_MAX=2
  - POSITION_TOP: Places the tab bar at the top.
  - POSITION_BOTTOM: Places the tab bar at the bottom. The tab bar's StyleBox will be flipped vertically.
  - POSITION_MAX: Represents the size of the `TabPosition` enum.

