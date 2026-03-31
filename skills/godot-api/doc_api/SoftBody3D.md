## SoftBody3D <- MeshInstance3D

A deformable 3D physics mesh. Used to create elastic or deformable objects such as cloth, rubber, or other flexible materials. Additionally, SoftBody3D is subject to wind forces defined in Area3D (see `Area3D.wind_source_path`, `Area3D.wind_force_magnitude`, and `Area3D.wind_attenuation_factor`). **Note:** It's recommended to use Jolt Physics when using SoftBody3D instead of the default GodotPhysics3D, as Jolt Physics' soft body implementation is faster and more reliable. You can switch the physics engine using the `ProjectSettings.physics/3d/physics_engine` project setting.

**Props:**
- collision_layer: int = 1
- collision_mask: int = 1
- damping_coefficient: float = 0.01
- disable_mode: int (SoftBody3D.DisableMode) = 0
- drag_coefficient: float = 0.0
- linear_stiffness: float = 0.5
- parent_collision_ignore: NodePath = NodePath("")
- pressure_coefficient: float = 0.0
- ray_pickable: bool = true
- shrinking_factor: float = 0.0
- simulation_precision: int = 5
- total_mass: float = 1.0

- **collision_layer**: The physics layers this SoftBody3D **is in**. Collision objects can exist in one or more of 32 different layers. See also `collision_mask`. **Note:** Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See in the documentation for more information.
- **collision_mask**: The physics layers this SoftBody3D **scans**. Collision objects can scan one or more of 32 different layers. See also `collision_layer`. **Note:** Object A can detect a contact with object B only if object B is in any of the layers that object A scans. See in the documentation for more information.
- **damping_coefficient**: The body's damping coefficient. Higher values will slow down the body more noticeably when forces are applied.
- **disable_mode**: Defines the behavior in physics when `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`.
- **drag_coefficient**: The body's drag coefficient. Higher values increase this body's air resistance. **Note:** This value is currently unused by Godot's default physics implementation.
- **linear_stiffness**: Higher values will result in a stiffer body, while lower values will increase the body's ability to bend. The value can be between `0.0` and `1.0` (inclusive).
- **parent_collision_ignore**: NodePath to a CollisionObject3D this SoftBody3D should avoid clipping.
- **pressure_coefficient**: The pressure coefficient of this soft body. Simulate pressure build-up from inside this body. Higher values increase the strength of this effect.
- **ray_pickable**: If `true`, the SoftBody3D will respond to RayCast3Ds.
- **shrinking_factor**: Scales the rest lengths of SoftBody3D's edge constraints. Positive values shrink the mesh, while negative values expand it. For example, a value of `0.1` shortens the edges of the mesh by 10%, while `-0.1` expands the edges by 10%. **Note:** `shrinking_factor` is best used on surface meshes with pinned points.
- **simulation_precision**: Increasing this value will improve the resulting simulation, but can affect performance. Use with care.
- **total_mass**: The SoftBody3D's mass.

**Methods:**
- add_collision_exception_with(body: Node) - Adds a body to the list of bodies that this body can't collide with.
- apply_central_force(force: Vector3) - Distributes and applies a force to all points. A force is time dependent and meant to be applied every physics update.
- apply_central_impulse(impulse: Vector3) - Distributes and applies an impulse to all points. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_force" functions otherwise).
- apply_force(point_index: int, force: Vector3) - Applies a force to a point. A force is time dependent and meant to be applied every physics update.
- apply_impulse(point_index: int, impulse: Vector3) - Applies an impulse to a point. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_force" functions otherwise).
- get_collision_exceptions() -> PhysicsBody3D[] - Returns an array of nodes that were added as collision exceptions for this body.
- get_collision_layer_value(layer_number: int) -> bool - Returns whether or not the specified layer of the `collision_layer` is enabled, given a `layer_number` between 1 and 32.
- get_collision_mask_value(layer_number: int) -> bool - Returns whether or not the specified layer of the `collision_mask` is enabled, given a `layer_number` between 1 and 32.
- get_physics_rid() -> RID - Returns the internal RID used by the PhysicsServer3D for this body.
- get_point_transform(point_index: int) -> Vector3 - Returns local translation of a vertex in the surface array.
- is_point_pinned(point_index: int) -> bool - Returns `true` if vertex is set to pinned.
- remove_collision_exception_with(body: Node) - Removes a body from the list of bodies that this body can't collide with.
- set_collision_layer_value(layer_number: int, value: bool) - Based on `value`, enables or disables the specified layer in the `collision_layer`, given a `layer_number` between 1 and 32.
- set_collision_mask_value(layer_number: int, value: bool) - Based on `value`, enables or disables the specified layer in the `collision_mask`, given a `layer_number` between 1 and 32.
- set_point_pinned(point_index: int, pinned: bool, attachment_path: NodePath = NodePath(""), insert_at: int = -1) - Sets the pinned state of a surface vertex. When set to `true`, the optional `attachment_path` can define a Node3D the pinned vertex will be attached to.

**Enums:**
**DisableMode:** DISABLE_MODE_REMOVE=0, DISABLE_MODE_KEEP_ACTIVE=1
  - DISABLE_MODE_REMOVE: When `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`, remove from the physics simulation to stop all physics interactions with this SoftBody3D. Automatically re-added to the physics simulation when the Node is processed again.
  - DISABLE_MODE_KEEP_ACTIVE: When `Node.process_mode` is set to `Node.PROCESS_MODE_DISABLED`, do not affect the physics simulation.

