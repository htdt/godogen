## ResourceImporterSVG <- ResourceImporter

This importer imports DPITexture resources. See also ResourceImporterTexture and ResourceImporterImage.

**Props:**
- base_scale: float = 1.0
- color_map: Dictionary = {}
- compress: bool = true
- fix_alpha_border: bool = false
- premult_alpha: bool = false
- saturation: float = 1.0

- **base_scale**: Texture scale. `1.0` is the original SVG size. Higher values result in a larger image.
- **color_map**: If set, remaps texture colors according to Color-Color map.
- **compress**: If `true`, uses lossless compression for the SVG source.
- **fix_alpha_border**: If `true`, puts pixels of the same surrounding color in transition from transparent to opaque areas. For textures displayed with bilinear filtering, this helps to reduce the outline effect when exporting images from an image editor.
- **premult_alpha**: An alternative to fixing darkened borders with `fix_alpha_border` is to use premultiplied alpha. By enabling this option, the texture will be converted to this format. A premultiplied alpha texture requires specific materials to be displayed correctly: - In 2D, a CanvasItemMaterial will need to be created and configured to use the `CanvasItemMaterial.BLEND_MODE_PREMULT_ALPHA` blend mode on CanvasItems that use this texture. In custom `canvas_item` shaders, `render_mode blend_premul_alpha;` should be used. - In 3D, a BaseMaterial3D will need to be created and configured to use the `BaseMaterial3D.BLEND_MODE_PREMULT_ALPHA` blend mode on materials that use this texture. In custom `spatial` shaders, `render_mode blend_premul_alpha;` should be used.
- **saturation**: Overrides texture saturation.

