## CollisionObject3D <- Node3D

Abstract base class for 3D physics objects. CollisionObject3D can hold any number of Shape3Ds for collision. Each shape must be assigned to a *shape owner*. Shape owners are not nodes and do not appear in the editor, but are accessible through code using the `shape_owner_*` methods. **Warning:** With a non-uniform scale, this node will likely not behave as expected. It is advised to keep its scale the same on all axes and adjust its collision shape(s) instead.

**Props:**
- collision_layer: int = 1
- collision_mask: int = 1
- collision_priority: float = 1.0
- disable_mode: int (CollisionObject3D.DisableMode) = 0
- input_capture_on_drag: bool = false
- input_ray_pickable: bool = true

- **collision_layer**: The physics layers this CollisionObject3D **is in**. Collision objects can exist in one or more of 32 different layers. See also `collision_mask`. **Note:** Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See in the documentation for more information.
- **collision_mask**: The physics layers this CollisionObject3D **scans**. Collision objects can scan one or more of 32 different layers. See also `collision_layer`. **Note:** Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See in the documentation for more information.
- **collision_priority**: The priority used to solve colliding when occurring penetration. The higher the priority is, the lower the penetration into the object will be. This can for example be used to prevent the player from breaking through the boundaries of a level.
- **disable_mode**: Defines the behavior in physics when `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`.
- **input_capture_on_drag**: If `true`, the CollisionObject3D will continue to receive input events as the mouse is dragged across its shapes.
- **input_ray_pickable**: If `true`, this object is pickable. A pickable object can detect the mouse pointer entering/leaving, and if the mouse is inside it, report input events. Requires at least one `collision_layer` bit to be set.

**Methods:**
- _input_event(camera: Camera3D, event: InputEvent, event_position: Vector3, normal: Vector3, shape_idx: int) - Receives unhandled InputEvents. `event_position` is the location in world space of the mouse pointer on the surface of the shape with index `shape_idx` and `normal` is the normal vector of the surface at that point. Connect to the `input_event` signal to easily pick up these events. **Note:** `_input_event` requires `input_ray_pickable` to be `true` and at least one `collision_layer` bit to be set.
- _mouse_enter() - Called when the mouse pointer enters any of this object's shapes. Requires `input_ray_pickable` to be `true` and at least one `collision_layer` bit to be set. Note that moving between different shapes within a single CollisionObject3D won't cause this function to be called.
- _mouse_exit() - Called when the mouse pointer exits all this object's shapes. Requires `input_ray_pickable` to be `true` and at least one `collision_layer` bit to be set. Note that moving between different shapes within a single CollisionObject3D won't cause this function to be called.
- create_shape_owner(owner: Object) -> int - Creates a new shape owner for the given object. Returns `owner_id` of the new owner for future reference.
- get_collision_layer_value(layer_number: int) -> bool - Returns whether or not the specified layer of the `collision_layer` is enabled, given a `layer_number` between 1 and 32.
- get_collision_mask_value(layer_number: int) -> bool - Returns whether or not the specified layer of the `collision_mask` is enabled, given a `layer_number` between 1 and 32.
- get_rid() -> RID - Returns the object's RID.
- get_shape_owners() -> PackedInt32Array - Returns an Array of `owner_id` identifiers. You can use these ids in other methods that take `owner_id` as an argument.
- is_shape_owner_disabled(owner_id: int) -> bool - If `true`, the shape owner and its shapes are disabled.
- remove_shape_owner(owner_id: int) - Removes the given shape owner.
- set_collision_layer_value(layer_number: int, value: bool) - Based on `value`, enables or disables the specified layer in the `collision_layer`, given a `layer_number` between 1 and 32.
- set_collision_mask_value(layer_number: int, value: bool) - Based on `value`, enables or disables the specified layer in the `collision_mask`, given a `layer_number` between 1 and 32.
- shape_find_owner(shape_index: int) -> int - Returns the `owner_id` of the given shape.
- shape_owner_add_shape(owner_id: int, shape: Shape3D) - Adds a Shape3D to the shape owner.
- shape_owner_clear_shapes(owner_id: int) - Removes all shapes from the shape owner.
- shape_owner_get_owner(owner_id: int) -> Object - Returns the parent object of the given shape owner.
- shape_owner_get_shape(owner_id: int, shape_id: int) -> Shape3D - Returns the Shape3D with the given ID from the given shape owner.
- shape_owner_get_shape_count(owner_id: int) -> int - Returns the number of shapes the given shape owner contains.
- shape_owner_get_shape_index(owner_id: int, shape_id: int) -> int - Returns the child index of the Shape3D with the given ID from the given shape owner.
- shape_owner_get_transform(owner_id: int) -> Transform3D - Returns the shape owner's Transform3D.
- shape_owner_remove_shape(owner_id: int, shape_id: int) - Removes a shape from the given shape owner.
- shape_owner_set_disabled(owner_id: int, disabled: bool) - If `true`, disables the given shape owner.
- shape_owner_set_transform(owner_id: int, transform: Transform3D) - Sets the Transform3D of the given shape owner.

**Signals:**
- input_event(camera: Node, event: InputEvent, event_position: Vector3, normal: Vector3, shape_idx: int) - Emitted when the object receives an unhandled InputEvent. `event_position` is the location in world space of the mouse pointer on the surface of the shape with index `shape_idx` and `normal` is the normal vector of the surface at that point.
- mouse_entered - Emitted when the mouse pointer enters any of this object's shapes. Requires `input_ray_pickable` to be `true` and at least one `collision_layer` bit to be set. **Note:** Due to the lack of continuous collision detection, this signal may not be emitted in the expected order if the mouse moves fast enough and the CollisionObject3D's area is small. This signal may also not be emitted if another CollisionObject3D is overlapping the CollisionObject3D in question.
- mouse_exited - Emitted when the mouse pointer exits all this object's shapes. Requires `input_ray_pickable` to be `true` and at least one `collision_layer` bit to be set. **Note:** Due to the lack of continuous collision detection, this signal may not be emitted in the expected order if the mouse moves fast enough and the CollisionObject3D's area is small. This signal may also not be emitted if another CollisionObject3D is overlapping the CollisionObject3D in question.

**Enums:**
**DisableMode:** DISABLE_MODE_REMOVE=0, DISABLE_MODE_MAKE_STATIC=1, DISABLE_MODE_KEEP_ACTIVE=2
  - DISABLE_MODE_REMOVE: When `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`, remove from the physics simulation to stop all physics interactions with this CollisionObject3D. Automatically re-added to the physics simulation when the Node is processed again.
  - DISABLE_MODE_MAKE_STATIC: When `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`, make the body static. Doesn't affect Area3D. PhysicsBody3D can't be affected by forces or other bodies while static. Automatically set PhysicsBody3D back to its original mode when the Node is processed again.
  - DISABLE_MODE_KEEP_ACTIVE: When `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`, do not affect the physics simulation.

