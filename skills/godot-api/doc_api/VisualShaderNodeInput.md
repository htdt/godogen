## VisualShaderNodeInput <- VisualShaderNode

Gives access to input variables (built-ins) available for the shader. See the shading reference for the list of available built-ins for each shader type (check `Tutorials` section for link).

**Props:**
- input_name: String = "[None]"

- **input_name**: One of the several input constants in lower-case style like: "vertex" (`VERTEX`) or "point_size" (`POINT_SIZE`).

**Methods:**
- get_input_real_name() -> String - Returns a translated name of the current constant in the Godot Shader Language. E.g. `"ALBEDO"` if the `input_name` equal to `"albedo"`.

**Signals:**
- input_type_changed - Emitted when input is changed via `input_name`.

