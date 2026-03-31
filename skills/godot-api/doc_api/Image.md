## Image <- Resource

Native image datatype. Contains image data which can be converted to an ImageTexture and provides commonly used *image processing* methods. The maximum width and height for an Image are `MAX_WIDTH` and `MAX_HEIGHT`. An Image cannot be assigned to a texture property of an object directly (such as `Sprite2D.texture`), and has to be converted manually to an ImageTexture first. **Note:** Methods that modify the image data cannot be used on VRAM-compressed images. Use `decompress` to convert the image to an uncompressed format first. **Note:** The maximum image size is 16384×16384 pixels due to graphics hardware limitations. Larger images may fail to import.

**Props:**
- data: Dictionary = { "data": PackedByteArray(), "format": "Lum8", "height": 0, "mipmaps": false, "width": 0 }

- **data**: Holds all the image's color data in a given format. See `Format` constants.

**Methods:**
- adjust_bcs(brightness: float, contrast: float, saturation: float) - Adjusts this image's `brightness`, `contrast`, and `saturation` by the given values. Does not work if the image is compressed (see `is_compressed`).
- blend_rect(src: Image, src_rect: Rect2i, dst: Vector2i) - Alpha-blends `src_rect` from `src` image to this image at coordinates `dst`, clipped accordingly to both image bounds. This image and `src` image **must** have the same format. `src_rect` with non-positive size is treated as empty.
- blend_rect_mask(src: Image, mask: Image, src_rect: Rect2i, dst: Vector2i) - Alpha-blends `src_rect` from `src` image to this image using `mask` image at coordinates `dst`, clipped accordingly to both image bounds. Alpha channels are required for both `src` and `mask`. `dst` pixels and `src` pixels will blend if the corresponding mask pixel's alpha value is not 0. This image and `src` image **must** have the same format. `src` image and `mask` image **must** have the same size (width and height) but they can have different formats. `src_rect` with non-positive size is treated as empty.
- blit_rect(src: Image, src_rect: Rect2i, dst: Vector2i) - Copies `src_rect` from `src` image to this image at coordinates `dst`, clipped accordingly to both image bounds. This image and `src` image **must** have the same format. `src_rect` with non-positive size is treated as empty. **Note:** The alpha channel data in `src` will overwrite the corresponding data in this image at the target position. To blend alpha channels, use `blend_rect` instead.
- blit_rect_mask(src: Image, mask: Image, src_rect: Rect2i, dst: Vector2i) - Blits `src_rect` area from `src` image to this image at the coordinates given by `dst`, clipped accordingly to both image bounds. `src` pixel is copied onto `dst` if the corresponding `mask` pixel's alpha value is not 0. This image and `src` image **must** have the same format. `src` image and `mask` image **must** have the same size (width and height) but they can have different formats. `src_rect` with non-positive size is treated as empty.
- bump_map_to_normal_map(bump_scale: float = 1.0) - Converts a bump map to a normal map. A bump map provides a height offset per-pixel, while a normal map provides a normal direction per pixel.
- clear_mipmaps() - Removes the image's mipmaps.
- compress(mode: int, source: int = 0, astc_format: int = 0) -> int - Compresses the image with a VRAM-compressed format to use less memory. Can not directly access pixel data while the image is compressed. Returns error if the chosen compression mode is not available. The `source` parameter helps to pick the best compression method for DXT and ETC2 formats. It is ignored for ASTC compression. The `astc_format` parameter is only taken into account when using ASTC compression; it is ignored for all other formats. **Note:** `compress` is only supported in editor builds. When run in an exported project, this method always returns `ERR_UNAVAILABLE`.
- compress_from_channels(mode: int, channels: int, astc_format: int = 0) -> int - Compresses the image with a VRAM-compressed format to use less memory. Can not directly access pixel data while the image is compressed. Returns error if the chosen compression mode is not available. This is an alternative to `compress` that lets the user supply the channels used in order for the compressor to pick the best DXT and ETC2 formats. For other formats (non DXT or ETC2), this argument is ignored. The `astc_format` parameter is only taken into account when using ASTC compression; it is ignored for all other formats. **Note:** `compress_from_channels` is only supported in editor builds. When run in an exported project, this method always returns `ERR_UNAVAILABLE`.
- compute_image_metrics(compared_image: Image, use_luma: bool) -> Dictionary - Compute image metrics on the current image and the compared image. This can be used to calculate the similarity between two images. The dictionary contains `max`, `mean`, `mean_squared`, `root_mean_squared` and `peak_snr`.
- convert(format: int) - Converts this image's format to the given `format`.
- copy_from(src: Image) - Copies `src` image to this image.
- create(width: int, height: int, use_mipmaps: bool, format: int) -> Image - Creates an empty image of the given size and format. If `use_mipmaps` is `true`, generates mipmaps for this image (see `generate_mipmaps`).
- create_empty(width: int, height: int, use_mipmaps: bool, format: int) -> Image - Creates an empty image of the given size and format. If `use_mipmaps` is `true`, generates mipmaps for this image (see `generate_mipmaps`).
- create_from_data(width: int, height: int, use_mipmaps: bool, format: int, data: PackedByteArray) -> Image - Creates a new image of the given size and format. Fills the image with the given raw data. If `use_mipmaps` is `true`, loads the mipmaps for this image from `data`. See `generate_mipmaps`.
- crop(width: int, height: int) - Crops the image to the given `width` and `height`. If the specified size is larger than the current size, the extra area is filled with black pixels.
- decompress() -> int - Decompresses the image if it is VRAM-compressed in a supported format. This increases memory utilization, but allows modifying the image. Returns `OK` if the format is supported, otherwise `ERR_UNAVAILABLE`. All VRAM-compressed formats supported by Godot can be decompressed with this method, except `FORMAT_ETC2_R11S`, `FORMAT_ETC2_RG11S`, and `FORMAT_ETC2_RGB8A1`.
- detect_alpha() -> int - Returns `ALPHA_BLEND` if the image has data for alpha values. Returns `ALPHA_BIT` if all the alpha values are stored in a single bit. Returns `ALPHA_NONE` if no data for alpha values is found.
- detect_used_channels(source: int = 0) -> int - Returns the color channels used by this image. If the image is compressed, the original `source` must be specified.
- fill(color: Color) - Fills the image with `color`.
- fill_rect(rect: Rect2i, color: Color) - Fills `rect` with `color`.
- fix_alpha_edges() - Blends low-alpha pixels with nearby pixels.
- flip_x() - Flips the image horizontally.
- flip_y() - Flips the image vertically.
- generate_mipmaps(renormalize: bool = false) -> int - Generates mipmaps for the image. Mipmaps are precalculated lower-resolution copies of the image that are automatically used if the image needs to be scaled down when rendered. They help improve image quality and performance when rendering. This method returns an error if the image is compressed, in a custom format, or if the image's width/height is `0`. Enabling `renormalize` when generating mipmaps for normal map textures will make sure all resulting vector values are normalized. It is possible to check if the image has mipmaps by calling `has_mipmaps` or `get_mipmap_count`. Calling `generate_mipmaps` on an image that already has mipmaps will replace existing mipmaps in the image.
- get_data() -> PackedByteArray - Returns a copy of the image's raw data.
- get_data_size() -> int - Returns size (in bytes) of the image's raw data.
- get_format() -> int - Returns this image's format.
- get_height() -> int - Returns the image's height.
- get_mipmap_count() -> int - Returns the number of mipmap levels or 0 if the image has no mipmaps. The largest main level image is not counted as a mipmap level by this method, so if you want to include it you can add 1 to this count.
- get_mipmap_offset(mipmap: int) -> int - Returns the offset where the image's mipmap with index `mipmap` is stored in the `data` dictionary.
- get_pixel(x: int, y: int) -> Color - Returns the color of the pixel at `(x, y)`. This is the same as `get_pixelv`, but with two integer arguments instead of a Vector2i argument.
- get_pixelv(point: Vector2i) -> Color - Returns the color of the pixel at `point`. This is the same as `get_pixel`, but with a Vector2i argument instead of two integer arguments.
- get_region(region: Rect2i) -> Image - Returns a new Image that is a copy of this Image's area specified with `region`.
- get_size() -> Vector2i - Returns the image's size (width and height).
- get_used_rect() -> Rect2i - Returns a Rect2i enclosing the visible portion of the image, considering each pixel with a non-zero alpha channel as visible.
- get_width() -> int - Returns the image's width.
- has_mipmaps() -> bool - Returns `true` if the image has generated mipmaps.
- is_compressed() -> bool - Returns `true` if the image is compressed.
- is_empty() -> bool - Returns `true` if the image has no data.
- is_invisible() -> bool - Returns `true` if all the image's pixels have an alpha value of 0. Returns `false` if any pixel has an alpha value higher than 0.
- linear_to_srgb() - Converts the entire image from linear encoding to nonlinear sRGB encoding by using a lookup table. Only works on images with `FORMAT_RGB8` or `FORMAT_RGBA8` formats.
- load(path: String) -> int - Loads an image from file `path`. See for a list of supported image formats and limitations. **Warning:** This method should only be used in the editor or in cases when you need to load external images at run-time, such as images located at the `user://` directory, and may not work in exported projects. See also ImageTexture description for usage examples.
- load_bmp_from_buffer(buffer: PackedByteArray) -> int - Loads an image from the binary contents of a BMP file. **Note:** Godot's BMP module doesn't support 16-bit per pixel images. Only 1-bit, 4-bit, 8-bit, 24-bit, and 32-bit per pixel images are supported. **Note:** This method is only available in engine builds with the BMP module enabled. By default, the BMP module is enabled, but it can be disabled at build-time using the `module_bmp_enabled=no` SCons option.
- load_dds_from_buffer(buffer: PackedByteArray) -> int - Loads an image from the binary contents of a DDS file. **Note:** This method is only available in engine builds with the DDS module enabled. By default, the DDS module is enabled, but it can be disabled at build-time using the `module_dds_enabled=no` SCons option.
- load_exr_from_buffer(buffer: PackedByteArray) -> int - Loads an image from the binary contents of an OpenEXR file.
- load_from_file(path: String) -> Image - Creates a new Image and loads data from the specified file.
- load_jpg_from_buffer(buffer: PackedByteArray) -> int - Loads an image from the binary contents of a JPEG file.
- load_ktx_from_buffer(buffer: PackedByteArray) -> int - Loads an image from the binary contents of a file. Unlike most image formats, KTX can store VRAM-compressed data and embed mipmaps. **Note:** Godot's libktx implementation only supports 2D images. Cubemaps, texture arrays, and de-padding are not supported. **Note:** This method is only available in engine builds with the KTX module enabled. By default, the KTX module is enabled, but it can be disabled at build-time using the `module_ktx_enabled=no` SCons option.
- load_png_from_buffer(buffer: PackedByteArray) -> int - Loads an image from the binary contents of a PNG file.
- load_svg_from_buffer(buffer: PackedByteArray, scale: float = 1.0) -> int - Loads an image from the UTF-8 binary contents of an **uncompressed** SVG file (**.svg**). **Note:** Beware when using compressed SVG files (like **.svgz**), they need to be `decompressed` before loading. **Note:** This method is only available in engine builds with the SVG module enabled. By default, the SVG module is enabled, but it can be disabled at build-time using the `module_svg_enabled=no` SCons option.
- load_svg_from_string(svg_str: String, scale: float = 1.0) -> int - Loads an image from the string contents of an SVG file (**.svg**). **Note:** This method is only available in engine builds with the SVG module enabled. By default, the SVG module is enabled, but it can be disabled at build-time using the `module_svg_enabled=no` SCons option.
- load_tga_from_buffer(buffer: PackedByteArray) -> int - Loads an image from the binary contents of a TGA file. **Note:** This method is only available in engine builds with the TGA module enabled. By default, the TGA module is enabled, but it can be disabled at build-time using the `module_tga_enabled=no` SCons option.
- load_webp_from_buffer(buffer: PackedByteArray) -> int - Loads an image from the binary contents of a WebP file.
- normal_map_to_xy() - Converts the image's data to represent coordinates on a 3D plane. This is used when the image represents a normal map. A normal map can add lots of detail to a 3D surface without increasing the polygon count.
- premultiply_alpha() - Multiplies color values with alpha values. Resulting color values for a pixel are `(color * alpha)/256`. See also `CanvasItemMaterial.blend_mode`.
- resize(width: int, height: int, interpolation: int = 1) - Resizes the image to the given `width` and `height`. New pixels are calculated using the `interpolation` mode defined via `Interpolation` constants. **Note:** If the image's format is `FORMAT_RGBA4444`, `FORMAT_RGB565`, or `FORMAT_RGBE9995`, it will be temporarily converted to either `FORMAT_RGBA8` or `FORMAT_RGBAH`. This can affect the quality of the resized image.
- resize_to_po2(square: bool = false, interpolation: int = 1) - Resizes the image to the nearest power of 2 for the width and height. If `square` is `true`, sets width and height to be the same. New pixels are calculated using the `interpolation` mode defined via `Interpolation` constants.
- rgbe_to_srgb() -> Image - Converts a standard linear RGBE (Red Green Blue Exponent) image to an image that uses nonlinear sRGB encoding.
- rotate_90(direction: int) - Rotates the image in the specified `direction` by `90` degrees. The width and height of the image must be greater than `1`. If the width and height are not equal, the image will be resized.
- rotate_180() - Rotates the image by `180` degrees. The width and height of the image must be greater than `1`.
- save_dds(path: String) -> int - Saves the image as a DDS (DirectDraw Surface) file to `path`. DDS is a container format that can store textures in various compression formats, such as DXT1, DXT5, or BC7. This function will return `ERR_UNAVAILABLE` if Godot was compiled without the DDS module. **Note:** The DDS module may be disabled in certain builds, which means `save_dds` will return `ERR_UNAVAILABLE` when it is called from an exported project.
- save_dds_to_buffer() -> PackedByteArray - Saves the image as a DDS (DirectDraw Surface) file to a byte array. DDS is a container format that can store textures in various compression formats, such as DXT1, DXT5, or BC7. This function will return an empty byte array if Godot was compiled without the DDS module. **Note:** The DDS module may be disabled in certain builds, which means `save_dds_to_buffer` will return an empty byte array when it is called from an exported project.
- save_exr(path: String, grayscale: bool = false) -> int - Saves the image as an EXR file to `path`. If `grayscale` is `true` and the image has only one channel, it will be saved explicitly as monochrome rather than one red channel. This function will return `ERR_UNAVAILABLE` if Godot was compiled without the TinyEXR module.
- save_exr_to_buffer(grayscale: bool = false) -> PackedByteArray - Saves the image as an EXR file to a byte array. If `grayscale` is `true` and the image has only one channel, it will be saved explicitly as monochrome rather than one red channel. This function will return an empty byte array if Godot was compiled without the TinyEXR module.
- save_jpg(path: String, quality: float = 0.75) -> int - Saves the image as a JPEG file to `path` with the specified `quality` between `0.01` and `1.0` (inclusive). Higher `quality` values result in better-looking output at the cost of larger file sizes. Recommended `quality` values are between `0.75` and `0.90`. Even at quality `1.00`, JPEG compression remains lossy. **Note:** JPEG does not save an alpha channel. If the Image contains an alpha channel, the image will still be saved, but the resulting JPEG file won't contain the alpha channel.
- save_jpg_to_buffer(quality: float = 0.75) -> PackedByteArray - Saves the image as a JPEG file to a byte array with the specified `quality` between `0.01` and `1.0` (inclusive). Higher `quality` values result in better-looking output at the cost of larger byte array sizes (and therefore memory usage). Recommended `quality` values are between `0.75` and `0.90`. Even at quality `1.00`, JPEG compression remains lossy. **Note:** JPEG does not save an alpha channel. If the Image contains an alpha channel, the image will still be saved, but the resulting byte array won't contain the alpha channel.
- save_png(path: String) -> int - Saves the image as a PNG file to the file at `path`.
- save_png_to_buffer() -> PackedByteArray - Saves the image as a PNG file to a byte array.
- save_webp(path: String, lossy: bool = false, quality: float = 0.75) -> int - Saves the image as a WebP (Web Picture) file to the file at `path`. By default it will save lossless. If `lossy` is `true`, the image will be saved lossy, using the `quality` setting between `0.0` and `1.0` (inclusive). Lossless WebP offers more efficient compression than PNG. **Note:** The WebP format is limited to a size of 16383×16383 pixels, while PNG can save larger images.
- save_webp_to_buffer(lossy: bool = false, quality: float = 0.75) -> PackedByteArray - Saves the image as a WebP (Web Picture) file to a byte array. By default it will save lossless. If `lossy` is `true`, the image will be saved lossy, using the `quality` setting between `0.0` and `1.0` (inclusive). Lossless WebP offers more efficient compression than PNG. **Note:** The WebP format is limited to a size of 16383×16383 pixels, while PNG can save larger images.
- set_data(width: int, height: int, use_mipmaps: bool, format: int, data: PackedByteArray) - Overwrites data of an existing Image. Non-static equivalent of `create_from_data`.
- set_pixel(x: int, y: int, color: Color) - Sets the Color of the pixel at `(x, y)` to `color`. This is the same as `set_pixelv`, but with a two integer arguments instead of a Vector2i argument. **Note:** Depending on the image's format, the color set here may be clamped or lose precision. Do not assume the color returned by `get_pixel` to be identical to the one set here; any comparisons will likely need to use an approximation like `Color.is_equal_approx`. **Note:** On grayscale image formats, only the red channel of `color` is used (and alpha if relevant). The green and blue channels are ignored.
- set_pixelv(point: Vector2i, color: Color) - Sets the Color of the pixel at `point` to `color`. This is the same as `set_pixel`, but with a Vector2i argument instead of two integer arguments. **Note:** Depending on the image's format, the color set here may be clamped or lose precision. Do not assume the color returned by `get_pixelv` to be identical to the one set here; any comparisons will likely need to use an approximation like `Color.is_equal_approx`. **Note:** On grayscale image formats, only the red channel of `color` is used (and alpha if relevant). The green and blue channels are ignored.
- shrink_x2() - Shrinks the image by a factor of 2 on each axis (this divides the pixel count by 4).
- srgb_to_linear() - Converts the raw data from nonlinear sRGB encoding to linear encoding using a lookup table. Only works on images with `FORMAT_RGB8` or `FORMAT_RGBA8` formats. **Note:** The 8-bit formats required by this method are not suitable for storing linearly encoded values; a significant amount of color information will be lost in darker values. To maintain image quality, this method should not be used.

