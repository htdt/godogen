## CanvasTexture <- Texture2D

CanvasTexture is an alternative to ImageTexture for 2D rendering. It allows using normal maps and specular maps in any node that inherits from CanvasItem. CanvasTexture also allows overriding the texture's filter and repeat mode independently of the node's properties (or the project settings). **Note:** CanvasTexture cannot be used in 3D. It will not display correctly when applied to any VisualInstance3D, such as Sprite3D or Decal. For physically-based materials in 3D, use BaseMaterial3D instead.

**Props:**
- diffuse_texture: Texture2D
- normal_texture: Texture2D
- resource_local_to_scene: bool = false
- specular_color: Color = Color(1, 1, 1, 1)
- specular_shininess: float = 1.0
- specular_texture: Texture2D
- texture_filter: int (CanvasItem.TextureFilter) = 0
- texture_repeat: int (CanvasItem.TextureRepeat) = 0

- **diffuse_texture**: The diffuse (color) texture to use. This is the main texture you want to set in most cases.
- **normal_texture**: The normal map texture to use. Only has a visible effect if Light2Ds are affecting this CanvasTexture. **Note:** Godot expects the normal map to use X+, Y+, and Z+ coordinates. See for a comparison of normal map coordinates expected by popular engines.
- **specular_color**: The multiplier for specular reflection colors. The Light2D's color is also taken into account when determining the reflection color. Only has a visible effect if Light2Ds are affecting this CanvasTexture.
- **specular_shininess**: The specular exponent for Light2D specular reflections. Higher values result in a more glossy/"wet" look, with reflections becoming more localized and less visible overall. The default value of `1.0` disables specular reflections entirely. Only has a visible effect if Light2Ds are affecting this CanvasTexture.
- **specular_texture**: The specular map to use for Light2D specular reflections. This should be a grayscale or colored texture, with brighter areas resulting in a higher `specular_shininess` value. Using a colored `specular_texture` allows controlling specular shininess on a per-channel basis. Only has a visible effect if Light2Ds are affecting this CanvasTexture.
- **texture_filter**: The texture filtering mode to use when drawing this CanvasTexture.
- **texture_repeat**: The texture repeat mode to use when drawing this CanvasTexture.

