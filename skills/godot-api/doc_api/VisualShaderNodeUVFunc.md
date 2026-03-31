## VisualShaderNodeUVFunc <- VisualShaderNode

UV functions are similar to Vector2 functions, but the input port of this node uses the shader's UV value by default.

**Props:**
- function: int (VisualShaderNodeUVFunc.Function) = 0

- **function**: A function to be applied to the texture coordinates.

**Enums:**
**Function:** FUNC_PANNING=0, FUNC_SCALING=1, FUNC_MAX=2
  - FUNC_PANNING: Translates `uv` by using `scale` and `offset` values using the following formula: `uv = uv + offset * scale`. `uv` port is connected to `UV` built-in by default.
  - FUNC_SCALING: Scales `uv` by using `scale` and `pivot` values using the following formula: `uv = (uv - pivot) * scale + pivot`. `uv` port is connected to `UV` built-in by default.
  - FUNC_MAX: Represents the size of the `Function` enum.

