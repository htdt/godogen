## RDShaderSPIRV <- Resource

RDShaderSPIRV represents an RDShaderFile's code for various shader stages, as well as possible compilation error messages. SPIR-V is a low-level intermediate shader representation. This intermediate representation is not used directly by GPUs for rendering, but it can be compiled into binary shaders that GPUs can understand. Unlike compiled shaders, SPIR-V is portable across GPU models and driver versions. This object is used by RenderingDevice.

**Props:**
- bytecode_any_hit: PackedByteArray = PackedByteArray()
- bytecode_closest_hit: PackedByteArray = PackedByteArray()
- bytecode_compute: PackedByteArray = PackedByteArray()
- bytecode_fragment: PackedByteArray = PackedByteArray()
- bytecode_intersection: PackedByteArray = PackedByteArray()
- bytecode_miss: PackedByteArray = PackedByteArray()
- bytecode_raygen: PackedByteArray = PackedByteArray()
- bytecode_tesselation_control: PackedByteArray = PackedByteArray()
- bytecode_tesselation_evaluation: PackedByteArray = PackedByteArray()
- bytecode_vertex: PackedByteArray = PackedByteArray()
- compile_error_any_hit: String = ""
- compile_error_closest_hit: String = ""
- compile_error_compute: String = ""
- compile_error_fragment: String = ""
- compile_error_intersection: String = ""
- compile_error_miss: String = ""
- compile_error_raygen: String = ""
- compile_error_tesselation_control: String = ""
- compile_error_tesselation_evaluation: String = ""
- compile_error_vertex: String = ""

- **bytecode_any_hit**: The SPIR-V bytecode for the any hit shader stage.
- **bytecode_closest_hit**: The SPIR-V bytecode for the closest hit shader stage.
- **bytecode_compute**: The SPIR-V bytecode for the compute shader stage.
- **bytecode_fragment**: The SPIR-V bytecode for the fragment shader stage.
- **bytecode_intersection**: The SPIR-V bytecode for the intersection shader stage.
- **bytecode_miss**: The SPIR-V bytecode for the miss shader stage.
- **bytecode_raygen**: The SPIR-V bytecode for the ray generation shader stage.
- **bytecode_tesselation_control**: The SPIR-V bytecode for the tessellation control shader stage.
- **bytecode_tesselation_evaluation**: The SPIR-V bytecode for the tessellation evaluation shader stage.
- **bytecode_vertex**: The SPIR-V bytecode for the vertex shader stage.
- **compile_error_any_hit**: The compilation error message for the any hit shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_closest_hit**: The compilation error message for the closest hit shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_compute**: The compilation error message for the compute shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_fragment**: The compilation error message for the fragment shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_intersection**: The compilation error message for the intersection shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_miss**: The compilation error message for the miss shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_raygen**: The compilation error message for the ray generation shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_tesselation_control**: The compilation error message for the tessellation control shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_tesselation_evaluation**: The compilation error message for the tessellation evaluation shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.
- **compile_error_vertex**: The compilation error message for the vertex shader stage (set by the SPIR-V compiler and Godot). If empty, shader compilation was successful.

**Methods:**
- get_stage_bytecode(stage: int) -> PackedByteArray - Equivalent to getting one of `bytecode_compute`, `bytecode_fragment`, `bytecode_tesselation_control`, `bytecode_tesselation_evaluation`, `bytecode_vertex`.
- get_stage_compile_error(stage: int) -> String - Returns the compilation error message for the given shader `stage`. Equivalent to getting one of `compile_error_compute`, `compile_error_fragment`, `compile_error_tesselation_control`, `compile_error_tesselation_evaluation`, `compile_error_vertex`.
- set_stage_bytecode(stage: int, bytecode: PackedByteArray) - Sets the SPIR-V `bytecode` for the given shader `stage`. Equivalent to setting one of `bytecode_compute`, `bytecode_fragment`, `bytecode_tesselation_control`, `bytecode_tesselation_evaluation`, `bytecode_vertex`.
- set_stage_compile_error(stage: int, compile_error: String) - Sets the compilation error message for the given shader `stage` to `compile_error`. Equivalent to setting one of `compile_error_compute`, `compile_error_fragment`, `compile_error_tesselation_control`, `compile_error_tesselation_evaluation`, `compile_error_vertex`.

