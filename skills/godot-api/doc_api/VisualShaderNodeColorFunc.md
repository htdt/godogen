## VisualShaderNodeColorFunc <- VisualShaderNode

Accept a Color to the input port and transform it according to `function`.

**Props:**
- function: int (VisualShaderNodeColorFunc.Function) = 0

- **function**: A function to be applied to the input color.

**Enums:**
**Function:** FUNC_GRAYSCALE=0, FUNC_HSV2RGB=1, FUNC_RGB2HSV=2, FUNC_SEPIA=3, FUNC_LINEAR_TO_SRGB=4, FUNC_SRGB_TO_LINEAR=5, FUNC_MAX=6
  - FUNC_GRAYSCALE: Converts the color to grayscale using the following formula:
  - FUNC_HSV2RGB: Converts HSV vector to RGB equivalent.
  - FUNC_RGB2HSV: Converts RGB vector to HSV equivalent.
  - FUNC_SEPIA: Applies sepia tone effect using the following formula:
  - FUNC_LINEAR_TO_SRGB: Converts color from linear encoding to nonlinear sRGB encoding using the following formula: The Compatibility renderer uses a simpler formula that may produce undefined behavior with negative input values:
  - FUNC_SRGB_TO_LINEAR: Converts color from nonlinear sRGB encoding to linear encoding using the following formula: The Compatibility renderer uses a simpler formula that behaves poorly with negative input values:
  - FUNC_MAX: Represents the size of the `Function` enum.

