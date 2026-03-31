## GraphEdit <- Control

GraphEdit provides tools for creation, manipulation, and display of various graphs. Its main purpose in the engine is to power the visual programming systems, such as visual shaders, but it is also available for use in user projects. GraphEdit by itself is only an empty container, representing an infinite grid where GraphNodes can be placed. Each GraphNode represents a node in the graph, a single unit of data in the connected scheme. GraphEdit, in turn, helps to control various interactions with nodes and between nodes. When the user attempts to connect, disconnect, or delete a GraphNode, a signal is emitted in the GraphEdit, but no action is taken by default. It is the responsibility of the programmer utilizing this control to implement the necessary logic to determine how each request should be handled. **Performance:** It is greatly advised to enable low-processor usage mode (see `OS.low_processor_usage_mode`) when using GraphEdits. **Note:** Keep in mind that `Node.get_children` will also return the connection layer node named `_connection_layer` due to technical limitations. This behavior may change in future releases.

**Props:**
- clip_contents: bool = true
- connection_lines_antialiased: bool = true
- connection_lines_curvature: float = 0.5
- connection_lines_thickness: float = 4.0
- connections: Dictionary[] = []
- focus_mode: int (Control.FocusMode) = 2
- grid_pattern: int (GraphEdit.GridPattern) = 0
- minimap_enabled: bool = true
- minimap_opacity: float = 0.65
- minimap_size: Vector2 = Vector2(240, 160)
- panning_scheme: int (GraphEdit.PanningScheme) = 0
- right_disconnects: bool = false
- scroll_offset: Vector2 = Vector2(0, 0)
- show_arrange_button: bool = true
- show_grid: bool = true
- show_grid_buttons: bool = true
- show_menu: bool = true
- show_minimap_button: bool = true
- show_zoom_buttons: bool = true
- show_zoom_label: bool = false
- snapping_distance: int = 20
- snapping_enabled: bool = true
- type_names: Dictionary = {}
- zoom: float = 1.0
- zoom_max: float = 2.0736003
- zoom_min: float = 0.23256795
- zoom_step: float = 1.2

- **connection_lines_antialiased**: If `true`, the lines between nodes will use antialiasing.
- **connection_lines_curvature**: The curvature of the lines between the nodes. 0 results in straight lines.
- **connection_lines_thickness**: The thickness of the lines between the nodes.
- **connections**: The connections between GraphNodes. A connection is represented as a Dictionary in the form of: Connections with `keep_alive` set to `false` may be deleted automatically if invalid during a redraw.
- **grid_pattern**: The pattern used for drawing the grid.
- **minimap_enabled**: If `true`, the minimap is visible.
- **minimap_opacity**: The opacity of the minimap rectangle.
- **minimap_size**: The size of the minimap rectangle. The map itself is based on the size of the grid area and is scaled to fit this rectangle.
- **panning_scheme**: Defines the control scheme for panning with mouse wheel.
- **right_disconnects**: If `true`, enables disconnection of existing connections in the GraphEdit by dragging the right end.
- **scroll_offset**: The scroll offset.
- **show_arrange_button**: If `true`, the button to automatically arrange graph nodes is visible.
- **show_grid**: If `true`, the grid is visible.
- **show_grid_buttons**: If `true`, buttons that allow to configure grid and snapping options are visible.
- **show_menu**: If `true`, the menu toolbar is visible.
- **show_minimap_button**: If `true`, the button to toggle the minimap is visible.
- **show_zoom_buttons**: If `true`, buttons that allow to change and reset the zoom level are visible.
- **show_zoom_label**: If `true`, the label with the current zoom level is visible. The zoom level is displayed in percents.
- **snapping_distance**: The snapping distance in pixels, also determines the grid line distance.
- **snapping_enabled**: If `true`, enables snapping.
- **type_names**: Dictionary of human-readable port type names.
- **zoom**: The current zoom value.
- **zoom_max**: The upper zoom limit.
- **zoom_min**: The lower zoom limit.
- **zoom_step**: The step of each zoom level.

