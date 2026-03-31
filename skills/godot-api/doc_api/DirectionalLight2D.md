## DirectionalLight2D <- Light2D

A directional light is a type of Light2D node that models an infinite number of parallel rays covering the entire scene. It is used for lights with strong intensity that are located far away from the scene (for example: to model sunlight or moonlight). Light is emitted in the +Y direction of the node's global basis. For an unrotated light, this means that the light is emitted downwards. The position of the node is ignored; only the basis is used to determine light direction. **Note:** DirectionalLight2D does not support light cull masks (but it supports shadow cull masks). It will always light up 2D nodes, regardless of the 2D node's `CanvasItem.light_mask`.

**Props:**
- height: float = 0.0
- max_distance: float = 10000.0

- **height**: The height of the light. Used with 2D normal mapping. Ranges from 0 (parallel to the plane) to 1 (perpendicular to the plane).
- **max_distance**: The maximum distance from the camera center objects can be before their shadows are culled (in pixels). Decreasing this value can prevent objects located outside the camera from casting shadows (while also improving performance). `Camera2D.zoom` is not taken into account by `max_distance`, which means that at higher zoom values, shadows will appear to fade out sooner when zooming onto a given point.

