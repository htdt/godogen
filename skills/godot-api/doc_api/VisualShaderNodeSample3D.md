## VisualShaderNodeSample3D <- VisualShaderNode

A virtual class, use the descendants instead.

**Props:**
- source: int (VisualShaderNodeSample3D.Source) = 0

- **source**: An input source type.

**Enums:**
**Source:** SOURCE_TEXTURE=0, SOURCE_PORT=1, SOURCE_MAX=2
  - SOURCE_TEXTURE: Creates internal uniform and provides a way to assign it within node.
  - SOURCE_PORT: Use the uniform texture from sampler port.
  - SOURCE_MAX: Represents the size of the `Source` enum.

