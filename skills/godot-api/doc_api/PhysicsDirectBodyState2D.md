## PhysicsDirectBodyState2D <- Object

Provides direct access to a physics body in the PhysicsServer2D, allowing safe changes to physics properties. This object is passed via the direct state callback of RigidBody2D, and is intended for changing the direct state of that body. See `RigidBody2D._integrate_forces`.

**Props:**
- angular_velocity: float
- center_of_mass: Vector2
- center_of_mass_local: Vector2
- collision_layer: int
- collision_mask: int
- inverse_inertia: float
- inverse_mass: float
- linear_velocity: Vector2
- sleeping: bool
- step: float
- total_angular_damp: float
- total_gravity: Vector2
- total_linear_damp: float
- transform: Transform2D

- **angular_velocity**: The body's rotational velocity in *radians* per second.
- **center_of_mass**: The body's center of mass position relative to the body's center in the global coordinate system.
- **center_of_mass_local**: The body's center of mass position in the body's local coordinate system.
- **collision_layer**: The body's collision layer.
- **collision_mask**: The body's collision mask.
- **inverse_inertia**: The inverse of the inertia of the body.
- **inverse_mass**: The inverse of the mass of the body.
- **linear_velocity**: The body's linear velocity in pixels per second.
- **sleeping**: If `true`, this body is currently sleeping (not active).
- **step**: The timestep (delta) used for the simulation.
- **total_angular_damp**: The rate at which the body stops rotating, if there are not any other forces moving it.
- **total_gravity**: The total gravity vector being currently applied to this body.
- **total_linear_damp**: The rate at which the body stops moving, if there are not any other forces moving it.
- **transform**: The body's transformation matrix.

**Methods:**
- add_constant_central_force(force: Vector2 = Vector2(0, 0)) - Adds a constant directional force without affecting rotation that keeps being applied over time until cleared with `constant_force = Vector2(0, 0)`. This is equivalent to using `add_constant_force` at the body's center of mass.
- add_constant_force(force: Vector2, position: Vector2 = Vector2(0, 0)) - Adds a constant positioned force to the body that keeps being applied over time until cleared with `constant_force = Vector2(0, 0)`. `position` is the offset from the body origin in global coordinates.
- add_constant_torque(torque: float) - Adds a constant rotational force without affecting position that keeps being applied over time until cleared with `constant_torque = 0`.
- apply_central_force(force: Vector2 = Vector2(0, 0)) - Applies a directional force without affecting rotation. A force is time dependent and meant to be applied every physics update. This is equivalent to using `apply_force` at the body's center of mass.
- apply_central_impulse(impulse: Vector2) - Applies a directional impulse without affecting rotation. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_force" functions otherwise). This is equivalent to using `apply_impulse` at the body's center of mass.
- apply_force(force: Vector2, position: Vector2 = Vector2(0, 0)) - Applies a positioned force to the body. A force is time dependent and meant to be applied every physics update. `position` is the offset from the body origin in global coordinates.
- apply_impulse(impulse: Vector2, position: Vector2 = Vector2(0, 0)) - Applies a positioned impulse to the body. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_force" functions otherwise). `position` is the offset from the body origin in global coordinates.
- apply_torque(torque: float) - Applies a rotational force without affecting position. A force is time dependent and meant to be applied every physics update. **Note:** `inverse_inertia` is required for this to work. To have `inverse_inertia`, an active CollisionShape2D must be a child of the node, or you can manually set `inverse_inertia`.
- apply_torque_impulse(impulse: float) - Applies a rotational impulse to the body without affecting the position. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_force" functions otherwise). **Note:** `inverse_inertia` is required for this to work. To have `inverse_inertia`, an active CollisionShape2D must be a child of the node, or you can manually set `inverse_inertia`.
- get_constant_force() -> Vector2 - Returns the body's total constant positional forces applied during each physics update. See `add_constant_force` and `add_constant_central_force`.
- get_constant_torque() -> float - Returns the body's total constant rotational forces applied during each physics update. See `add_constant_torque`.
- get_contact_collider(contact_idx: int) -> RID - Returns the collider's RID.
- get_contact_collider_id(contact_idx: int) -> int - Returns the collider's object id.
- get_contact_collider_object(contact_idx: int) -> Object - Returns the collider object. This depends on how it was created (will return a scene node if such was used to create it).
- get_contact_collider_position(contact_idx: int) -> Vector2 - Returns the position of the contact point on the collider in the global coordinate system.
- get_contact_collider_shape(contact_idx: int) -> int - Returns the collider's shape index.
- get_contact_collider_velocity_at_position(contact_idx: int) -> Vector2 - Returns the velocity vector at the collider's contact point.
- get_contact_count() -> int - Returns the number of contacts this body has with other bodies. **Note:** By default, this returns 0 unless bodies are configured to monitor contacts. See `RigidBody2D.contact_monitor`.
- get_contact_impulse(contact_idx: int) -> Vector2 - Returns the impulse created by the contact.
- get_contact_local_normal(contact_idx: int) -> Vector2 - Returns the local normal at the contact point.
- get_contact_local_position(contact_idx: int) -> Vector2 - Returns the position of the contact point on the body in the global coordinate system.
- get_contact_local_shape(contact_idx: int) -> int - Returns the local shape index of the collision.
- get_contact_local_velocity_at_position(contact_idx: int) -> Vector2 - Returns the velocity vector at the body's contact point.
- get_space_state() -> PhysicsDirectSpaceState2D - Returns the current state of the space, useful for queries.
- get_velocity_at_local_position(local_position: Vector2) -> Vector2 - Returns the body's velocity at the given relative position. `local_position` is the offset from the body origin in global coordinates.
- integrate_forces() - Updates the body's linear and angular velocity by applying gravity and damping for the equivalent of one physics tick.
- set_constant_force(force: Vector2) - Sets the body's total constant positional forces applied during each physics update. See `add_constant_force` and `add_constant_central_force`.
- set_constant_torque(torque: float) - Sets the body's total constant rotational forces applied during each physics update. See `add_constant_torque`.

