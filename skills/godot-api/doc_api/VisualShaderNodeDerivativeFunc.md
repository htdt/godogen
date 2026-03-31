## VisualShaderNodeDerivativeFunc <- VisualShaderNode

This node is only available in `Fragment` and `Light` visual shaders.

**Props:**
- function: int (VisualShaderNodeDerivativeFunc.Function) = 0
- op_type: int (VisualShaderNodeDerivativeFunc.OpType) = 0
- precision: int (VisualShaderNodeDerivativeFunc.Precision) = 0

- **function**: A derivative function type.
- **op_type**: A type of operands and returned value.
- **precision**: Sets the level of precision to use for the derivative function. When using the Compatibility renderer, this setting has no effect.

**Enums:**
**OpType:** OP_TYPE_SCALAR=0, OP_TYPE_VECTOR_2D=1, OP_TYPE_VECTOR_3D=2, OP_TYPE_VECTOR_4D=3, OP_TYPE_MAX=4
  - OP_TYPE_SCALAR: A floating-point scalar.
  - OP_TYPE_VECTOR_2D: A 2D vector type.
  - OP_TYPE_VECTOR_3D: A 3D vector type.
  - OP_TYPE_VECTOR_4D: A 4D vector type.
  - OP_TYPE_MAX: Represents the size of the `OpType` enum.
**Function:** FUNC_SUM=0, FUNC_X=1, FUNC_Y=2, FUNC_MAX=3
  - FUNC_SUM: Sum of absolute derivative in `x` and `y`.
  - FUNC_X: Derivative in `x` using local differencing.
  - FUNC_Y: Derivative in `y` using local differencing.
  - FUNC_MAX: Represents the size of the `Function` enum.
**Precision:** PRECISION_NONE=0, PRECISION_COARSE=1, PRECISION_FINE=2, PRECISION_MAX=3
  - PRECISION_NONE: No precision is specified, the GPU driver is allowed to use whatever level of precision it chooses. This is the default option and is equivalent to using `dFdx()` or `dFdy()` in text shaders.
  - PRECISION_COARSE: The derivative will be calculated using the current fragment's neighbors (which may not include the current fragment). This tends to be faster than using `PRECISION_FINE`, but may not be suitable when more precision is needed. This is equivalent to using `dFdxCoarse()` or `dFdyCoarse()` in text shaders.
  - PRECISION_FINE: The derivative will be calculated using the current fragment and its immediate neighbors. This tends to be slower than using `PRECISION_COARSE`, but may be necessary when more precision is needed. This is equivalent to using `dFdxFine()` or `dFdyFine()` in text shaders.
  - PRECISION_MAX: Represents the size of the `Precision` enum.

