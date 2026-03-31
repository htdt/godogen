## PhysicsDirectBodyState3DExtension <- PhysicsDirectBodyState3D

This class extends PhysicsDirectBodyState3D by providing additional virtual methods that can be overridden. When these methods are overridden, they will be called instead of the internal methods of the physics server. Intended for use with GDExtension to create custom implementations of PhysicsDirectBodyState3D.

**Methods:**
- _add_constant_central_force(force: Vector3)
- _add_constant_force(force: Vector3, position: Vector3)
- _add_constant_torque(torque: Vector3)
- _apply_central_force(force: Vector3)
- _apply_central_impulse(impulse: Vector3)
- _apply_force(force: Vector3, position: Vector3)
- _apply_impulse(impulse: Vector3, position: Vector3)
- _apply_torque(torque: Vector3)
- _apply_torque_impulse(impulse: Vector3)
- _get_angular_velocity() -> Vector3
- _get_center_of_mass() -> Vector3
- _get_center_of_mass_local() -> Vector3
- _get_collision_layer() -> int
- _get_collision_mask() -> int
- _get_constant_force() -> Vector3
- _get_constant_torque() -> Vector3
- _get_contact_collider(contact_idx: int) -> RID
- _get_contact_collider_id(contact_idx: int) -> int
- _get_contact_collider_object(contact_idx: int) -> Object
- _get_contact_collider_position(contact_idx: int) -> Vector3
- _get_contact_collider_shape(contact_idx: int) -> int
- _get_contact_collider_velocity_at_position(contact_idx: int) -> Vector3
- _get_contact_count() -> int
- _get_contact_impulse(contact_idx: int) -> Vector3
- _get_contact_local_normal(contact_idx: int) -> Vector3
- _get_contact_local_position(contact_idx: int) -> Vector3
- _get_contact_local_shape(contact_idx: int) -> int
- _get_contact_local_velocity_at_position(contact_idx: int) -> Vector3
- _get_inverse_inertia() -> Vector3
- _get_inverse_inertia_tensor() -> Basis
- _get_inverse_mass() -> float
- _get_linear_velocity() -> Vector3
- _get_principal_inertia_axes() -> Basis
- _get_space_state() -> PhysicsDirectSpaceState3D
- _get_step() -> float
- _get_total_angular_damp() -> float
- _get_total_gravity() -> Vector3
- _get_total_linear_damp() -> float
- _get_transform() -> Transform3D
- _get_velocity_at_local_position(local_position: Vector3) -> Vector3
- _integrate_forces()
- _is_sleeping() -> bool
- _set_angular_velocity(velocity: Vector3)
- _set_collision_layer(layer: int)
- _set_collision_mask(mask: int)
- _set_constant_force(force: Vector3)
- _set_constant_torque(torque: Vector3)
- _set_linear_velocity(velocity: Vector3)
- _set_sleep_state(enabled: bool)
- _set_transform(transform: Transform3D)