**Enums:**
**Constants:** MAX_WIDTH=16777216, MAX_HEIGHT=16777216
  - MAX_WIDTH: The maximal width allowed for Image resources.
  - MAX_HEIGHT: The maximal height allowed for Image resources.
**Format:** FORMAT_L8=0, FORMAT_LA8=1, FORMAT_R8=2, FORMAT_RG8=3, FORMAT_RGB8=4, FORMAT_RGBA8=5, FORMAT_RGBA4444=6, FORMAT_RGB565=7, FORMAT_RF=8, FORMAT_RGF=9, ...
  - FORMAT_L8: Texture format with a single 8-bit depth representing luminance.
  - FORMAT_LA8: OpenGL texture format with two values, luminance and alpha each stored with 8 bits.
  - FORMAT_R8: OpenGL texture format `RED` with a single component and a bitdepth of 8.
  - FORMAT_RG8: OpenGL texture format `RG` with two components and a bitdepth of 8 for each.
  - FORMAT_RGB8: OpenGL texture format `RGB` with three components, each with a bitdepth of 8. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_RGBA8: OpenGL texture format `RGBA` with four components, each with a bitdepth of 8. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_RGBA4444: OpenGL texture format `RGBA` with four components, each with a bitdepth of 4.
  - FORMAT_RGB565: OpenGL texture format `RGB` with three components. Red and blue have a bitdepth of 5, and green has a bitdepth of 6.
  - FORMAT_RF: OpenGL texture format `GL_R32F` where there's one component, a 32-bit floating-point value.
  - FORMAT_RGF: OpenGL texture format `GL_RG32F` where there are two components, each a 32-bit floating-point values.
  - FORMAT_RGBF: OpenGL texture format `GL_RGB32F` where there are three components, each a 32-bit floating-point values.
  - FORMAT_RGBAF: OpenGL texture format `GL_RGBA32F` where there are four components, each a 32-bit floating-point values.
  - FORMAT_RH: OpenGL texture format `GL_R16F` where there's one component, a 16-bit "half-precision" floating-point value.
  - FORMAT_RGH: OpenGL texture format `GL_RG16F` where there are two components, each a 16-bit "half-precision" floating-point value.
  - FORMAT_RGBH: OpenGL texture format `GL_RGB16F` where there are three components, each a 16-bit "half-precision" floating-point value.
  - FORMAT_RGBAH: OpenGL texture format `GL_RGBA16F` where there are four components, each a 16-bit "half-precision" floating-point value.
  - FORMAT_RGBE9995: A special OpenGL texture format where the three color components have 9 bits of precision and all three share a single 5-bit exponent.
  - FORMAT_DXT1: The texture format that uses Block Compression 1, and is the smallest variation of S3TC, only providing 1 bit of alpha and color data being premultiplied with alpha. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_DXT3: The texture format that uses Block Compression 2, and color data is interpreted as not having been premultiplied by alpha. Well suited for images with sharp alpha transitions between translucent and opaque areas. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_DXT5: The texture format also known as Block Compression 3 or BC3 that contains 64 bits of alpha channel data followed by 64 bits of DXT1-encoded color data. Color data is not premultiplied by alpha, same as DXT3. DXT5 generally produces superior results for transparent gradients compared to DXT3. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_RGTC_R: Texture format that uses , normalizing the red channel data using the same compression algorithm that DXT5 uses for the alpha channel.
  - FORMAT_RGTC_RG: Texture format that uses , normalizing the red and green channel data using the same compression algorithm that DXT5 uses for the alpha channel.
  - FORMAT_BPTC_RGBA: Texture format that uses compression with unsigned normalized RGBA components. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_BPTC_RGBF: Texture format that uses compression with signed floating-point RGB components.
  - FORMAT_BPTC_RGBFU: Texture format that uses compression with unsigned floating-point RGB components.
  - FORMAT_ETC: , also referred to as "ETC1", and is part of the OpenGL ES graphics standard. This format cannot store an alpha channel.
  - FORMAT_ETC2_R11: (`R11_EAC` variant), which provides one channel of unsigned data.
  - FORMAT_ETC2_R11S: (`SIGNED_R11_EAC` variant), which provides one channel of signed data.
  - FORMAT_ETC2_RG11: (`RG11_EAC` variant), which provides two channels of unsigned data.
  - FORMAT_ETC2_RG11S: (`SIGNED_RG11_EAC` variant), which provides two channels of signed data.
  - FORMAT_ETC2_RGB8: (`RGB8` variant), which is a follow-up of ETC1 and compresses RGB888 data. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_ETC2_RGBA8: (`RGBA8`variant), which compresses RGBA8888 data with full alpha support. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_ETC2_RGB8A1: (`RGB8_PUNCHTHROUGH_ALPHA1` variant), which compresses RGBA data to make alpha either fully transparent or fully opaque. **Note:** When creating an ImageTexture, a nonlinear sRGB to linear encoding conversion is performed.
  - FORMAT_ETC2_RA_AS_RG: (`RGBA8` variant), which compresses RA data and interprets it as two channels (red and green). See also `FORMAT_ETC2_RGBA8`.
  - FORMAT_DXT5_RA_AS_RG: The texture format also known as Block Compression 3 or BC3, which compresses RA data and interprets it as two channels (red and green). See also `FORMAT_DXT5`.
  - FORMAT_ASTC_4x4: . This implements the 4×4 (high quality) mode.
  - FORMAT_ASTC_4x4_HDR: Same format as `FORMAT_ASTC_4x4`, but with the hint to let the GPU know it is used for HDR.
  - FORMAT_ASTC_8x8: . This implements the 8×8 (low quality) mode.
  - FORMAT_ASTC_8x8_HDR: Same format as `FORMAT_ASTC_8x8`, but with the hint to let the GPU know it is used for HDR.
  - FORMAT_R16: OpenGL texture format `GL_R16` where there's one component, a 16-bit unsigned normalized integer value. Since the value is normalized, each component is clamped between `0.0` and `1.0` (inclusive). **Note:** Due to limited hardware support, it is mainly recommended to be used on desktop or console devices. It may be unsupported on mobile or web, and will consequently be converted to `FORMAT_RF`.
  - FORMAT_RG16: OpenGL texture format `GL_RG16` where there are two components, each a 16-bit unsigned normalized integer value. Since the value is normalized, each component is clamped between `0.0` and `1.0` (inclusive). **Note:** Due to limited hardware support, it is mainly recommended to be used on desktop or console devices. It may be unsupported on mobile or web, and will consequently be converted to `FORMAT_RGF`.
  - FORMAT_RGB16: OpenGL texture format `GL_RGB16` where there are three components, each a 16-bit unsigned normalized integer value. Since the value is normalized, each component is clamped between `0.0` and `1.0` (inclusive). **Note:** Due to limited hardware support, it is mainly recommended to be used on desktop or console devices. It may be unsupported on mobile or web, and will consequently be converted to `FORMAT_RGBF`.
  - FORMAT_RGBA16: OpenGL texture format `GL_RGBA16` where there are four components, each a 16-bit unsigned normalized integer value. Since the value is normalized, each component is clamped between `0.0` and `1.0` (inclusive). **Note:** Due to limited hardware support, it is mainly recommended to be used on desktop or console devices. It may be unsupported on mobile or web, and will consequently be converted to `FORMAT_RGBAF`.
  - FORMAT_R16I: OpenGL texture format `GL_R16UI` where there's one component, a 16-bit unsigned integer value. Each component is clamped between `0` and `65535` (inclusive). **Note:** When used in a shader, the texture requires usage of `usampler` samplers. Additionally, it only supports nearest-neighbor filtering under the Compatibility renderer. **Note:** When sampling using `Image.get_pixel`, returned Colors have to be divided by `65535` to get the correct color value.
  - FORMAT_RG16I: OpenGL texture format `GL_RG16UI` where there are two components, each a 16-bit unsigned integer value. Each component is clamped between `0` and `65535` (inclusive). **Note:** When used in a shader, the texture requires usage of `usampler` samplers. Additionally, it only supports nearest-neighbor filtering under the Compatibility renderer. **Note:** When sampling using `Image.get_pixel`, returned Colors have to be divided by `65535` to get the correct color value.
  - FORMAT_RGB16I: OpenGL texture format `GL_RGB16UI` where there are three components, each a 16-bit unsigned integer value. Each component is clamped between `0` and `65535` (inclusive). **Note:** When used in a shader, the texture requires usage of `usampler` samplers. Additionally, it only supports nearest-neighbor filtering under the Compatibility renderer. **Note:** When sampling using `Image.get_pixel`, returned Colors have to be divided by `65535` to get the correct color value.
  - FORMAT_RGBA16I: OpenGL texture format `GL_RGBA16UI` where there are four components, each a 16-bit unsigned integer value. Each component is clamped between `0` and `65535` (inclusive). **Note:** When used in a shader, the texture requires usage of `usampler` samplers. Additionally, it only supports nearest-neighbor filtering under the Compatibility renderer. **Note:** When sampling using `Image.get_pixel`, returned Colors have to be divided by `65535` to get the correct color value.
  - FORMAT_MAX: Represents the size of the `Format` enum.
