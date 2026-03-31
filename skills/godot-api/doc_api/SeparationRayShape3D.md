## SeparationRayShape3D <- Shape3D

A 3D ray shape, intended for use in physics. Usually used to provide a shape for a CollisionShape3D. When a SeparationRayShape3D collides with an object, it tries to separate itself from it by moving its endpoint to the collision point. For example, a SeparationRayShape3D next to a character can allow it to instantly move up when touching stairs.

**Props:**
- length: float = 1.0
- slide_on_slope: bool = false

- **length**: The ray's length.
- **slide_on_slope**: If `false` (default), the shape always separates and returns a normal along its own direction. If `true`, the shape can return the correct normal and separate in any direction, allowing sliding motion on slopes.