**Methods:**
- _get_connection_line(from_position: Vector2, to_position: Vector2) -> PackedVector2Array - Virtual method which can be overridden to customize how connections are drawn.
- _is_in_input_hotzone(in_node: Object, in_port: int, mouse_position: Vector2) -> bool - Returns whether the `mouse_position` is in the input hot zone. By default, a hot zone is a Rect2 positioned such that its center is at `in_node`.`GraphNode.get_input_port_position`(`in_port`) (For output's case, call `GraphNode.get_output_port_position` instead). The hot zone's width is twice the Theme Property `port_grab_distance_horizontal`, and its height is twice the `port_grab_distance_vertical`. Below is a sample code to help get started:
- _is_in_output_hotzone(in_node: Object, in_port: int, mouse_position: Vector2) -> bool - Returns whether the `mouse_position` is in the output hot zone. For more information on hot zones, see `_is_in_input_hotzone`. Below is a sample code to help get started:
- _is_node_hover_valid(from_node: StringName, from_port: int, to_node: StringName, to_port: int) -> bool - This virtual method can be used to insert additional error detection while the user is dragging a connection over a valid port. Return `true` if the connection is indeed valid or return `false` if the connection is impossible. If the connection is impossible, no snapping to the port and thus no connection request to that port will happen. In this example a connection to same node is suppressed:
- add_valid_connection_type(from_type: int, to_type: int) - Allows the connection between two different port types. The port type is defined individually for the left and the right port of each slot with the `GraphNode.set_slot` method. See also `is_valid_connection_type` and `remove_valid_connection_type`.
- add_valid_left_disconnect_type(type: int) - Allows to disconnect nodes when dragging from the left port of the GraphNode's slot if it has the specified type. See also `remove_valid_left_disconnect_type`.
- add_valid_right_disconnect_type(type: int) - Allows to disconnect nodes when dragging from the right port of the GraphNode's slot if it has the specified type. See also `remove_valid_right_disconnect_type`.
- arrange_nodes() - Rearranges selected nodes in a layout with minimum crossings between connections and uniform horizontal and vertical gap between nodes.
- attach_graph_element_to_frame(element: StringName, frame: StringName) - Attaches the `element` GraphElement to the `frame` GraphFrame.
- clear_connections() - Removes all connections between nodes.
- connect_node(from_node: StringName, from_port: int, to_node: StringName, to_port: int, keep_alive: bool = false) -> int - Create a connection between the `from_port` of the `from_node` GraphNode and the `to_port` of the `to_node` GraphNode. If the connection already exists, no connection is created. Connections with `keep_alive` set to `false` may be deleted automatically if invalid during a redraw.
- detach_graph_element_from_frame(element: StringName) - Detaches the `element` GraphElement from the GraphFrame it is currently attached to.
- disconnect_node(from_node: StringName, from_port: int, to_node: StringName, to_port: int) - Removes the connection between the `from_port` of the `from_node` GraphNode and the `to_port` of the `to_node` GraphNode. If the connection does not exist, no connection is removed.
- force_connection_drag_end() - Ends the creation of the current connection. In other words, if you are dragging a connection you can use this method to abort the process and remove the line that followed your cursor. This is best used together with `connection_drag_started` and `connection_drag_ended` to add custom behavior like node addition through shortcuts. **Note:** This method suppresses any other connection request signals apart from `connection_drag_ended`.
- get_attached_nodes_of_frame(frame: StringName) -> StringName[] - Returns an array of node names that are attached to the GraphFrame with the given name.
- get_closest_connection_at_point(point: Vector2, max_distance: float = 4.0) -> Dictionary - Returns the closest connection to the given point in screen space. If no connection is found within `max_distance` pixels, an empty Dictionary is returned. A connection is represented as a Dictionary in the form of: For example, getting a connection at a given mouse position can be achieved like this:
- get_connection_count(from_node: StringName, from_port: int) -> int - Returns the number of connections from `from_port` of `from_node`.
- get_connection_line(from_node: Vector2, to_node: Vector2) -> PackedVector2Array - Returns the points which would make up a connection between `from_node` and `to_node`.
- get_connection_list_from_node(node: StringName) -> Dictionary[] - Returns an Array containing a list of all connections for `node`. A connection is represented as a Dictionary in the form of: **Example:** Get all connections on a specific port:
- get_connections_intersecting_with_rect(rect: Rect2) -> Dictionary[] - Returns an Array containing the list of connections that intersect with the given Rect2. A connection is represented as a Dictionary in the form of:
- get_element_frame(element: StringName) -> GraphFrame - Returns the GraphFrame that contains the GraphElement with the given name.
- get_menu_hbox() -> HBoxContainer - Gets the HBoxContainer that contains the zooming and grid snap controls in the top left of the graph. You can use this method to reposition the toolbar or to add your own custom controls to it. **Warning:** This is a required internal node, removing and freeing it may cause a crash. If you wish to hide it or any of its children, use their `CanvasItem.visible` property.
- is_node_connected(from_node: StringName, from_port: int, to_node: StringName, to_port: int) -> bool - Returns `true` if the `from_port` of the `from_node` GraphNode is connected to the `to_port` of the `to_node` GraphNode.
- is_valid_connection_type(from_type: int, to_type: int) -> bool - Returns whether it's possible to make a connection between two different port types. The port type is defined individually for the left and the right port of each slot with the `GraphNode.set_slot` method. See also `add_valid_connection_type` and `remove_valid_connection_type`.
- remove_valid_connection_type(from_type: int, to_type: int) - Disallows the connection between two different port types previously allowed by `add_valid_connection_type`. The port type is defined individually for the left and the right port of each slot with the `GraphNode.set_slot` method. See also `is_valid_connection_type`.
- remove_valid_left_disconnect_type(type: int) - Disallows to disconnect nodes when dragging from the left port of the GraphNode's slot if it has the specified type. Use this to disable a disconnection previously allowed with `add_valid_left_disconnect_type`.
- remove_valid_right_disconnect_type(type: int) - Disallows to disconnect nodes when dragging from the right port of the GraphNode's slot if it has the specified type. Use this to disable a disconnection previously allowed with `add_valid_right_disconnect_type`.
- set_connection_activity(from_node: StringName, from_port: int, to_node: StringName, to_port: int, amount: float) - Sets the coloration of the connection between `from_node`'s `from_port` and `to_node`'s `to_port` with the color provided in the [theme_item activity] theme property. The color is linearly interpolated between the connection color and the activity color using `amount` as weight.
- set_selected(node: Node) - Sets the specified `node` as the one selected.

**Signals:**
- begin_node_move - Emitted at the beginning of a GraphElement's movement.
- connection_drag_ended - Emitted at the end of a connection drag.
- connection_drag_started(from_node: StringName, from_port: int, is_output: bool) - Emitted at the beginning of a connection drag.
- connection_from_empty(to_node: StringName, to_port: int, release_position: Vector2) - Emitted when user drags a connection from an input port into the empty space of the graph.
- connection_request(from_node: StringName, from_port: int, to_node: StringName, to_port: int) - Emitted to the GraphEdit when the connection between the `from_port` of the `from_node` GraphNode and the `to_port` of the `to_node` GraphNode is attempted to be created.
- connection_to_empty(from_node: StringName, from_port: int, release_position: Vector2) - Emitted when user drags a connection from an output port into the empty space of the graph.
- copy_nodes_request - Emitted when this GraphEdit captures a `ui_copy` action ([kbd]Ctrl + C[/kbd] by default). In general, this signal indicates that the selected GraphElements should be copied.
- cut_nodes_request - Emitted when this GraphEdit captures a `ui_cut` action ([kbd]Ctrl + X[/kbd] by default). In general, this signal indicates that the selected GraphElements should be cut.
- delete_nodes_request(nodes: StringName[]) - Emitted when this GraphEdit captures a `ui_graph_delete` action ([kbd]Delete[/kbd] by default). `nodes` is an array of node names that should be removed. These usually include all selected nodes.
- disconnection_request(from_node: StringName, from_port: int, to_node: StringName, to_port: int) - Emitted to the GraphEdit when the connection between `from_port` of `from_node` GraphNode and `to_port` of `to_node` GraphNode is attempted to be removed.
- duplicate_nodes_request - Emitted when this GraphEdit captures a `ui_graph_duplicate` action ([kbd]Ctrl + D[/kbd] by default). In general, this signal indicates that the selected GraphElements should be duplicated.
- end_node_move - Emitted at the end of a GraphElement's movement.
- frame_rect_changed(frame: GraphFrame, new_rect: Rect2) - Emitted when the GraphFrame `frame` is resized to `new_rect`.
- graph_elements_linked_to_frame_request(elements: Array, frame: StringName) - Emitted when one or more GraphElements are dropped onto the GraphFrame named `frame`, when they were not previously attached to any other one. `elements` is an array of GraphElements to be attached.
- node_deselected(node: Node) - Emitted when the given GraphElement node is deselected.
- node_selected(node: Node) - Emitted when the given GraphElement node is selected.
- paste_nodes_request - Emitted when this GraphEdit captures a `ui_paste` action ([kbd]Ctrl + V[/kbd] by default). In general, this signal indicates that previously copied GraphElements should be pasted.
- popup_request(at_position: Vector2) - Emitted when a popup is requested. Happens on right-clicking in the GraphEdit. `at_position` is the position of the mouse pointer when the signal is sent.
- scroll_offset_changed(offset: Vector2) - Emitted when the scroll offset is changed by the user. It will not be emitted when changed in code.

**Enums:**
**PanningScheme:** SCROLL_ZOOMS=0, SCROLL_PANS=1
  - SCROLL_ZOOMS: [kbd]Mouse Wheel[/kbd] will zoom, [kbd]Ctrl + Mouse Wheel[/kbd] will move the view.
  - SCROLL_PANS: [kbd]Mouse Wheel[/kbd] will move the view, [kbd]Ctrl + Mouse Wheel[/kbd] will zoom.
**GridPattern:** GRID_PATTERN_LINES=0, GRID_PATTERN_DOTS=1
  - GRID_PATTERN_LINES: Draw the grid using solid lines.
  - GRID_PATTERN_DOTS: Draw the grid using dots.

