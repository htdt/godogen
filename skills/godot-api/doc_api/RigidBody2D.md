## RigidBody2D <- PhysicsBody2D

RigidBody2D implements full 2D physics. It cannot be controlled directly, instead, you must apply forces to it (gravity, impulses, etc.), and the physics simulation will calculate the resulting movement, rotation, react to collisions, and affect other physics bodies in its path. The body's behavior can be adjusted via `lock_rotation`, `freeze`, and `freeze_mode`. By changing various properties of the object, such as `mass`, you can control how the physics simulation acts on it. A rigid body will always maintain its shape and size, even when forces are applied to it. It is useful for objects that can be interacted with in an environment, such as a tree that can be knocked over or a stack of crates that can be pushed around. If you need to directly affect the body, prefer `_integrate_forces` as it allows you to directly access the physics state. If you need to override the default physics behavior, you can write a custom force integration function. See `custom_integrator`. **Note:** Changing the 2D transform or `linear_velocity` of a RigidBody2D very often may lead to some unpredictable behaviors. This also happens when a RigidBody2D is the descendant of a constantly moving node, like another RigidBody2D, as that will cause its global transform to be set whenever its ancestor moves.

**Props:**
- angular_damp: float = 0.0
- angular_damp_mode: int (RigidBody2D.DampMode) = 0
- angular_velocity: float = 0.0
- can_sleep: bool = true
- center_of_mass: Vector2 = Vector2(0, 0)
- center_of_mass_mode: int (RigidBody2D.CenterOfMassMode) = 0
- constant_force: Vector2 = Vector2(0, 0)
- constant_torque: float = 0.0
- contact_monitor: bool = false
- continuous_cd: int (RigidBody2D.CCDMode) = 0
- custom_integrator: bool = false
- freeze: bool = false
- freeze_mode: int (RigidBody2D.FreezeMode) = 0
- gravity_scale: float = 1.0
- inertia: float = 0.0
- linear_damp: float = 0.0
- linear_damp_mode: int (RigidBody2D.DampMode) = 0
- linear_velocity: Vector2 = Vector2(0, 0)
- lock_rotation: bool = false
- mass: float = 1.0
- max_contacts_reported: int = 0
- physics_material_override: PhysicsMaterial
- sleeping: bool = false

- **angular_damp**: Damps the body's rotation. By default, the body will use the `ProjectSettings.physics/2d/default_angular_damp` setting or any value override set by an Area2D the body is in. Depending on `angular_damp_mode`, you can set `angular_damp` to be added to or to replace the body's damping value. See `ProjectSettings.physics/2d/default_angular_damp` for more details about damping.
- **angular_damp_mode**: Defines how `angular_damp` is applied.
- **angular_velocity**: The body's rotational velocity in *radians* per second.
- **can_sleep**: If `true`, the body can enter sleep mode when there is no movement. See `sleeping`.
- **center_of_mass**: The body's custom center of mass, relative to the body's origin position, when `center_of_mass_mode` is set to `CENTER_OF_MASS_MODE_CUSTOM`. This is the balanced point of the body, where applied forces only cause linear acceleration. Applying forces outside of the center of mass causes angular acceleration. When `center_of_mass_mode` is set to `CENTER_OF_MASS_MODE_AUTO` (default value), the center of mass is automatically determined, but this does not update the value of `center_of_mass`.
- **center_of_mass_mode**: Defines the way the body's center of mass is set.
- **constant_force**: The body's total constant positional forces applied during each physics update. See `add_constant_force` and `add_constant_central_force`.
- **constant_torque**: The body's total constant rotational forces applied during each physics update. See `add_constant_torque`.
- **contact_monitor**: If `true`, the RigidBody2D will emit signals when it collides with another body. **Note:** By default the maximum contacts reported is set to 0, meaning nothing will be recorded, see `max_contacts_reported`.
- **continuous_cd**: Continuous collision detection mode. Continuous collision detection tries to predict where a moving body will collide instead of moving it and correcting its movement after collision. Continuous collision detection is slower, but more precise and misses fewer collisions with small, fast-moving objects. Raycasting and shapecasting methods are available.
- **custom_integrator**: If `true`, the standard force integration (like gravity or damping) will be disabled for this body. Other than collision response, the body will only move as determined by the `_integrate_forces` method, if that virtual method is overridden. Setting this property will call the method `PhysicsServer2D.body_set_omit_force_integration` internally.
- **freeze**: If `true`, the body is frozen. Gravity and forces are not applied anymore. See `freeze_mode` to set the body's behavior when frozen. **Note:** For a body that is always frozen, use StaticBody2D or AnimatableBody2D instead.
- **freeze_mode**: The body's freeze mode. Determines the body's behavior when `freeze` is `true`. **Note:** For a body that is always frozen, use StaticBody2D or AnimatableBody2D instead.
- **gravity_scale**: Multiplies the gravity applied to the body. The body's gravity is calculated from the `ProjectSettings.physics/2d/default_gravity` project setting and/or any additional gravity vector applied by Area2Ds.
- **inertia**: The body's moment of inertia. This is like mass, but for rotation: it determines how much torque it takes to rotate the body. The moment of inertia is usually computed automatically from the mass and the shapes, but this property allows you to set a custom value. If set to `0`, inertia is automatically computed (default value). **Note:** This value does not change when inertia is automatically computed. Use PhysicsServer2D to get the computed inertia.
- **linear_damp**: Damps the body's movement. By default, the body will use the `ProjectSettings.physics/2d/default_linear_damp` setting or any value override set by an Area2D the body is in. Depending on `linear_damp_mode`, you can set `linear_damp` to be added to or to replace the body's damping value. See `ProjectSettings.physics/2d/default_linear_damp` for more details about damping.
- **linear_damp_mode**: Defines how `linear_damp` is applied.
- **linear_velocity**: The body's linear velocity in pixels per second. Can be used sporadically, but **don't set this every frame**, because physics may run in another thread and runs at a different granularity. Use `_integrate_forces` as your process loop for precise control of the body state.
- **lock_rotation**: If `true`, the body cannot rotate. Gravity and forces only apply linear movement.
- **mass**: The body's mass.
- **max_contacts_reported**: The maximum number of contacts that will be recorded. Requires a value greater than 0 and `contact_monitor` to be set to `true` to start to register contacts. Use `get_contact_count` to retrieve the count or `get_colliding_bodies` to retrieve bodies that have been collided with. **Note:** The number of contacts is different from the number of collisions. Collisions between parallel edges will result in two contacts (one at each end), and collisions between parallel faces will result in four contacts (one at each corner).
- **physics_material_override**: The physics material override for the body. If a material is assigned to this property, it will be used instead of any other physics material, such as an inherited one.
- **sleeping**: If `true`, the body will not move and will not calculate forces until woken up by another body through, for example, a collision, or by using the `apply_impulse` or `apply_force` methods.

