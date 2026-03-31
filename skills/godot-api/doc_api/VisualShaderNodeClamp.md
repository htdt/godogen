## VisualShaderNodeClamp <- VisualShaderNode

Constrains a value to lie between `min` and `max` values.

**Props:**
- op_type: int (VisualShaderNodeClamp.OpType) = 0

- **op_type**: A type of operands and returned value.

**Enums:**
**OpType:** OP_TYPE_FLOAT=0, OP_TYPE_INT=1, OP_TYPE_UINT=2, OP_TYPE_VECTOR_2D=3, OP_TYPE_VECTOR_3D=4, OP_TYPE_VECTOR_4D=5, OP_TYPE_MAX=6
  - OP_TYPE_FLOAT: A floating-point scalar.
  - OP_TYPE_INT: An integer scalar.
  - OP_TYPE_UINT: An unsigned integer scalar.
  - OP_TYPE_VECTOR_2D: A 2D vector type.
  - OP_TYPE_VECTOR_3D: A 3D vector type.
  - OP_TYPE_VECTOR_4D: A 4D vector type.
  - OP_TYPE_MAX: Represents the size of the `OpType` enum.

