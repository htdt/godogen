## VisualShaderNodeFloatFunc <- VisualShaderNode

Accept a floating-point scalar (`x`) to the input port and transform it according to `function`.

**Props:**
- function: int (VisualShaderNodeFloatFunc.Function) = 13

- **function**: A function to be applied to the scalar.

**Enums:**
**Function:** FUNC_SIN=0, FUNC_COS=1, FUNC_TAN=2, FUNC_ASIN=3, FUNC_ACOS=4, FUNC_ATAN=5, FUNC_SINH=6, FUNC_COSH=7, FUNC_TANH=8, FUNC_LOG=9, ...
  - FUNC_SIN: Returns the sine of the parameter. Translates to `sin(x)` in the Godot Shader Language.
  - FUNC_COS: Returns the cosine of the parameter. Translates to `cos(x)` in the Godot Shader Language.
  - FUNC_TAN: Returns the tangent of the parameter. Translates to `tan(x)` in the Godot Shader Language.
  - FUNC_ASIN: Returns the arc-sine of the parameter. Translates to `asin(x)` in the Godot Shader Language.
  - FUNC_ACOS: Returns the arc-cosine of the parameter. Translates to `acos(x)` in the Godot Shader Language.
  - FUNC_ATAN: Returns the arc-tangent of the parameter. Translates to `atan(x)` in the Godot Shader Language.
  - FUNC_SINH: Returns the hyperbolic sine of the parameter. Translates to `sinh(x)` in the Godot Shader Language.
  - FUNC_COSH: Returns the hyperbolic cosine of the parameter. Translates to `cosh(x)` in the Godot Shader Language.
  - FUNC_TANH: Returns the hyperbolic tangent of the parameter. Translates to `tanh(x)` in the Godot Shader Language.
  - FUNC_LOG: Returns the natural logarithm of the parameter. Translates to `log(x)` in the Godot Shader Language.
  - FUNC_EXP: Returns the natural exponentiation of the parameter. Translates to `exp(x)` in the Godot Shader Language.
  - FUNC_SQRT: Returns the square root of the parameter. Translates to `sqrt(x)` in the Godot Shader Language.
  - FUNC_ABS: Returns the absolute value of the parameter. Translates to `abs(x)` in the Godot Shader Language.
  - FUNC_SIGN: Extracts the sign of the parameter. Translates to `sign(x)` in the Godot Shader Language.
  - FUNC_FLOOR: Finds the nearest integer less than or equal to the parameter. Translates to `floor(x)` in the Godot Shader Language.
  - FUNC_ROUND: Finds the nearest integer to the parameter. Translates to `round(x)` in the Godot Shader Language.
  - FUNC_CEIL: Finds the nearest integer that is greater than or equal to the parameter. Translates to `ceil(x)` in the Godot Shader Language.
  - FUNC_FRACT: Computes the fractional part of the argument. Translates to `fract(x)` in the Godot Shader Language.
  - FUNC_SATURATE: Clamps the value between `0.0` and `1.0` using `min(max(x, 0.0), 1.0)`.
  - FUNC_NEGATE: Negates the `x` using `-(x)`.
  - FUNC_ACOSH: Returns the arc-hyperbolic-cosine of the parameter. Translates to `acosh(x)` in the Godot Shader Language.
  - FUNC_ASINH: Returns the arc-hyperbolic-sine of the parameter. Translates to `asinh(x)` in the Godot Shader Language.
  - FUNC_ATANH: Returns the arc-hyperbolic-tangent of the parameter. Translates to `atanh(x)` in the Godot Shader Language.
  - FUNC_DEGREES: Convert a quantity in radians to degrees. Translates to `degrees(x)` in the Godot Shader Language.
  - FUNC_EXP2: Returns 2 raised by the power of the parameter. Translates to `exp2(x)` in the Godot Shader Language.
  - FUNC_INVERSE_SQRT: Returns the inverse of the square root of the parameter. Translates to `inversesqrt(x)` in the Godot Shader Language.
  - FUNC_LOG2: Returns the base 2 logarithm of the parameter. Translates to `log2(x)` in the Godot Shader Language.
  - FUNC_RADIANS: Convert a quantity in degrees to radians. Translates to `radians(x)` in the Godot Shader Language.
  - FUNC_RECIPROCAL: Finds reciprocal value of dividing 1 by `x` (i.e. `1 / x`).
  - FUNC_ROUNDEVEN: Finds the nearest even integer to the parameter. Translates to `roundEven(x)` in the Godot Shader Language.
  - FUNC_TRUNC: Returns a value equal to the nearest integer to `x` whose absolute value is not larger than the absolute value of `x`. Translates to `trunc(x)` in the Godot Shader Language.
  - FUNC_ONEMINUS: Subtracts scalar `x` from 1 (i.e. `1 - x`).
  - FUNC_MAX: Represents the size of the `Function` enum.

