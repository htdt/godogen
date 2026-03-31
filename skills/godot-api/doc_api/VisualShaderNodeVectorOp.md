## VisualShaderNodeVectorOp <- VisualShaderNodeVectorBase

A visual shader node for use of vector operators. Operates on vector `a` and vector `b`.

**Props:**
- operator: int (VisualShaderNodeVectorOp.Operator) = 0

- **operator**: The operator to be used.

**Enums:**
**Operator:** OP_ADD=0, OP_SUB=1, OP_MUL=2, OP_DIV=3, OP_MOD=4, OP_POW=5, OP_MAX=6, OP_MIN=7, OP_CROSS=8, OP_ATAN2=9, ...
  - OP_ADD: Adds two vectors.
  - OP_SUB: Subtracts a vector from a vector.
  - OP_MUL: Multiplies two vectors.
  - OP_DIV: Divides vector by vector.
  - OP_MOD: Returns the remainder of the two vectors.
  - OP_POW: Returns the value of the first parameter raised to the power of the second, for each component of the vectors.
  - OP_MAX: Returns the greater of two values, for each component of the vectors.
  - OP_MIN: Returns the lesser of two values, for each component of the vectors.
  - OP_CROSS: Calculates the cross product of two vectors.
  - OP_ATAN2: Returns the arc-tangent of the parameters.
  - OP_REFLECT: Returns the vector that points in the direction of reflection. `a` is incident vector and `b` is the normal vector.
  - OP_STEP: Vector step operator. Returns `0.0` if `a` is smaller than `b` and `1.0` otherwise.
  - OP_ENUM_SIZE: Represents the size of the `Operator` enum.

