## VisualShaderNodeTransformVecMult <- VisualShaderNode

A multiplication operation on a transform (4×4 matrix) and a vector, with support for different multiplication operators.

**Props:**
- operator: int (VisualShaderNodeTransformVecMult.Operator) = 0

- **operator**: The multiplication type to be performed.

**Enums:**
**Operator:** OP_AxB=0, OP_BxA=1, OP_3x3_AxB=2, OP_3x3_BxA=3, OP_MAX=4
  - OP_AxB: Multiplies transform `a` by the vector `b`.
  - OP_BxA: Multiplies vector `b` by the transform `a`.
  - OP_3x3_AxB: Multiplies transform `a` by the vector `b`, skipping the last row and column of the transform.
  - OP_3x3_BxA: Multiplies vector `b` by the transform `a`, skipping the last row and column of the transform.
  - OP_MAX: Represents the size of the `Operator` enum.

