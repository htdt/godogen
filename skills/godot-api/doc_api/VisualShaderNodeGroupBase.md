## VisualShaderNodeGroupBase <- VisualShaderNodeResizableBase

Currently, has no direct usage, use the derived classes instead.

**Methods:**
- add_input_port(id: int, type: int, name: String) - Adds an input port with the specified `type` (see `VisualShaderNode.PortType`) and `name`.
- add_output_port(id: int, type: int, name: String) - Adds an output port with the specified `type` (see `VisualShaderNode.PortType`) and `name`.
- clear_input_ports() - Removes all previously specified input ports.
- clear_output_ports() - Removes all previously specified output ports.
- get_free_input_port_id() -> int - Returns a free input port ID which can be used in `add_input_port`.
- get_free_output_port_id() -> int - Returns a free output port ID which can be used in `add_output_port`.
- get_input_port_count() -> int - Returns the number of input ports in use. Alternative for `get_free_input_port_id`.
- get_inputs() -> String - Returns a String description of the input ports as a colon-separated list using the format `id,type,name;` (see `add_input_port`).
- get_output_port_count() -> int - Returns the number of output ports in use. Alternative for `get_free_output_port_id`.
- get_outputs() -> String - Returns a String description of the output ports as a colon-separated list using the format `id,type,name;` (see `add_output_port`).
- has_input_port(id: int) -> bool - Returns `true` if the specified input port exists.
- has_output_port(id: int) -> bool - Returns `true` if the specified output port exists.
- is_valid_port_name(name: String) -> bool - Returns `true` if the specified port name does not override an existed port name and is valid within the shader.
- remove_input_port(id: int) - Removes the specified input port.
- remove_output_port(id: int) - Removes the specified output port.
- set_input_port_name(id: int, name: String) - Renames the specified input port.
- set_input_port_type(id: int, type: int) - Sets the specified input port's type (see `VisualShaderNode.PortType`).
- set_inputs(inputs: String) - Defines all input ports using a String formatted as a colon-separated list: `id,type,name;` (see `add_input_port`).
- set_output_port_name(id: int, name: String) - Renames the specified output port.
- set_output_port_type(id: int, type: int) - Sets the specified output port's type (see `VisualShaderNode.PortType`).
- set_outputs(outputs: String) - Defines all output ports using a String formatted as a colon-separated list: `id,type,name;` (see `add_output_port`).

