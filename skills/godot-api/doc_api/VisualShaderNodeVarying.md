## VisualShaderNodeVarying <- VisualShaderNode

Varying values are shader variables that can be passed between shader functions, e.g. from Vertex shader to Fragment shader.

**Props:**
- varying_name: String = "[None]"
- varying_type: int (VisualShader.VaryingType) = 0

- **varying_name**: Name of the variable. Must be unique.
- **varying_type**: Type of the variable. Determines where the variable can be accessed.

