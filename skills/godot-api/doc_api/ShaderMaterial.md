## ShaderMaterial <- Material

A material that uses a custom Shader program to render visual items (canvas items, meshes, skies, fog), or to process particles. Compared to other materials, ShaderMaterial gives deeper control over the generated shader code. For more information, see the shaders documentation index below. Multiple ShaderMaterials can use the same shader and configure different values for the shader uniforms. **Note:** For performance reasons, the `Resource.changed` signal is only emitted when the `Resource.resource_name` changes. Only in editor, it is also emitted for `shader` changes.

**Props:**
- shader: Shader

- **shader**: The Shader program used to render this material.

**Methods:**
- get_shader_parameter(param: StringName) -> Variant - Returns the current value set for this material of a uniform in the shader.
- set_shader_parameter(param: StringName, value: Variant) - Changes the value set for this material of a uniform in the shader. **Note:** `param` is case-sensitive and must match the name of the uniform in the code exactly (not the capitalized name in the inspector). **Note:** Changes to the shader uniform will be effective on all instances using this ShaderMaterial. To prevent this, use per-instance uniforms with `CanvasItem.set_instance_shader_parameter`, `GeometryInstance3D.set_instance_shader_parameter` or duplicate the ShaderMaterial resource using `Resource.duplicate`. Per-instance uniforms allow for better shader reuse and are therefore faster, so they should be preferred over duplicating the ShaderMaterial when possible.

