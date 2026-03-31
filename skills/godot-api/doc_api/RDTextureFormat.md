## RDTextureFormat <- RefCounted

This object is used by RenderingDevice.

**Props:**
- array_layers: int = 1
- depth: int = 1
- format: int (RenderingDevice.DataFormat) = 8
- height: int = 1
- is_discardable: bool = false
- is_resolve_buffer: bool = false
- mipmaps: int = 1
- samples: int (RenderingDevice.TextureSamples) = 0
- texture_type: int (RenderingDevice.TextureType) = 1
- usage_bits: int (RenderingDevice.TextureUsageBits) = 0
- width: int = 1

- **array_layers**: The number of layers in the texture. Only relevant for 2D texture arrays.
- **depth**: The texture's depth (in pixels). This is always `1` for 2D textures.
- **format**: The texture's pixel data format.
- **height**: The texture's height (in pixels).
- **is_discardable**: If a texture is discardable, its contents do not need to be preserved between frames. This flag is only relevant when the texture is used as target in a draw list. This information is used by RenderingDevice to figure out if a texture's contents can be discarded, eliminating unnecessary writes to memory and boosting performance.
- **is_resolve_buffer**: The texture will be used as the destination of a resolve operation.
- **mipmaps**: The number of mipmaps available in the texture.
- **samples**: The number of samples used when sampling the texture.
- **texture_type**: The texture type.
- **usage_bits**: The texture's usage bits, which determine what can be done using the texture.
- **width**: The texture's width (in pixels).

**Methods:**
- add_shareable_format(format: int) - Adds `format` as a valid format for the corresponding RDTextureView's `RDTextureView.format_override` property. If any format is added as shareable, then the main `format` must also be added.
- remove_shareable_format(format: int) - Removes `format` from the list of valid formats that the corresponding RDTextureView's `RDTextureView.format_override` property can be set to.

