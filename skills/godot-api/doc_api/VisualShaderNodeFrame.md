## VisualShaderNodeFrame <- VisualShaderNodeResizableBase

A rectangular frame that can be used to group visual shader nodes together to improve organization. Nodes attached to the frame will move with it when it is dragged and it can automatically resize to enclose all attached nodes. Its title, description and color can be customized.

**Props:**
- attached_nodes: PackedInt32Array = PackedInt32Array()
- autoshrink: bool = true
- tint_color: Color = Color(0.3, 0.3, 0.3, 0.75)
- tint_color_enabled: bool = false
- title: String = "Title"

- **attached_nodes**: The list of nodes attached to the frame.
- **autoshrink**: If `true`, the frame will automatically resize to enclose all attached nodes.
- **tint_color**: The color of the frame when `tint_color_enabled` is `true`.
- **tint_color_enabled**: If `true`, the frame will be tinted with the color specified in `tint_color`.
- **title**: The title of the node.

**Methods:**
- add_attached_node(node: int) - Adds a node to the list of nodes attached to the frame. Should not be called directly, use the `VisualShader.attach_node_to_frame` method instead.
- remove_attached_node(node: int) - Removes a node from the list of nodes attached to the frame. Should not be called directly, use the `VisualShader.detach_node_from_frame` method instead.

