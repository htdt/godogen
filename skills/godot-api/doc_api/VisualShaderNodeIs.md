## VisualShaderNodeIs <- VisualShaderNode

Returns the boolean result of the comparison between `INF` or `NaN` and a scalar parameter.

**Props:**
- function: int (VisualShaderNodeIs.Function) = 0

- **function**: The comparison function.

**Enums:**
**Function:** FUNC_IS_INF=0, FUNC_IS_NAN=1, FUNC_MAX=2
  - FUNC_IS_INF: Comparison with `INF` (Infinity).
  - FUNC_IS_NAN: Comparison with `NaN` (Not a Number; indicates invalid numeric results, such as division by zero).
  - FUNC_MAX: Represents the size of the `Function` enum.

