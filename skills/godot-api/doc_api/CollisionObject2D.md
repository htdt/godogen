## CollisionObject2D <- Node2D

Abstract base class for 2D physics objects. CollisionObject2D can hold any number of Shape2Ds for collision. Each shape must be assigned to a *shape owner*. Shape owners are not nodes and do not appear in the editor, but are accessible through code using the `shape_owner_*` methods. **Note:** Only collisions between objects within the same canvas (Viewport canvas or CanvasLayer) are supported. The behavior of collisions between objects in different canvases is undefined.

**Props:**
- collision_layer: int = 1
- collision_mask: int = 1
- collision_priority: float = 1.0
- disable_mode: int (CollisionObject2D.DisableMode) = 0
- input_pickable: bool = true

- **collision_layer**: The physics layers this CollisionObject2D is in. Collision objects can exist in one or more of 32 different layers. See also `collision_mask`. **Note:** Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See in the documentation for more information.
- **collision_mask**: The physics layers this CollisionObject2D scans. Collision objects can scan one or more of 32 different layers. See also `collision_layer`. **Note:** Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See in the documentation for more information.
- **collision_priority**: The priority used to solve colliding when occurring penetration. The higher the priority is, the lower the penetration into the object will be. This can for example be used to prevent the player from breaking through the boundaries of a level.
- **disable_mode**: Defines the behavior in physics when `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`.
- **input_pickable**: If `true`, this object is pickable. A pickable object can detect the mouse pointer entering/leaving, and if the mouse is inside it, report input events. Requires at least one `collision_layer` bit to be set.

**Methods:**
- _input_event(viewport: Viewport, event: InputEvent, shape_idx: int) - Accepts unhandled InputEvents. `shape_idx` is the child index of the clicked Shape2D. Connect to `input_event` to easily pick up these events. **Note:** `_input_event` requires `input_pickable` to be `true` and at least one `collision_layer` bit to be set.
- _mouse_enter() - Called when the mouse pointer enters any of this object's shapes. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be set. Note that moving between different shapes within a single CollisionObject2D won't cause this function to be called.
- _mouse_exit() - Called when the mouse pointer exits all this object's shapes. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be set. Note that moving between different shapes within a single CollisionObject2D won't cause this function to be called.
- _mouse_shape_enter(shape_idx: int) - Called when the mouse pointer enters any of this object's shapes or moves from one shape to another. `shape_idx` is the child index of the newly entered Shape2D. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be called.
- _mouse_shape_exit(shape_idx: int) - Called when the mouse pointer exits any of this object's shapes. `shape_idx` is the child index of the exited Shape2D. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be called.
- create_shape_owner(owner: Object) -> int - Creates a new shape owner for the given object. Returns `owner_id` of the new owner for future reference.
- get_collision_layer_value(layer_number: int) -> bool - Returns whether or not the specified layer of the `collision_layer` is enabled, given a `layer_number` between 1 and 32.
- get_collision_mask_value(layer_number: int) -> bool - Returns whether or not the specified layer of the `collision_mask` is enabled, given a `layer_number` between 1 and 32.
- get_rid() -> RID - Returns the object's RID.
- get_shape_owner_one_way_collision_direction(owner_id: int) -> Vector2 - Returns the `one_way_collision_direction` of the shape owner identified by the given `owner_id`.
- get_shape_owner_one_way_collision_margin(owner_id: int) -> float - Returns the `one_way_collision_margin` of the shape owner identified by given `owner_id`.
- get_shape_owners() -> PackedInt32Array - Returns an Array of `owner_id` identifiers. You can use these ids in other methods that take `owner_id` as an argument.
- is_shape_owner_disabled(owner_id: int) -> bool - If `true`, the shape owner and its shapes are disabled.
- is_shape_owner_one_way_collision_enabled(owner_id: int) -> bool - Returns `true` if collisions for the shape owner originating from this CollisionObject2D will not be reported to collided with CollisionObject2Ds.
- remove_shape_owner(owner_id: int) - Removes the given shape owner.
- set_collision_layer_value(layer_number: int, value: bool) - Based on `value`, enables or disables the specified layer in the `collision_layer`, given a `layer_number` between 1 and 32.
- set_collision_mask_value(layer_number: int, value: bool) - Based on `value`, enables or disables the specified layer in the `collision_mask`, given a `layer_number` between 1 and 32.
- shape_find_owner(shape_index: int) -> int - Returns the `owner_id` of the given shape.
- shape_owner_add_shape(owner_id: int, shape: Shape2D) - Adds a Shape2D to the shape owner.
- shape_owner_clear_shapes(owner_id: int) - Removes all shapes from the shape owner.
- shape_owner_get_owner(owner_id: int) -> Object - Returns the parent object of the given shape owner.
- shape_owner_get_shape(owner_id: int, shape_id: int) -> Shape2D - Returns the Shape2D with the given ID from the given shape owner.
- shape_owner_get_shape_count(owner_id: int) -> int - Returns the number of shapes the given shape owner contains.
- shape_owner_get_shape_index(owner_id: int, shape_id: int) -> int - Returns the child index of the Shape2D with the given ID from the given shape owner.
- shape_owner_get_transform(owner_id: int) -> Transform2D - Returns the shape owner's Transform2D.
- shape_owner_remove_shape(owner_id: int, shape_id: int) - Removes a shape from the given shape owner.
- shape_owner_set_disabled(owner_id: int, disabled: bool) - If `true`, disables the given shape owner.
- shape_owner_set_one_way_collision(owner_id: int, enable: bool) - If `enable` is `true`, collisions for the shape owner originating from this CollisionObject2D will not be reported to collided with CollisionObject2Ds.
- shape_owner_set_one_way_collision_direction(owner_id: int, p_direction: Vector2) - Sets the `one_way_collision_direction` of the shape owner identified by the given `owner_id` to `p_direction`.
- shape_owner_set_one_way_collision_margin(owner_id: int, margin: float) - Sets the `one_way_collision_margin` of the shape owner identified by given `owner_id` to `margin` pixels.
- shape_owner_set_transform(owner_id: int, transform: Transform2D) - Sets the Transform2D of the given shape owner.

