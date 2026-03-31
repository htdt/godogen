## VisualShaderNodeIntOp <- VisualShaderNode

Applies `operator` to two integer inputs: `a` and `b`.

**Props:**
- operator: int (VisualShaderNodeIntOp.Operator) = 0

- **operator**: An operator to be applied to the inputs.

**Enums:**
**Operator:** OP_ADD=0, OP_SUB=1, OP_MUL=2, OP_DIV=3, OP_MOD=4, OP_MAX=5, OP_MIN=6, OP_BITWISE_AND=7, OP_BITWISE_OR=8, OP_BITWISE_XOR=9, ...
  - OP_ADD: Sums two numbers using `a + b`.
  - OP_SUB: Subtracts two numbers using `a - b`.
  - OP_MUL: Multiplies two numbers using `a * b`.
  - OP_DIV: Divides two numbers using `a / b`.
  - OP_MOD: Calculates the remainder of two numbers using `a % b`.
  - OP_MAX: Returns the greater of two numbers. Translates to `max(a, b)` in the Godot Shader Language.
  - OP_MIN: Returns the lesser of two numbers. Translates to `max(a, b)` in the Godot Shader Language.
  - OP_BITWISE_AND: Returns the result of bitwise `AND` operation on the integer. Translates to `a & b` in the Godot Shader Language.
  - OP_BITWISE_OR: Returns the result of bitwise `OR` operation for two integers. Translates to `a | b` in the Godot Shader Language.
  - OP_BITWISE_XOR: Returns the result of bitwise `XOR` operation for two integers. Translates to `a ^ b` in the Godot Shader Language.
  - OP_BITWISE_LEFT_SHIFT: Returns the result of bitwise left shift operation on the integer. Translates to `a << b` in the Godot Shader Language.
  - OP_BITWISE_RIGHT_SHIFT: Returns the result of bitwise right shift operation on the integer. Translates to `a >> b` in the Godot Shader Language.
  - OP_ENUM_SIZE: Represents the size of the `Operator` enum.

