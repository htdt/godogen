## PointLight2D <- Light2D

Casts light in a 2D environment. This light's shape is defined by a (usually grayscale) texture.

**Props:**
- height: float = 0.0
- offset: Vector2 = Vector2(0, 0)
- texture: Texture2D
- texture_scale: float = 1.0

- **height**: The height of the light. Used with 2D normal mapping. The units are in pixels, e.g. if the height is 100, then it will illuminate an object 100 pixels away at a 45° angle to the plane.
- **offset**: The offset of the light's `texture`.
- **texture**: Texture2D used for the light's appearance.
- **texture_scale**: The `texture`'s scale factor.