**Signals:**
- input_event(viewport: Node, event: InputEvent, shape_idx: int) - Emitted when an input event occurs. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be set. See `_input_event` for details.
- mouse_entered - Emitted when the mouse pointer enters any of this object's shapes. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be set. Note that moving between different shapes within a single CollisionObject2D won't cause this signal to be emitted. **Note:** Due to the lack of continuous collision detection, this signal may not be emitted in the expected order if the mouse moves fast enough and the CollisionObject2D's area is small. This signal may also not be emitted if another CollisionObject2D is overlapping the CollisionObject2D in question.
- mouse_exited - Emitted when the mouse pointer exits all this object's shapes. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be set. Note that moving between different shapes within a single CollisionObject2D won't cause this signal to be emitted. **Note:** Due to the lack of continuous collision detection, this signal may not be emitted in the expected order if the mouse moves fast enough and the CollisionObject2D's area is small. This signal may also not be emitted if another CollisionObject2D is overlapping the CollisionObject2D in question.
- mouse_shape_entered(shape_idx: int) - Emitted when the mouse pointer enters any of this object's shapes or moves from one shape to another. `shape_idx` is the child index of the newly entered Shape2D. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be set.
- mouse_shape_exited(shape_idx: int) - Emitted when the mouse pointer exits any of this object's shapes. `shape_idx` is the child index of the exited Shape2D. Requires `input_pickable` to be `true` and at least one `collision_layer` bit to be set.

**Enums:**
**DisableMode:** DISABLE_MODE_REMOVE=0, DISABLE_MODE_MAKE_STATIC=1, DISABLE_MODE_KEEP_ACTIVE=2
  - DISABLE_MODE_REMOVE: When `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`, remove from the physics simulation to stop all physics interactions with this CollisionObject2D. Automatically re-added to the physics simulation when the Node is processed again.
  - DISABLE_MODE_MAKE_STATIC: When `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`, make the body static. Doesn't affect Area2D. PhysicsBody2D can't be affected by forces or other bodies while static. Automatically set PhysicsBody2D back to its original mode when the Node is processed again.
  - DISABLE_MODE_KEEP_ACTIVE: When `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`, do not affect the physics simulation.

