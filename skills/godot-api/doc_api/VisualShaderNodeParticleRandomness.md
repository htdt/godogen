## VisualShaderNodeParticleRandomness <- VisualShaderNode

Randomness node will output pseudo-random values of the given type based on the specified minimum and maximum values.

**Props:**
- op_type: int (VisualShaderNodeParticleRandomness.OpType) = 0

- **op_type**: A type of operands and returned value.

**Enums:**
**OpType:** OP_TYPE_SCALAR=0, OP_TYPE_VECTOR_2D=1, OP_TYPE_VECTOR_3D=2, OP_TYPE_VECTOR_4D=3, OP_TYPE_MAX=4
  - OP_TYPE_SCALAR: A floating-point scalar.
  - OP_TYPE_VECTOR_2D: A 2D vector type.
  - OP_TYPE_VECTOR_3D: A 3D vector type.
  - OP_TYPE_VECTOR_4D: A 4D vector type.
  - OP_TYPE_MAX: Represents the size of the `OpType` enum.

