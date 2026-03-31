## RDShaderSource <- RefCounted

Shader source code in text form. See also RDShaderFile. RDShaderSource is only meant to be used with the RenderingDevice API. It should not be confused with Godot's own Shader resource, which is what Godot's various nodes use for high-level shader programming.

**Props:**
- language: int (RenderingDevice.ShaderLanguage) = 0
- source_any_hit: String = ""
- source_closest_hit: String = ""
- source_compute: String = ""
- source_fragment: String = ""
- source_intersection: String = ""
- source_miss: String = ""
- source_raygen: String = ""
- source_tesselation_control: String = ""
- source_tesselation_evaluation: String = ""
- source_vertex: String = ""

- **language**: The language the shader is written in.
- **source_any_hit**: Source code for the shader's any hit stage.
- **source_closest_hit**: Source code for the shader's closest hit stage.
- **source_compute**: Source code for the shader's compute stage.
- **source_fragment**: Source code for the shader's fragment stage.
- **source_intersection**: Source code for the shader's intersection stage.
- **source_miss**: Source code for the shader's miss stage.
- **source_raygen**: Source code for the shader's ray generation stage.
- **source_tesselation_control**: Source code for the shader's tessellation control stage.
- **source_tesselation_evaluation**: Source code for the shader's tessellation evaluation stage.
- **source_vertex**: Source code for the shader's vertex stage.

**Methods:**
- get_stage_source(stage: int) -> String - Returns source code for the specified shader `stage`. Equivalent to getting one of `source_compute`, `source_fragment`, `source_tesselation_control`, `source_tesselation_evaluation` or `source_vertex`.
- set_stage_source(stage: int, source: String) - Sets `source` code for the specified shader `stage`. Equivalent to setting one of `source_compute`, `source_fragment`, `source_tesselation_control`, `source_tesselation_evaluation` or `source_vertex`. **Note:** If you set the compute shader source code using this method directly, remember to remove the Godot-specific hint `#[compute]`.

