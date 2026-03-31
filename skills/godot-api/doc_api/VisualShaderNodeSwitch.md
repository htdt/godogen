## VisualShaderNodeSwitch <- VisualShaderNode

Returns an associated value of the `op_type` type if the provided boolean value is `true` or `false`.

**Props:**
- op_type: int (VisualShaderNodeSwitch.OpType) = 0

- **op_type**: A type of operands and returned value.

**Enums:**
**OpType:** OP_TYPE_FLOAT=0, OP_TYPE_INT=1, OP_TYPE_UINT=2, OP_TYPE_VECTOR_2D=3, OP_TYPE_VECTOR_3D=4, OP_TYPE_VECTOR_4D=5, OP_TYPE_BOOLEAN=6, OP_TYPE_TRANSFORM=7, OP_TYPE_MAX=8
  - OP_TYPE_FLOAT: A floating-point scalar.
  - OP_TYPE_INT: An integer scalar.
  - OP_TYPE_UINT: An unsigned integer scalar.
  - OP_TYPE_VECTOR_2D: A 2D vector type.
  - OP_TYPE_VECTOR_3D: A 3D vector type.
  - OP_TYPE_VECTOR_4D: A 4D vector type.
  - OP_TYPE_BOOLEAN: A boolean type.
  - OP_TYPE_TRANSFORM: A transform type.
  - OP_TYPE_MAX: Represents the size of the `OpType` enum.

