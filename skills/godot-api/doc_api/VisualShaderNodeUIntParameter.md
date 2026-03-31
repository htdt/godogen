## VisualShaderNodeUIntParameter <- VisualShaderNodeParameter

A VisualShaderNodeParameter of type unsigned [int]. Offers additional customization for range of accepted values.

**Props:**
- default_value: int = 0
- default_value_enabled: bool = false

- **default_value**: Default value of this parameter, which will be used if not set externally. `default_value_enabled` must be enabled; defaults to `0` otherwise.
- **default_value_enabled**: If `true`, the node will have a custom default value.

