## VisualShaderNodeRemap <- VisualShaderNode

Remap will transform the input range into output range, e.g. you can change a `0..1` value to `-2..2` etc. See `@GlobalScope.remap` for more details.

**Props:**
- op_type: int (VisualShaderNodeRemap.OpType) = 0


**Enums:**
**OpType:** OP_TYPE_SCALAR=0, OP_TYPE_VECTOR_2D=1, OP_TYPE_VECTOR_2D_SCALAR=2, OP_TYPE_VECTOR_3D=3, OP_TYPE_VECTOR_3D_SCALAR=4, OP_TYPE_VECTOR_4D=5, OP_TYPE_VECTOR_4D_SCALAR=6, OP_TYPE_MAX=7
  - OP_TYPE_SCALAR: A floating-point scalar type.
  - OP_TYPE_VECTOR_2D: A 2D vector type.
  - OP_TYPE_VECTOR_2D_SCALAR: The `value` port uses a 2D vector type, while the `input min`, `input max`, `output min`, and `output max` ports use a floating-point scalar type.
  - OP_TYPE_VECTOR_3D: A 3D vector type.
  - OP_TYPE_VECTOR_3D_SCALAR: The `value` port uses a 3D vector type, while the `input min`, `input max`, `output min`, and `output max` ports use a floating-point scalar type.
  - OP_TYPE_VECTOR_4D: A 4D vector type.
  - OP_TYPE_VECTOR_4D_SCALAR: The `value` port uses a 4D vector type, while the `input min`, `input max`, `output min`, and `output max` ports use a floating-point scalar type.
  - OP_TYPE_MAX: Represents the size of the `OpType` enum.

