## VisualShaderNodeMix <- VisualShaderNode

Translates to `mix(a, b, weight)` in the shader language.

**Props:**
- op_type: int (VisualShaderNodeMix.OpType) = 0

- **op_type**: A type of operands and returned value.

**Enums:**
**OpType:** OP_TYPE_SCALAR=0, OP_TYPE_VECTOR_2D=1, OP_TYPE_VECTOR_2D_SCALAR=2, OP_TYPE_VECTOR_3D=3, OP_TYPE_VECTOR_3D_SCALAR=4, OP_TYPE_VECTOR_4D=5, OP_TYPE_VECTOR_4D_SCALAR=6, OP_TYPE_MAX=7
  - OP_TYPE_SCALAR: A floating-point scalar.
  - OP_TYPE_VECTOR_2D: A 2D vector type.
  - OP_TYPE_VECTOR_2D_SCALAR: The `a` and `b` ports use a 2D vector type. The `weight` port uses a scalar type.
  - OP_TYPE_VECTOR_3D: A 3D vector type.
  - OP_TYPE_VECTOR_3D_SCALAR: The `a` and `b` ports use a 3D vector type. The `weight` port uses a scalar type.
  - OP_TYPE_VECTOR_4D: A 4D vector type.
  - OP_TYPE_VECTOR_4D_SCALAR: The `a` and `b` ports use a 4D vector type. The `weight` port uses a scalar type.
  - OP_TYPE_MAX: Represents the size of the `OpType` enum.

