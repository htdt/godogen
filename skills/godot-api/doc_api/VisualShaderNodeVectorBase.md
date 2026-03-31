## VisualShaderNodeVectorBase <- VisualShaderNode

This is an abstract class. See the derived types for descriptions of the possible operations.

**Props:**
- op_type: int (VisualShaderNodeVectorBase.OpType) = 1

- **op_type**: A vector type that this operation is performed on.

**Enums:**
**OpType:** OP_TYPE_VECTOR_2D=0, OP_TYPE_VECTOR_3D=1, OP_TYPE_VECTOR_4D=2, OP_TYPE_MAX=3
  - OP_TYPE_VECTOR_2D: A 2D vector type.
  - OP_TYPE_VECTOR_3D: A 3D vector type.
  - OP_TYPE_VECTOR_4D: A 4D vector type.
  - OP_TYPE_MAX: Represents the size of the `OpType` enum.

