## VisualShaderNode <- Resource

Visual shader graphs consist of various nodes. Each node in the graph is a separate object and they are represented as a rectangular boxes with title and a set of properties. Each node also has connection ports that allow to connect it to another nodes and control the flow of the shader.

**Props:**
- linked_parent_graph_frame: int = -1
- output_port_for_preview: int = -1

- **linked_parent_graph_frame**: Represents the index of the frame this node is linked to. If set to `-1` the node is not linked to any frame.
- **output_port_for_preview**: Sets the output port index which will be showed for preview. If set to `-1` no port will be open for preview.

**Methods:**
- clear_default_input_values() - Clears the default input ports value.
- get_default_input_port(type: int) -> int - Returns the input port which should be connected by default when this node is created as a result of dragging a connection from an existing node to the empty space on the graph.
- get_default_input_values() -> Array - Returns an Array containing default values for all of the input ports of the node in the form `[index0, value0, index1, value1, ...]`.
- get_input_port_default_value(port: int) -> Variant - Returns the default value of the input `port`.
- remove_input_port_default_value(port: int) - Removes the default value of the input `port`.
- set_default_input_values(values: Array) - Sets the default input ports values using an Array of the form `[index0, value0, index1, value1, ...]`. For example: `[0, Vector3(0, 0, 0), 1, Vector3(0, 0, 0)]`.
- set_input_port_default_value(port: int, value: Variant, prev_value: Variant = null) - Sets the default `value` for the selected input `port`.

**Enums:**
**PortType:** PORT_TYPE_SCALAR=0, PORT_TYPE_SCALAR_INT=1, PORT_TYPE_SCALAR_UINT=2, PORT_TYPE_VECTOR_2D=3, PORT_TYPE_VECTOR_3D=4, PORT_TYPE_VECTOR_4D=5, PORT_TYPE_BOOLEAN=6, PORT_TYPE_TRANSFORM=7, PORT_TYPE_SAMPLER=8, PORT_TYPE_MAX=9
  - PORT_TYPE_SCALAR: Floating-point scalar. Translated to [code skip-lint]float[/code] type in shader code.
  - PORT_TYPE_SCALAR_INT: Integer scalar. Translated to [code skip-lint]int[/code] type in shader code.
  - PORT_TYPE_SCALAR_UINT: Unsigned integer scalar. Translated to [code skip-lint]uint[/code] type in shader code.
  - PORT_TYPE_VECTOR_2D: 2D vector of floating-point values. Translated to [code skip-lint]vec2[/code] type in shader code.
  - PORT_TYPE_VECTOR_3D: 3D vector of floating-point values. Translated to [code skip-lint]vec3[/code] type in shader code.
  - PORT_TYPE_VECTOR_4D: 4D vector of floating-point values. Translated to [code skip-lint]vec4[/code] type in shader code.
  - PORT_TYPE_BOOLEAN: Boolean type. Translated to [code skip-lint]bool[/code] type in shader code.
  - PORT_TYPE_TRANSFORM: Transform type. Translated to [code skip-lint]mat4[/code] type in shader code.
  - PORT_TYPE_SAMPLER: Sampler type. Translated to reference of sampler uniform in shader code. Can only be used for input ports in non-uniform nodes.
  - PORT_TYPE_MAX: Represents the size of the `PortType` enum.