**Interpolation:** INTERPOLATE_NEAREST=0, INTERPOLATE_BILINEAR=1, INTERPOLATE_CUBIC=2, INTERPOLATE_TRILINEAR=3, INTERPOLATE_LANCZOS=4
  - INTERPOLATE_NEAREST: Performs nearest-neighbor interpolation. If the image is resized, it will be pixelated.
  - INTERPOLATE_BILINEAR: Performs bilinear interpolation. If the image is resized, it will be blurry. This mode is faster than `INTERPOLATE_CUBIC`, but it results in lower quality.
  - INTERPOLATE_CUBIC: Performs cubic interpolation. If the image is resized, it will be blurry. This mode often gives better results compared to `INTERPOLATE_BILINEAR`, at the cost of being slower.
  - INTERPOLATE_TRILINEAR: Performs bilinear separately on the two most-suited mipmap levels, then linearly interpolates between them. It's slower than `INTERPOLATE_BILINEAR`, but produces higher-quality results with far fewer aliasing artifacts. If the image does not have mipmaps, they will be generated and used internally, but no mipmaps will be generated on the resulting image. **Note:** If you intend to scale multiple copies of the original image, it's better to call `generate_mipmaps`] on it in advance, to avoid wasting processing power in generating them again and again. On the other hand, if the image already has mipmaps, they will be used, and a new set will be generated for the resulting image.
  - INTERPOLATE_LANCZOS: Performs Lanczos interpolation. This is the slowest image resizing mode, but it typically gives the best results, especially when downscaling images.
