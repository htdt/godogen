## CollisionShape2D <- Node2D

A node that provides a Shape2D to a CollisionObject2D parent and allows it to be edited. This can give a detection shape to an Area2D or turn a PhysicsBody2D into a solid object.

**Props:**
- debug_color: Color = Color(0, 0, 0, 0)
- disabled: bool = false
- one_way_collision: bool = false
- one_way_collision_direction: Vector2 = Vector2(0, 1)
- one_way_collision_margin: float = 1.0
- shape: Shape2D

- **debug_color**: The collision shape color that is displayed in the editor, or in the running project if **Debug > Visible Collision Shapes** is checked at the top of the editor. **Note:** The default value is `ProjectSettings.debug/shapes/collision/shape_color`. The `Color(0, 0, 0, 0)` value documented here is a placeholder, and not the actual default debug color.
- **disabled**: A disabled collision shape has no effect in the world. This property should be changed with `Object.set_deferred`.
- **one_way_collision**: Sets whether this collision shape should only detect collision on one side (top or bottom). **Note:** This property has no effect if this CollisionShape2D is a child of an Area2D node. **Note:** The one way collision direction can be configured by setting `one_way_collision_direction`.
- **one_way_collision_direction**: The direction used for one-way collision.
- **one_way_collision_margin**: The margin used for one-way collision (in pixels). Higher values will make the shape thicker, and work better for colliders that enter the shape at a high velocity.
- **shape**: The actual shape owned by this collision shape.

