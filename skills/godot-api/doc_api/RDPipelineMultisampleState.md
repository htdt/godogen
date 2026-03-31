## RDPipelineMultisampleState <- RefCounted

RDPipelineMultisampleState is used to control how multisample or supersample antialiasing is being performed when rendering using RenderingDevice.

**Props:**
- enable_alpha_to_coverage: bool = false
- enable_alpha_to_one: bool = false
- enable_sample_shading: bool = false
- min_sample_shading: float = 0.0
- sample_count: int (RenderingDevice.TextureSamples) = 0
- sample_masks: int[] = []

- **enable_alpha_to_coverage**: If `true`, alpha to coverage is enabled. This generates a temporary coverage value based on the alpha component of the fragment's first color output. This allows alpha transparency to make use of multisample antialiasing.
- **enable_alpha_to_one**: If `true`, alpha is forced to either `0.0` or `1.0`. This allows hardening the edges of antialiased alpha transparencies. Only relevant if `enable_alpha_to_coverage` is `true`.
- **enable_sample_shading**: If `true`, enables per-sample shading which replaces MSAA by SSAA. This provides higher quality antialiasing that works with transparent (alpha scissor) edges. This has a very high performance cost. See also `min_sample_shading`. See the for more details.
- **min_sample_shading**: The multiplier of `sample_count` that determines how many samples are performed for each fragment. Must be between `0.0` and `1.0` (inclusive). Only effective if `enable_sample_shading` is `true`. If `min_sample_shading` is `1.0`, fragment invocation must only read from the coverage index sample. Tile image access must not be used if `enable_sample_shading` is *not* `1.0`.
- **sample_count**: The number of MSAA samples (or SSAA samples if `enable_sample_shading` is `true`) to perform. Higher values result in better antialiasing, at the cost of performance.
- **sample_masks**: The sample mask array. See the for more details.

