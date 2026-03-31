## RDUniform <- RefCounted

This object is used by RenderingDevice.

**Props:**
- binding: int = 0
- uniform_type: int (RenderingDevice.UniformType) = 3

- **binding**: The uniform's binding.
- **uniform_type**: The uniform's data type.

**Methods:**
- add_id(id: RID) - Binds the given id to the uniform. The data associated with the id is then used when the uniform is passed to a shader.
- clear_ids() - Unbinds all ids currently bound to the uniform.
- get_ids() -> RID[] - Returns an array of all ids currently bound to the uniform.

