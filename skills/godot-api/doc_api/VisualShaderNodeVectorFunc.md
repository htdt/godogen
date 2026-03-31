## VisualShaderNodeVectorFunc <- VisualShaderNodeVectorBase

A visual shader node able to perform different functions using vectors.

**Props:**
- function: int (VisualShaderNodeVectorFunc.Function) = 0

- **function**: The function to be performed.

**Enums:**
**Function:** FUNC_NORMALIZE=0, FUNC_SATURATE=1, FUNC_NEGATE=2, FUNC_RECIPROCAL=3, FUNC_ABS=4, FUNC_ACOS=5, FUNC_ACOSH=6, FUNC_ASIN=7, FUNC_ASINH=8, FUNC_ATAN=9, ...
  - FUNC_NORMALIZE: Normalizes the vector so that it has a length of `1` but points in the same direction.
  - FUNC_SATURATE: Clamps the value between `0.0` and `1.0`.
  - FUNC_NEGATE: Returns the opposite value of the parameter.
  - FUNC_RECIPROCAL: Returns `1/vector`.
  - FUNC_ABS: Returns the absolute value of the parameter.
  - FUNC_ACOS: Returns the arc-cosine of the parameter.
  - FUNC_ACOSH: Returns the inverse hyperbolic cosine of the parameter.
  - FUNC_ASIN: Returns the arc-sine of the parameter.
  - FUNC_ASINH: Returns the inverse hyperbolic sine of the parameter.
  - FUNC_ATAN: Returns the arc-tangent of the parameter.
  - FUNC_ATANH: Returns the inverse hyperbolic tangent of the parameter.
  - FUNC_CEIL: Finds the nearest integer that is greater than or equal to the parameter.
  - FUNC_COS: Returns the cosine of the parameter.
  - FUNC_COSH: Returns the hyperbolic cosine of the parameter.
  - FUNC_DEGREES: Converts a quantity in radians to degrees.
  - FUNC_EXP: Base-e Exponential.
  - FUNC_EXP2: Base-2 Exponential.
  - FUNC_FLOOR: Finds the nearest integer less than or equal to the parameter.
  - FUNC_FRACT: Computes the fractional part of the argument.
  - FUNC_INVERSE_SQRT: Returns the inverse of the square root of the parameter.
  - FUNC_LOG: Natural logarithm.
  - FUNC_LOG2: Base-2 logarithm.
  - FUNC_RADIANS: Converts a quantity in degrees to radians.
  - FUNC_ROUND: Finds the nearest integer to the parameter.
  - FUNC_ROUNDEVEN: Finds the nearest even integer to the parameter.
  - FUNC_SIGN: Extracts the sign of the parameter, i.e. returns `-1` if the parameter is negative, `1` if it's positive and `0` otherwise.
  - FUNC_SIN: Returns the sine of the parameter.
  - FUNC_SINH: Returns the hyperbolic sine of the parameter.
  - FUNC_SQRT: Returns the square root of the parameter.
  - FUNC_TAN: Returns the tangent of the parameter.
  - FUNC_TANH: Returns the hyperbolic tangent of the parameter.
  - FUNC_TRUNC: Returns a value equal to the nearest integer to the parameter whose absolute value is not larger than the absolute value of the parameter.
  - FUNC_ONEMINUS: Returns `1.0 - vector`.
  - FUNC_MAX: Represents the size of the `Function` enum.

