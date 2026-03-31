## VisualShaderNodeIntParameter <- VisualShaderNodeParameter

A VisualShaderNodeParameter of type [int]. Offers additional customization for range of accepted values.

**Props:**
- default_value: int = 0
- default_value_enabled: bool = false
- enum_names: PackedStringArray = PackedStringArray()
- hint: int (VisualShaderNodeIntParameter.Hint) = 0
- max: int = 100
- min: int = 0
- step: int = 1

- **default_value**: Default value of this parameter, which will be used if not set externally. `default_value_enabled` must be enabled; defaults to `0` otherwise.
- **default_value_enabled**: If `true`, the node will have a custom default value.
- **enum_names**: The names used for the enum select in the editor. `hint` must be `HINT_ENUM` for this to take effect.
- **hint**: Range hint of this node. Use it to customize valid parameter range.
- **max**: The maximum value this parameter can take. `hint` must be either `HINT_RANGE` or `HINT_RANGE_STEP` for this to take effect.
- **min**: The minimum value this parameter can take. `hint` must be either `HINT_RANGE` or `HINT_RANGE_STEP` for this to take effect.
- **step**: The step between parameter's values. Forces the parameter to be a multiple of the given value. `hint` must be `HINT_RANGE_STEP` for this to take effect.

**Enums:**
**Hint:** HINT_NONE=0, HINT_RANGE=1, HINT_RANGE_STEP=2, HINT_ENUM=3, HINT_MAX=4
  - HINT_NONE: The parameter will not constrain its value.
  - HINT_RANGE: The parameter's value must be within the specified `min`/`max` range.
  - HINT_RANGE_STEP: The parameter's value must be within the specified range, with the given `step` between values.
  - HINT_ENUM: The parameter uses an enum to associate preset values to names in the editor.
  - HINT_MAX: Represents the size of the `Hint` enum.

