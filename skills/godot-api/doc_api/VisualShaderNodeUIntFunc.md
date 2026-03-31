## VisualShaderNodeUIntFunc <- VisualShaderNode

Accept an unsigned integer scalar (`x`) to the input port and transform it according to `function`.

**Props:**
- function: int (VisualShaderNodeUIntFunc.Function) = 0

- **function**: A function to be applied to the scalar.

**Enums:**
**Function:** FUNC_NEGATE=0, FUNC_BITWISE_NOT=1, FUNC_MAX=2
  - FUNC_NEGATE: Negates the `x` using `-(x)`.
  - FUNC_BITWISE_NOT: Returns the result of bitwise `NOT` operation on the integer. Translates to `~a` in the Godot Shader Language.
  - FUNC_MAX: Represents the size of the `Function` enum.

