## VisualShaderNodeFloatParameter <- VisualShaderNodeParameter

Translated to `uniform float` in the shader language.

**Props:**
- default_value: float = 0.0
- default_value_enabled: bool = false
- hint: int (VisualShaderNodeFloatParameter.Hint) = 0
- max: float = 1.0
- min: float = 0.0
- step: float = 0.1

- **default_value**: A default value to be assigned within the shader.
- **default_value_enabled**: Enables usage of the `default_value`.
- **hint**: A hint applied to the uniform, which controls the values it can take when set through the Inspector.
- **max**: Minimum value for range hints. Used if `hint` is set to `HINT_RANGE` or `HINT_RANGE_STEP`.
- **min**: Maximum value for range hints. Used if `hint` is set to `HINT_RANGE` or `HINT_RANGE_STEP`.
- **step**: Step (increment) value for the range hint with step. Used if `hint` is set to `HINT_RANGE_STEP`.

**Enums:**
**Hint:** HINT_NONE=0, HINT_RANGE=1, HINT_RANGE_STEP=2, HINT_MAX=3
  - HINT_NONE: No hint used.
  - HINT_RANGE: A range hint for scalar value, which limits possible input values between `min` and `max`. Translated to `hint_range(min, max)` in shader code.
  - HINT_RANGE_STEP: A range hint for scalar value with step, which limits possible input values between `min` and `max`, with a step (increment) of `step`). Translated to `hint_range(min, max, step)` in shader code.
  - HINT_MAX: Represents the size of the `Hint` enum.

