## CameraFeed <- RefCounted

A camera feed gives you access to a single physical camera attached to your device. When enabled, Godot will start capturing frames from the camera which can then be used. See also CameraServer. **Note:** Many cameras will return YCbCr images which are split into two textures and need to be combined in a shader. Godot does this automatically for you if you set the environment to show the camera image in the background. **Note:** This class is currently only implemented on Linux, Android, macOS, and iOS. On other platforms no CameraFeeds will be available. To get a CameraFeed on iOS, the camera plugin from is required.

**Props:**
- feed_is_active: bool = false
- feed_transform: Transform2D = Transform2D(1, 0, 0, -1, 0, 1)
- formats: Array = []

- **feed_is_active**: If `true`, the feed is active.
- **feed_transform**: The transform applied to the camera's image.
- **formats**: Formats supported by the feed. Each entry is a Dictionary describing format parameters.

**Methods:**
- _activate_feed() -> bool - Called when the camera feed is activated.
- _deactivate_feed() - Called when the camera feed is deactivated.
- _get_formats() -> Array - Override this method to define supported formats of the camera feed.
- _set_format(index: int, parameters: Dictionary) -> bool - Override this method to set the format of the camera feed.
- get_datatype() -> int - Returns feed image data type.
- get_id() -> int - Returns the unique ID for this feed.
- get_name() -> String - Returns the camera's name.
- get_position() -> int - Returns the position of camera on the device.
- get_texture_tex_id(feed_image_type: int) -> int - Returns the texture backend ID (usable by some external libraries that need a handle to a texture to write data).
- set_external(width: int, height: int) - Sets the feed as external feed provided by another library.
- set_format(index: int, parameters: Dictionary) -> bool - Sets the feed format parameters for the given `index` in the `formats` array. Returns `true` on success. By default, the YUYV encoded stream is transformed to `FEED_RGB`. The YUYV encoded stream output format can be changed by setting `parameters`'s `output` entry to one of the following: - `"separate"` will result in `FEED_YCBCR_SEP`; - `"grayscale"` will result in desaturated `FEED_RGB`; - `"copy"` will result in `FEED_YCBCR`.
- set_name(name: String) - Sets the camera's name.
- set_position(position: int) - Sets the position of this camera.
- set_rgb_image(rgb_image: Image) - Sets RGB image for this feed.
- set_ycbcr_image(ycbcr_image: Image) - Sets YCbCr image for this feed.
- set_ycbcr_images(y_image: Image, cbcr_image: Image) - Sets Y and CbCr images for this feed.

**Signals:**
- format_changed - Emitted when the format has changed.
- frame_changed - Emitted when a new frame is available.

**Enums:**
**FeedDataType:** FEED_NOIMAGE=0, FEED_RGB=1, FEED_YCBCR=2, FEED_YCBCR_SEP=3, FEED_EXTERNAL=4
  - FEED_NOIMAGE: No image set for the feed.
  - FEED_RGB: Feed supplies RGB images.
  - FEED_YCBCR: Feed supplies YCbCr images that need to be converted to RGB.
  - FEED_YCBCR_SEP: Feed supplies separate Y and CbCr images that need to be combined and converted to RGB.
  - FEED_EXTERNAL: Feed supplies external image.
**FeedPosition:** FEED_UNSPECIFIED=0, FEED_FRONT=1, FEED_BACK=2
  - FEED_UNSPECIFIED: Unspecified position.
  - FEED_FRONT: Camera is mounted at the front of the device.
  - FEED_BACK: Camera is mounted at the back of the device.

