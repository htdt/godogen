## VisualShader <- Shader

This class provides a graph-like visual editor for creating a Shader. Although VisualShaders do not require coding, they share the same logic with script shaders. They use VisualShaderNodes that can be connected to each other to control the flow of the shader. The visual shader graph is converted to a script shader behind the scenes.

**Props:**
- graph_offset: Vector2

- **graph_offset**: Deprecated.

**Methods:**
- add_node(type: int, node: VisualShaderNode, position: Vector2, id: int) - Adds the specified `node` to the shader.
- add_varying(name: String, mode: int, type: int) - Adds a new varying value node to the shader.
- attach_node_to_frame(type: int, id: int, frame: int) - Attaches the given node to the given frame.
- can_connect_nodes(type: int, from_node: int, from_port: int, to_node: int, to_port: int) -> bool - Returns `true` if the specified nodes and ports can be connected together.
- connect_nodes(type: int, from_node: int, from_port: int, to_node: int, to_port: int) -> int - Connects the specified nodes and ports.
- connect_nodes_forced(type: int, from_node: int, from_port: int, to_node: int, to_port: int) - Connects the specified nodes and ports, even if they can't be connected. Such connection is invalid and will not function properly.
- detach_node_from_frame(type: int, id: int) - Detaches the given node from the frame it is attached to.
- disconnect_nodes(type: int, from_node: int, from_port: int, to_node: int, to_port: int) - Connects the specified nodes and ports.
- get_node(type: int, id: int) -> VisualShaderNode - Returns the shader node instance with specified `type` and `id`.
- get_node_connections(type: int) -> Dictionary[] - Returns the list of connected nodes with the specified type.
- get_node_list(type: int) -> PackedInt32Array - Returns the list of all nodes in the shader with the specified type.
- get_node_position(type: int, id: int) -> Vector2 - Returns the position of the specified node within the shader graph.
- get_valid_node_id(type: int) -> int - Returns next valid node ID that can be added to the shader graph.
- has_varying(name: String) -> bool - Returns `true` if the shader has a varying with the given `name`.
- is_node_connection(type: int, from_node: int, from_port: int, to_node: int, to_port: int) -> bool - Returns `true` if the specified node and port connection exist.
- remove_node(type: int, id: int) - Removes the specified node from the shader.
- remove_varying(name: String) - Removes a varying value node with the given `name`. Prints an error if a node with this name is not found.
- replace_node(type: int, id: int, new_class: StringName) - Replaces the specified node with a node of new class type.
- set_mode(mode: int) - Sets the mode of this shader.
- set_node_position(type: int, id: int, position: Vector2) - Sets the position of the specified node.

**Enums:**
**Type:** TYPE_VERTEX=0, TYPE_FRAGMENT=1, TYPE_LIGHT=2, TYPE_START=3, TYPE_PROCESS=4, TYPE_COLLIDE=5, TYPE_START_CUSTOM=6, TYPE_PROCESS_CUSTOM=7, TYPE_SKY=8, TYPE_FOG=9, ...
  - TYPE_VERTEX: A vertex shader, operating on vertices.
  - TYPE_FRAGMENT: A fragment shader, operating on fragments (pixels).
  - TYPE_LIGHT: A shader for light calculations.
  - TYPE_START: A function for the "start" stage of particle shader.
  - TYPE_PROCESS: A function for the "process" stage of particle shader.
  - TYPE_COLLIDE: A function for the "collide" stage (particle collision handler) of particle shader.
  - TYPE_START_CUSTOM: A function for the "start" stage of particle shader, with customized output.
  - TYPE_PROCESS_CUSTOM: A function for the "process" stage of particle shader, with customized output.
  - TYPE_SKY: A shader for 3D environment's sky.
  - TYPE_FOG: A compute shader that runs for each froxel of the volumetric fog map.
  - TYPE_TEXTURE_BLIT: A shader used to process blit calls to a DrawableTexture.
  - TYPE_MAX: Represents the size of the `Type` enum.
**VaryingMode:** VARYING_MODE_VERTEX_TO_FRAG_LIGHT=0, VARYING_MODE_FRAG_TO_LIGHT=1, VARYING_MODE_MAX=2
  - VARYING_MODE_VERTEX_TO_FRAG_LIGHT: Varying is passed from `Vertex` function to `Fragment` and `Light` functions.
  - VARYING_MODE_FRAG_TO_LIGHT: Varying is passed from `Fragment` function to `Light` function.
  - VARYING_MODE_MAX: Represents the size of the `VaryingMode` enum.
**VaryingType:** VARYING_TYPE_FLOAT=0, VARYING_TYPE_INT=1, VARYING_TYPE_UINT=2, VARYING_TYPE_VECTOR_2D=3, VARYING_TYPE_VECTOR_3D=4, VARYING_TYPE_VECTOR_4D=5, VARYING_TYPE_BOOLEAN=6, VARYING_TYPE_TRANSFORM=7, VARYING_TYPE_MAX=8
  - VARYING_TYPE_FLOAT: Varying is of type [float].
  - VARYING_TYPE_INT: Varying is of type [int].
  - VARYING_TYPE_UINT: Varying is of type unsigned [int].
  - VARYING_TYPE_VECTOR_2D: Varying is of type Vector2.
  - VARYING_TYPE_VECTOR_3D: Varying is of type Vector3.
  - VARYING_TYPE_VECTOR_4D: Varying is of type Vector4.
  - VARYING_TYPE_BOOLEAN: Varying is of type [bool].
  - VARYING_TYPE_TRANSFORM: Varying is of type Transform3D.
  - VARYING_TYPE_MAX: Represents the size of the `VaryingType` enum.
**Constants:** NODE_ID_INVALID=-1, NODE_ID_OUTPUT=0
  - NODE_ID_INVALID: Indicates an invalid VisualShader node.
  - NODE_ID_OUTPUT: Indicates an output node of VisualShader.