**AlphaMode:** ALPHA_NONE=0, ALPHA_BIT=1, ALPHA_BLEND=2
  - ALPHA_NONE: Image is fully opaque. It does not store alpha data.
  - ALPHA_BIT: Image stores either fully opaque or fully transparent pixels. Also known as punchthrough alpha.
  - ALPHA_BLEND: Image stores alpha data with values varying between `0.0` and `1.0`.
**CompressMode:** COMPRESS_S3TC=0, COMPRESS_ETC=1, COMPRESS_ETC2=2, COMPRESS_BPTC=3, COMPRESS_ASTC=4, COMPRESS_MAX=5
  - COMPRESS_S3TC: Use S3TC compression.
  - COMPRESS_ETC: Use ETC compression.
  - COMPRESS_ETC2: Use ETC2 compression.
  - COMPRESS_BPTC: Use BPTC compression.
  - COMPRESS_ASTC: Use ASTC compression.
  - COMPRESS_MAX: Represents the size of the `CompressMode` enum.
**UsedChannels:** USED_CHANNELS_L=0, USED_CHANNELS_LA=1, USED_CHANNELS_R=2, USED_CHANNELS_RG=3, USED_CHANNELS_RGB=4, USED_CHANNELS_RGBA=5
  - USED_CHANNELS_L: The image only uses one channel for luminance (grayscale).
  - USED_CHANNELS_LA: The image uses two channels for luminance and alpha, respectively.
  - USED_CHANNELS_R: The image only uses the red channel.
  - USED_CHANNELS_RG: The image uses two channels for red and green.
  - USED_CHANNELS_RGB: The image uses three channels for red, green, and blue.
  - USED_CHANNELS_RGBA: The image uses four channels for red, green, blue, and alpha.
**CompressSource:** COMPRESS_SOURCE_GENERIC=0, COMPRESS_SOURCE_SRGB=1, COMPRESS_SOURCE_NORMAL=2
  - COMPRESS_SOURCE_GENERIC: Source texture (before compression) is a regular texture. Default for all textures.
  - COMPRESS_SOURCE_SRGB: Source texture (before compression) uses nonlinear sRGB encoding.
  - COMPRESS_SOURCE_NORMAL: Source texture (before compression) is a normal texture (e.g. it can be compressed into two channels).
**ASTCFormat:** ASTC_FORMAT_4x4=0, ASTC_FORMAT_8x8=1
  - ASTC_FORMAT_4x4: Hint to indicate that the high quality 4×4 ASTC compression format should be used.
  - ASTC_FORMAT_8x8: Hint to indicate that the low quality 8×8 ASTC compression format should be used.

