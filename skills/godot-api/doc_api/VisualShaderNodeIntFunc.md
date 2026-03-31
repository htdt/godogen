## VisualShaderNodeIntFunc <- VisualShaderNode

Accept an integer scalar (`x`) to the input port and transform it according to `function`.

**Props:**
- function: int (VisualShaderNodeIntFunc.Function) = 2

- **function**: A function to be applied to the scalar.

**Enums:**
**Function:** FUNC_ABS=0, FUNC_NEGATE=1, FUNC_SIGN=2, FUNC_BITWISE_NOT=3, FUNC_MAX=4
  - FUNC_ABS: Returns the absolute value of the parameter. Translates to `abs(x)` in the Godot Shader Language.
  - FUNC_NEGATE: Negates the `x` using `-(x)`.
  - FUNC_SIGN: Extracts the sign of the parameter. Translates to `sign(x)` in the Godot Shader Language.
  - FUNC_BITWISE_NOT: Returns the result of bitwise `NOT` operation on the integer. Translates to `~a` in the Godot Shader Language.
  - FUNC_MAX: Represents the size of the `Function` enum.

