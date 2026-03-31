## VisualShaderNodeSmoothStep <- VisualShaderNode

Translates to `smoothstep(edge0, edge1, x)` in the shader language. Returns `0.0` if `x` is smaller than `edge0` and `1.0` if `x` is larger than `edge1`. Otherwise, the return value is interpolated between `0.0` and `1.0` using Hermite polynomials.

**Props:**
- op_type: int (VisualShaderNodeSmoothStep.OpType) = 0

- **op_type**: A type of operands and returned value.

**Enums:**
**OpType:** OP_TYPE_SCALAR=0, OP_TYPE_VECTOR_2D=1, OP_TYPE_VECTOR_2D_SCALAR=2, OP_TYPE_VECTOR_3D=3, OP_TYPE_VECTOR_3D_SCALAR=4, OP_TYPE_VECTOR_4D=5, OP_TYPE_VECTOR_4D_SCALAR=6, OP_TYPE_MAX=7
  - OP_TYPE_SCALAR: A floating-point scalar type.
  - OP_TYPE_VECTOR_2D: A 2D vector type.
  - OP_TYPE_VECTOR_2D_SCALAR: The `x` port uses a 2D vector type. The first two ports use a floating-point scalar type.
  - OP_TYPE_VECTOR_3D: A 3D vector type.
  - OP_TYPE_VECTOR_3D_SCALAR: The `x` port uses a 3D vector type. The first two ports use a floating-point scalar type.
  - OP_TYPE_VECTOR_4D: A 4D vector type.
  - OP_TYPE_VECTOR_4D_SCALAR: The `a` and `b` ports use a 4D vector type. The `weight` port uses a scalar type.
  - OP_TYPE_MAX: Represents the size of the `OpType` enum.

