## WorldBoundaryShape3D <- Shape3D

A 3D world boundary shape, intended for use in physics. WorldBoundaryShape3D works like an infinite plane that forces all physics bodies to stay above it. The `plane`'s normal determines which direction is considered as "above" and in the editor, the line over the plane represents this direction. It can for example be used for endless flat floors. **Note:** When the physics engine is set to **Jolt Physics** in the project settings (`ProjectSettings.physics/3d/physics_engine`), WorldBoundaryShape3D has a finite size (centered at the shape's origin). It can be adjusted by changing `ProjectSettings.physics/jolt_physics_3d/limits/world_boundary_shape_size`.

**Props:**
- plane: Plane = Plane(0, 1, 0, 0)

- **plane**: The Plane used by the WorldBoundaryShape3D for collision.

