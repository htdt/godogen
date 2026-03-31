## VisualShaderNodeBillboard <- VisualShaderNode

The output port of this node needs to be connected to `Model View Matrix` port of VisualShaderNodeOutput.

**Props:**
- billboard_type: int (VisualShaderNodeBillboard.BillboardType) = 1
- keep_scale: bool = false

- **billboard_type**: Controls how the object faces the camera.
- **keep_scale**: If `true`, the shader will keep the scale set for the mesh. Otherwise, the scale is lost when billboarding.

**Enums:**
**BillboardType:** BILLBOARD_TYPE_DISABLED=0, BILLBOARD_TYPE_ENABLED=1, BILLBOARD_TYPE_FIXED_Y=2, BILLBOARD_TYPE_PARTICLES=3, BILLBOARD_TYPE_MAX=4
  - BILLBOARD_TYPE_DISABLED: Billboarding is disabled and the node does nothing.
  - BILLBOARD_TYPE_ENABLED: A standard billboarding algorithm is enabled.
  - BILLBOARD_TYPE_FIXED_Y: A billboarding algorithm to rotate around Y-axis is enabled.
  - BILLBOARD_TYPE_PARTICLES: A billboarding algorithm designed to use on particles is enabled.
  - BILLBOARD_TYPE_MAX: Represents the size of the `BillboardType` enum.