**Methods:**
- _integrate_forces(state: PhysicsDirectBodyState2D) - Called during physics processing, allowing you to read and safely modify the simulation state for the object. By default, it is called before the standard force integration, but the `custom_integrator` property allows you to disable the standard force integration and do fully custom force integration for a body.
- add_constant_central_force(force: Vector2) - Adds a constant directional force without affecting rotation that keeps being applied over time until cleared with `constant_force = Vector2(0, 0)`. This is equivalent to using `add_constant_force` at the body's center of mass.
- add_constant_force(force: Vector2, position: Vector2 = Vector2(0, 0)) - Adds a constant positioned force to the body that keeps being applied over time until cleared with `constant_force = Vector2(0, 0)`. `position` is the offset from the body origin in global coordinates.
- add_constant_torque(torque: float) - Adds a constant rotational force without affecting position that keeps being applied over time until cleared with `constant_torque = 0`.
- apply_central_force(force: Vector2) - Applies a directional force without affecting rotation. A force is time dependent and meant to be applied every physics update. This is equivalent to using `apply_force` at the body's center of mass.
- apply_central_impulse(impulse: Vector2 = Vector2(0, 0)) - Applies a directional impulse without affecting rotation. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_force" functions otherwise). This is equivalent to using `apply_impulse` at the body's center of mass.
- apply_force(force: Vector2, position: Vector2 = Vector2(0, 0)) - Applies a positioned force to the body. A force is time dependent and meant to be applied every physics update. `position` is the offset from the body origin in global coordinates.
- apply_impulse(impulse: Vector2, position: Vector2 = Vector2(0, 0)) - Applies a positioned impulse to the body. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_force" functions otherwise). `position` is the offset from the body origin in global coordinates.
- apply_torque(torque: float) - Applies a rotational force without affecting position. A force is time dependent and meant to be applied every physics update. **Note:** `inertia` is required for this to work. To have `inertia`, an active CollisionShape2D must be a child of the node, or you can manually set `inertia`.
- apply_torque_impulse(torque: float) - Applies a rotational impulse to the body without affecting the position. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_force" functions otherwise). **Note:** `inertia` is required for this to work. To have `inertia`, an active CollisionShape2D must be a child of the node, or you can manually set `inertia`.
- get_colliding_bodies() -> Node2D[] - Returns a list of the bodies colliding with this one. Requires `contact_monitor` to be set to `true` and `max_contacts_reported` to be set high enough to detect all the collisions. **Note:** The result of this test is not immediate after moving objects. For performance, list of collisions is updated once per frame and before the physics step. Consider using signals instead.
- get_contact_count() -> int - Returns the number of contacts this body has with other bodies. By default, this returns 0 unless bodies are configured to monitor contacts (see `contact_monitor`). **Note:** To retrieve the colliding bodies, use `get_colliding_bodies`.
- set_axis_velocity(axis_velocity: Vector2) - Sets the body's velocity on the given axis. The velocity in the given vector axis will be set as the given vector length. This is useful for jumping behavior.

