## ImageFormatLoaderExtension <- ImageFormatLoader

The engine supports multiple image formats out of the box (PNG, SVG, JPEG, WebP to name a few), but you can choose to implement support for additional image formats by extending this class. Be sure to respect the documented return types and values. You should create an instance of it, and call `add_format_loader` to register that loader during the initialization phase.

**Methods:**
- _get_recognized_extensions() -> PackedStringArray - Returns the list of file extensions for this image format. Files with the given extensions will be treated as image file and loaded using this class.
- _load_image(image: Image, fileaccess: FileAccess, flags: int, scale: float) -> int - Loads the content of `fileaccess` into the provided `image`.
- add_format_loader() - Add this format loader to the engine, allowing it to recognize the file extensions returned by `_get_recognized_extensions`.
- remove_format_loader() - Remove this format loader from the engine.

