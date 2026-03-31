## RDPipelineDepthStencilState <- RefCounted

RDPipelineDepthStencilState controls the way depth and stencil comparisons are performed when sampling those values using RenderingDevice.

**Props:**
- back_op_compare: int (RenderingDevice.CompareOperator) = 7
- back_op_compare_mask: int = 0
- back_op_depth_fail: int (RenderingDevice.StencilOperation) = 1
- back_op_fail: int (RenderingDevice.StencilOperation) = 1
- back_op_pass: int (RenderingDevice.StencilOperation) = 1
- back_op_reference: int = 0
- back_op_write_mask: int = 0
- depth_compare_operator: int (RenderingDevice.CompareOperator) = 7
- depth_range_max: float = 0.0
- depth_range_min: float = 0.0
- enable_depth_range: bool = false
- enable_depth_test: bool = false
- enable_depth_write: bool = false
- enable_stencil: bool = false
- front_op_compare: int (RenderingDevice.CompareOperator) = 7
- front_op_compare_mask: int = 0
- front_op_depth_fail: int (RenderingDevice.StencilOperation) = 1
- front_op_fail: int (RenderingDevice.StencilOperation) = 1
- front_op_pass: int (RenderingDevice.StencilOperation) = 1
- front_op_reference: int = 0
- front_op_write_mask: int = 0

- **back_op_compare**: The method used for comparing the previous back stencil value and `back_op_reference`.
- **back_op_compare_mask**: Selects which bits from the back stencil value will be compared.
- **back_op_depth_fail**: The operation to perform on the stencil buffer for back pixels that pass the stencil test but fail the depth test.
- **back_op_fail**: The operation to perform on the stencil buffer for back pixels that fail the stencil test.
- **back_op_pass**: The operation to perform on the stencil buffer for back pixels that pass the stencil test.
- **back_op_reference**: The value the previous back stencil value will be compared to.
- **back_op_write_mask**: Selects which bits from the back stencil value will be changed.
- **depth_compare_operator**: The method used for comparing the previous and current depth values.
- **depth_range_max**: The maximum depth that returns `true` for `enable_depth_range`.
- **depth_range_min**: The minimum depth that returns `true` for `enable_depth_range`.
- **enable_depth_range**: If `true`, each depth value will be tested to see if it is between `depth_range_min` and `depth_range_max`. If it is outside of these values, it is discarded.
- **enable_depth_test**: If `true`, enables depth testing which allows objects to be automatically occluded by other objects based on their depth. This also allows objects to be partially occluded by other objects. If `false`, objects will appear in the order they were drawn (like in Godot's 2D renderer).
- **enable_depth_write**: If `true`, writes to the depth buffer whenever the depth test returns `true`. Only works when enable_depth_test is also `true`.
- **enable_stencil**: If `true`, enables stencil testing. There are separate stencil buffers for front-facing triangles and back-facing triangles. See properties that begin with "front_op" and properties with "back_op" for each.
- **front_op_compare**: The method used for comparing the previous front stencil value and `front_op_reference`.
- **front_op_compare_mask**: Selects which bits from the front stencil value will be compared.
- **front_op_depth_fail**: The operation to perform on the stencil buffer for front pixels that pass the stencil test but fail the depth test.
- **front_op_fail**: The operation to perform on the stencil buffer for front pixels that fail the stencil test.
- **front_op_pass**: The operation to perform on the stencil buffer for front pixels that pass the stencil test.
- **front_op_reference**: The value the previous front stencil value will be compared to.
- **front_op_write_mask**: Selects which bits from the front stencil value will be changed.