**Signals:**
- body_entered(body: Node) - Emitted when a collision with another PhysicsBody2D or TileMap occurs. Requires `contact_monitor` to be set to `true` and `max_contacts_reported` to be set high enough to detect all the collisions. TileMaps are detected if the TileSet has Collision Shape2Ds. `body` the Node, if it exists in the tree, of the other PhysicsBody2D or TileMap.
- body_exited(body: Node) - Emitted when the collision with another PhysicsBody2D or TileMap ends. Requires `contact_monitor` to be set to `true` and `max_contacts_reported` to be set high enough to detect all the collisions. TileMaps are detected if the TileSet has Collision Shape2Ds. `body` the Node, if it exists in the tree, of the other PhysicsBody2D or TileMap.
- body_shape_entered(body_rid: RID, body: Node, body_shape_index: int, local_shape_index: int) - Emitted when one of this RigidBody2D's Shape2Ds collides with another PhysicsBody2D or TileMap's Shape2Ds. Requires `contact_monitor` to be set to `true` and `max_contacts_reported` to be set high enough to detect all the collisions. TileMaps are detected if the TileSet has Collision Shape2Ds. `body_rid` the RID of the other PhysicsBody2D or TileSet's CollisionObject2D used by the PhysicsServer2D. `body` the Node, if it exists in the tree, of the other PhysicsBody2D or TileMap. `body_shape_index` the index of the Shape2D of the other PhysicsBody2D or TileMap used by the PhysicsServer2D. Get the CollisionShape2D node with `body.shape_owner_get_owner(body.shape_find_owner(body_shape_index))`. `local_shape_index` the index of the Shape2D of this RigidBody2D used by the PhysicsServer2D. Get the CollisionShape2D node with `self.shape_owner_get_owner(self.shape_find_owner(local_shape_index))`.
- body_shape_exited(body_rid: RID, body: Node, body_shape_index: int, local_shape_index: int) - Emitted when the collision between one of this RigidBody2D's Shape2Ds and another PhysicsBody2D or TileMap's Shape2Ds ends. Requires `contact_monitor` to be set to `true` and `max_contacts_reported` to be set high enough to detect all the collisions. TileMaps are detected if the TileSet has Collision Shape2Ds. `body_rid` the RID of the other PhysicsBody2D or TileSet's CollisionObject2D used by the PhysicsServer2D. `body` the Node, if it exists in the tree, of the other PhysicsBody2D or TileMap. `body_shape_index` the index of the Shape2D of the other PhysicsBody2D or TileMap used by the PhysicsServer2D. Get the CollisionShape2D node with `body.shape_owner_get_owner(body.shape_find_owner(body_shape_index))`. `local_shape_index` the index of the Shape2D of this RigidBody2D used by the PhysicsServer2D. Get the CollisionShape2D node with `self.shape_owner_get_owner(self.shape_find_owner(local_shape_index))`.
- sleeping_state_changed - Emitted when the physics engine changes the body's sleeping state. **Note:** Changing the value `sleeping` will not trigger this signal. It is only emitted if the sleeping state is changed by the physics engine or `emit_signal("sleeping_state_changed")` is used.

**Enums:**
**FreezeMode:** FREEZE_MODE_STATIC=0, FREEZE_MODE_KINEMATIC=1
  - FREEZE_MODE_STATIC: Static body freeze mode (default). The body is not affected by gravity and forces. It can be only moved by user code and doesn't collide with other bodies along its path.
  - FREEZE_MODE_KINEMATIC: Kinematic body freeze mode. Similar to `FREEZE_MODE_STATIC`, but collides with other bodies along its path when moved. Useful for a frozen body that needs to be animated.
**CenterOfMassMode:** CENTER_OF_MASS_MODE_AUTO=0, CENTER_OF_MASS_MODE_CUSTOM=1
  - CENTER_OF_MASS_MODE_AUTO: In this mode, the body's center of mass is calculated automatically based on its shapes. This assumes that the shapes' origins are also their center of mass.
  - CENTER_OF_MASS_MODE_CUSTOM: In this mode, the body's center of mass is set through `center_of_mass`. Defaults to the body's origin position.
**DampMode:** DAMP_MODE_COMBINE=0, DAMP_MODE_REPLACE=1
  - DAMP_MODE_COMBINE: In this mode, the body's damping value is added to any value set in areas or the default value.
  - DAMP_MODE_REPLACE: In this mode, the body's damping value replaces any value set in areas or the default value.
**CCDMode:** CCD_MODE_DISABLED=0, CCD_MODE_CAST_RAY=1, CCD_MODE_CAST_SHAPE=2
  - CCD_MODE_DISABLED: Continuous collision detection disabled. This is the fastest way to detect body collisions, but can miss small, fast-moving objects.
  - CCD_MODE_CAST_RAY: Continuous collision detection enabled using raycasting. This is faster than shapecasting but less precise.
  - CCD_MODE_CAST_SHAPE: Continuous collision detection enabled using shapecasting. This is the slowest CCD method and the most precise.

