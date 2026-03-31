## RDPipelineColorBlendState <- RefCounted

This object is used by RenderingDevice.

**Props:**
- attachments: RDPipelineColorBlendStateAttachment[] = []
- blend_constant: Color = Color(0, 0, 0, 1)
- enable_logic_op: bool = false
- logic_op: int (RenderingDevice.LogicOperation) = 0

- **attachments**: The attachments that are blended together.
- **blend_constant**: The constant color to blend with. See also `RenderingDevice.draw_list_set_blend_constants`.
- **enable_logic_op**: If `true`, performs the logic operation defined in `logic_op`.
- **logic_op**: The logic operation to perform for blending. Only effective if `enable_logic_op` is `true`.

