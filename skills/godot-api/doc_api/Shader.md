## Shader <- Resource

A custom shader program implemented in the Godot shading language, saved with the `.gdshader` extension. This class is used by a ShaderMaterial and allows you to write your own custom behavior for rendering visual items or updating particle information. For a detailed explanation and usage, please see the tutorials linked below.

**Props:**
- code: String = ""

- **code**: Returns the shader's code as the user has written it, not the full generated code used internally.

**Methods:**
- get_default_texture_parameter(name: StringName, index: int = 0) -> Texture - Returns the texture that is set as default for the specified parameter. **Note:** `name` must match the name of the uniform in the code exactly. **Note:** If the sampler array is used use `index` to access the specified texture.
- get_mode() -> int - Returns the shader mode for the shader.
- get_shader_uniform_list(get_groups: bool = false) -> Array - Returns the list of shader uniforms that can be assigned to a ShaderMaterial, for use with `ShaderMaterial.set_shader_parameter` and `ShaderMaterial.get_shader_parameter`. The parameters returned are contained in dictionaries in a similar format to the ones returned by `Object.get_property_list`. If argument `get_groups` is `true`, parameter grouping hints are also included in the list.
- inspect_native_shader_code() - Only available when running in the editor. Opens a popup that visualizes the generated shader code, including all variants and internal shader code. See also `Material.inspect_native_shader_code`.
- set_default_texture_parameter(name: StringName, texture: Texture, index: int = 0) - Sets the default texture to be used with a texture uniform. The default is used if a texture is not set in the ShaderMaterial. **Note:** `name` must match the name of the uniform in the code exactly. **Note:** If the sampler array is used use `index` to access the specified texture.

**Enums:**
**Mode:** MODE_SPATIAL=0, MODE_CANVAS_ITEM=1, MODE_PARTICLES=2, MODE_SKY=3, MODE_FOG=4, MODE_TEXTURE_BLIT=5
  - MODE_SPATIAL: Mode used to draw all 3D objects.
  - MODE_CANVAS_ITEM: Mode used to draw all 2D objects.
  - MODE_PARTICLES: Mode used to calculate particle information on a per-particle basis. Not used for drawing.
  - MODE_SKY: Mode used for drawing skies. Only works with shaders attached to Sky objects.
  - MODE_FOG: Mode used for setting the color and density of volumetric fog effect.
  - MODE_TEXTURE_BLIT: Mode used for drawing to DrawableTexture resources via blit calls.

