## VisualShaderNodeTransformOp <- VisualShaderNode

Applies `operator` to two transform (4×4 matrices) inputs.

**Props:**
- operator: int (VisualShaderNodeTransformOp.Operator) = 0

- **operator**: The type of the operation to be performed on the transforms.

**Enums:**
**Operator:** OP_AxB=0, OP_BxA=1, OP_AxB_COMP=2, OP_BxA_COMP=3, OP_ADD=4, OP_A_MINUS_B=5, OP_B_MINUS_A=6, OP_A_DIV_B=7, OP_B_DIV_A=8, OP_MAX=9
  - OP_AxB: Multiplies transform `a` by the transform `b`.
  - OP_BxA: Multiplies transform `b` by the transform `a`.
  - OP_AxB_COMP: Performs a component-wise multiplication of transform `a` by the transform `b`.
  - OP_BxA_COMP: Performs a component-wise multiplication of transform `b` by the transform `a`.
  - OP_ADD: Adds two transforms.
  - OP_A_MINUS_B: Subtracts the transform `a` from the transform `b`.
  - OP_B_MINUS_A: Subtracts the transform `b` from the transform `a`.
  - OP_A_DIV_B: Divides the transform `a` by the transform `b`.
  - OP_B_DIV_A: Divides the transform `b` by the transform `a`.
  - OP_MAX: Represents the size of the `Operator` enum.

