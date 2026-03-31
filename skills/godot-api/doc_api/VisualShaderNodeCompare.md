## VisualShaderNodeCompare <- VisualShaderNode

Compares `a` and `b` of `type` by `function`. Returns a boolean scalar. Translates to `if` instruction in shader code.

**Props:**
- condition: int (VisualShaderNodeCompare.Condition) = 0
- function: int (VisualShaderNodeCompare.Function) = 0
- type: int (VisualShaderNodeCompare.ComparisonType) = 0

- **condition**: Extra condition which is applied if `type` is set to `CTYPE_VECTOR_3D`.
- **function**: A comparison function.
- **type**: The type to be used in the comparison.

**Enums:**
**ComparisonType:** CTYPE_SCALAR=0, CTYPE_SCALAR_INT=1, CTYPE_SCALAR_UINT=2, CTYPE_VECTOR_2D=3, CTYPE_VECTOR_3D=4, CTYPE_VECTOR_4D=5, CTYPE_BOOLEAN=6, CTYPE_TRANSFORM=7, CTYPE_MAX=8
  - CTYPE_SCALAR: A floating-point scalar.
  - CTYPE_SCALAR_INT: An integer scalar.
  - CTYPE_SCALAR_UINT: An unsigned integer scalar.
  - CTYPE_VECTOR_2D: A 2D vector type.
  - CTYPE_VECTOR_3D: A 3D vector type.
  - CTYPE_VECTOR_4D: A 4D vector type.
  - CTYPE_BOOLEAN: A boolean type.
  - CTYPE_TRANSFORM: A transform (`mat4`) type.
  - CTYPE_MAX: Represents the size of the `ComparisonType` enum.
**Function:** FUNC_EQUAL=0, FUNC_NOT_EQUAL=1, FUNC_GREATER_THAN=2, FUNC_GREATER_THAN_EQUAL=3, FUNC_LESS_THAN=4, FUNC_LESS_THAN_EQUAL=5, FUNC_MAX=6
  - FUNC_EQUAL: Comparison for equality (`a == b`).
  - FUNC_NOT_EQUAL: Comparison for inequality (`a != b`).
  - FUNC_GREATER_THAN: Comparison for greater than (`a > b`). Cannot be used if `type` set to `CTYPE_BOOLEAN` or `CTYPE_TRANSFORM`.
  - FUNC_GREATER_THAN_EQUAL: Comparison for greater than or equal (`a >= b`). Cannot be used if `type` set to `CTYPE_BOOLEAN` or `CTYPE_TRANSFORM`.
  - FUNC_LESS_THAN: Comparison for less than (`a < b`). Cannot be used if `type` set to `CTYPE_BOOLEAN` or `CTYPE_TRANSFORM`.
  - FUNC_LESS_THAN_EQUAL: Comparison for less than or equal (`a <= b`). Cannot be used if `type` set to `CTYPE_BOOLEAN` or `CTYPE_TRANSFORM`.
  - FUNC_MAX: Represents the size of the `Function` enum.
**Condition:** COND_ALL=0, COND_ANY=1, COND_MAX=2
  - COND_ALL: The result will be `true` if all components in the vector satisfy the comparison condition.
  - COND_ANY: The result will be `true` if any component in the vector satisfies the comparison condition.
  - COND_MAX: Represents the size of the `Condition` enum.

