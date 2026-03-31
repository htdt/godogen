## PortableCompressedTexture2D <- Texture2D

This class allows storing compressed textures as self contained (not imported) resources. For 2D usage (compressed on disk, uncompressed on VRAM), the lossy and lossless modes are recommended. For 3D usage (compressed on VRAM) it depends on the target platform. If you intend to only use desktop, S3TC or BPTC are recommended. For only mobile, ETC2 is recommended. For portable, self contained 3D textures that work on both desktop and mobile, Basis Universal is recommended (although it has a small quality cost and longer compression time as a tradeoff). This resource is intended to be created from code.

**Props:**
- keep_compressed_buffer: bool = false
- resource_local_to_scene: bool = false
- size_override: Vector2 = Vector2(0, 0)

- **keep_compressed_buffer**: If `true`, when running in the editor, this texture will keep the source-compressed data in memory, allowing the data to persist after loading. Otherwise, the source-compressed data is lost after loading and the texture can't be re-saved. **Note:** This property must be set before `create_from_image` for this to work.
- **size_override**: Allows overriding the texture's size (for 2D only).

**Methods:**
- create_from_image(image: Image, compression_mode: int, normal_map: bool = false, lossy_quality: float = 0.8) - Initializes the compressed texture from a base image. The compression mode must be provided. `normal_map` is recommended to ensure optimum quality if this image will be used as a normal map. If lossy compression is requested, the quality setting can optionally be provided. This maps to Lossy WebP compression quality.
- get_compression_mode() -> int - Return the compression mode used (valid after initialized).
- is_keeping_all_compressed_buffers() -> bool - Returns `true` if the flag is overridden for all textures of this type.
- set_basisu_compressor_params(uastc_level: int, rdo_quality_loss: float) - Sets the compressor parameters for Basis Universal compression. See also the settings in ResourceImporterTexture. **Note:** This method must be called before `create_from_image` for this to work.
- set_keep_all_compressed_buffers(keep: bool) - If `keep` is `true`, overrides the flag globally for all textures of this type. This is used primarily by the editor.

**Enums:**
**CompressionMode:** COMPRESSION_MODE_LOSSLESS=0, COMPRESSION_MODE_LOSSY=1, COMPRESSION_MODE_BASIS_UNIVERSAL=2, COMPRESSION_MODE_S3TC=3, COMPRESSION_MODE_ETC2=4, COMPRESSION_MODE_BPTC=5, COMPRESSION_MODE_ASTC=6

