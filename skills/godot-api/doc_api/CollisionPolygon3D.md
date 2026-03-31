## CollisionPolygon3D <- Node3D

A node that provides a thickened polygon shape (a prism) to a CollisionObject3D parent and allows it to be edited. The polygon can be concave or convex. This can give a detection shape to an Area3D or turn a PhysicsBody3D into a solid object. **Warning:** A non-uniformly scaled CollisionShape3D will likely not behave as expected. Make sure to keep its scale the same on all axes and adjust its shape resource instead.

**Props:**
- debug_color: Color = Color(0, 0, 0, 0)
- debug_fill: bool = true
- depth: float = 1.0
- disabled: bool = false
- margin: float = 0.04
- polygon: PackedVector2Array = PackedVector2Array()

- **debug_color**: The collision shape color that is displayed in the editor, or in the running project if **Debug > Visible Collision Shapes** is checked at the top of the editor. **Note:** The default value is `ProjectSettings.debug/shapes/collision/shape_color`. The `Color(0, 0, 0, 0)` value documented here is a placeholder, and not the actual default debug color.
- **debug_fill**: If `true`, when the shape is displayed, it will show a solid fill color in addition to its wireframe.
- **depth**: Length that the resulting collision extends in either direction perpendicular to its 2D polygon.
- **disabled**: If `true`, no collision will be produced. This property should be changed with `Object.set_deferred`.
- **margin**: The collision margin for the generated Shape3D. See `Shape3D.margin` for more details.
- **polygon**: Array of vertices which define the 2D polygon in the local XY plane.

