## PanoramaSkyMaterial <- Material

A resource referenced in a Sky that is used to draw a background. PanoramaSkyMaterial functions similar to skyboxes in other engines, except it uses an equirectangular sky map instead of a Cubemap. Using an HDR panorama is strongly recommended for accurate, high-quality reflections. Godot supports the Radiance HDR (`.hdr`) and OpenEXR (`.exr`) image formats for this purpose. You can use to convert a cubemap to an equirectangular sky map.

**Props:**
- energy_multiplier: float = 1.0
- filter: bool = true
- panorama: Texture2D

- **energy_multiplier**: The sky's overall brightness multiplier. Higher values result in a brighter sky.
- **filter**: A boolean value to determine if the background texture should be filtered or not.
- **panorama**: Texture2D to be applied to the PanoramaSkyMaterial.

