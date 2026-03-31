## ExternalTexture <- Texture2D

Displays the content of an external buffer provided by the platform. Requires the extension (OpenGL) or extension (Vulkan). **Note:** This is currently only supported in Android builds.

**Props:**
- resource_local_to_scene: bool = false
- size: Vector2 = Vector2(256, 256)

- **size**: External texture size.

**Methods:**
- get_external_texture_id() -> int - Returns the external texture ID. Depending on your use case, you may need to pass this to platform APIs, for example, when creating an `android.graphics.SurfaceTexture` on Android.
- set_external_buffer_id(external_buffer_id: int) - Sets the external buffer ID. Depending on your use case, you may need to call this with data received from a platform API, for example, `SurfaceTexture.getHardwareBuffer()` on Android.

