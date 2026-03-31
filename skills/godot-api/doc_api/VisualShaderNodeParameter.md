## VisualShaderNodeParameter <- VisualShaderNode

A parameter represents a variable in the shader which is set externally, i.e. from the ShaderMaterial. Parameters are exposed as properties in the ShaderMaterial and can be assigned from the Inspector or from a script.

**Props:**
- instance_index: int = 0
- parameter_name: String = ""
- qualifier: int (VisualShaderNodeParameter.Qualifier) = 0

- **instance_index**: The index within 0-15 range, which is used to avoid clashes when shader used on multiple materials.
- **parameter_name**: Name of the parameter, by which it can be accessed through the ShaderMaterial properties.
- **qualifier**: Defines the scope of the parameter.

**Enums:**
**Qualifier:** QUAL_NONE=0, QUAL_GLOBAL=1, QUAL_INSTANCE=2, QUAL_INSTANCE_INDEX=3, QUAL_MAX=4
  - QUAL_NONE: The parameter will be tied to the ShaderMaterial using this shader.
  - QUAL_GLOBAL: The parameter will use a global value, defined in Project Settings.
  - QUAL_INSTANCE: The parameter will be tied to the node with attached ShaderMaterial using this shader.
  - QUAL_INSTANCE_INDEX: The parameter will be tied to the node with attached ShaderMaterial using this shader. Enables setting a `instance_index` property.
  - QUAL_MAX: Represents the size of the `Qualifier` enum.

