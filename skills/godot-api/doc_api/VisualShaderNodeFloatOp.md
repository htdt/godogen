## VisualShaderNodeFloatOp <- VisualShaderNode

Applies `operator` to two floating-point inputs: `a` and `b`.

**Props:**
- operator: int (VisualShaderNodeFloatOp.Operator) = 0

- **operator**: An operator to be applied to the inputs.

**Enums:**
**Operator:** OP_ADD=0, OP_SUB=1, OP_MUL=2, OP_DIV=3, OP_MOD=4, OP_POW=5, OP_MAX=6, OP_MIN=7, OP_ATAN2=8, OP_STEP=9, ...
  - OP_ADD: Sums two numbers using `a + b`.
  - OP_SUB: Subtracts two numbers using `a - b`.
  - OP_MUL: Multiplies two numbers using `a * b`.
  - OP_DIV: Divides two numbers using `a / b`.
  - OP_MOD: Calculates the remainder of two numbers. Translates to `mod(a, b)` in the Godot Shader Language.
  - OP_POW: Raises the `a` to the power of `b`. Translates to `pow(a, b)` in the Godot Shader Language.
  - OP_MAX: Returns the greater of two numbers. Translates to `max(a, b)` in the Godot Shader Language.
  - OP_MIN: Returns the lesser of two numbers. Translates to `min(a, b)` in the Godot Shader Language.
  - OP_ATAN2: Returns the arc-tangent of the parameters. Translates to `atan(a, b)` in the Godot Shader Language.
  - OP_STEP: Generates a step function by comparing `b`(x) to `a`(edge). Returns 0.0 if `x` is smaller than `edge` and otherwise 1.0. Translates to `step(a, b)` in the Godot Shader Language.
  - OP_ENUM_SIZE: Represents the size of the `Operator` enum.

