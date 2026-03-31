## TextureLayered <- Texture

Base class for ImageTextureLayered and CompressedTextureLayered. Cannot be used directly, but contains all the functions necessary for accessing the derived resource types. See also Texture3D. Data is set on a per-layer basis. For Texture2DArrays, the layer specifies the array layer. All images need to have the same width, height and number of mipmap levels. A TextureLayered can be loaded with `ResourceLoader.load`. Internally, Godot maps these files to their respective counterparts in the target rendering driver (Vulkan, OpenGL3).

**Methods:**
- _get_format() -> int - Called when the TextureLayered's format is queried.
- _get_height() -> int - Called when the TextureLayered's height is queried.
- _get_layer_data(layer_index: int) -> Image - Called when the data for a layer in the TextureLayered is queried.
- _get_layered_type() -> int - Called when the layers' type in the TextureLayered is queried.
- _get_layers() -> int - Called when the number of layers in the TextureLayered is queried.
- _get_width() -> int - Called when the TextureLayered's width queried.
- _has_mipmaps() -> bool - Called when the presence of mipmaps in the TextureLayered is queried.
- get_format() -> int - Returns the current format being used by this texture.
- get_height() -> int - Returns the height of the texture in pixels. Height is typically represented by the Y axis.
- get_layer_data(layer: int) -> Image - Returns an Image resource with the data from specified `layer`.
- get_layered_type() -> int - Returns the TextureLayered's type. The type determines how the data is accessed, with cubemaps having special types.
- get_layers() -> int - Returns the number of referenced Images.
- get_width() -> int - Returns the width of the texture in pixels. Width is typically represented by the X axis.
- has_mipmaps() -> bool - Returns `true` if the layers have generated mipmaps.

**Enums:**
**LayeredType:** LAYERED_TYPE_2D_ARRAY=0, LAYERED_TYPE_CUBEMAP=1, LAYERED_TYPE_CUBEMAP_ARRAY=2
  - LAYERED_TYPE_2D_ARRAY: Texture is a generic Texture2DArray.
  - LAYERED_TYPE_CUBEMAP: Texture is a Cubemap, with each side in its own layer (6 in total).
  - LAYERED_TYPE_CUBEMAP_ARRAY: Texture is a CubemapArray, with each cubemap being made of 6 layers.

