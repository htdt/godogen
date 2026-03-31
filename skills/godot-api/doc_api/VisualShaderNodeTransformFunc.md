## VisualShaderNodeTransformFunc <- VisualShaderNode

Computes an inverse or transpose function on the provided Transform3D.

**Props:**
- function: int (VisualShaderNodeTransformFunc.Function) = 0

- **function**: The function to be computed.

**Enums:**
**Function:** FUNC_INVERSE=0, FUNC_TRANSPOSE=1, FUNC_MAX=2
  - FUNC_INVERSE: Perform the inverse operation on the Transform3D matrix.
  - FUNC_TRANSPOSE: Perform the transpose operation on the Transform3D matrix.
  - FUNC_MAX: Represents the size of the `Function` enum.

