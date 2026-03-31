## PhysicalBone3D <- PhysicsBody3D

The PhysicalBone3D node is a physics body that can be used to make bones in a Skeleton3D react to physics. **Note:** In order to detect physical bones with raycasts, the `SkeletonModifier3D.active` property of the parent PhysicalBoneSimulator3D must be `true` and the Skeleton3D's bone must be assigned to PhysicalBone3D correctly; it means that `get_bone_id` should return a valid id (`>= 0`).

**Props:**
- angular_damp: float = 0.0
- angular_damp_mode: int (PhysicalBone3D.DampMode) = 0
- angular_velocity: Vector3 = Vector3(0, 0, 0)
- body_offset: Transform3D = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)
- bounce: float = 0.0
- can_sleep: bool = true
- custom_integrator: bool = false
- friction: float = 1.0
- gravity_scale: float = 1.0
- joint_offset: Transform3D = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)
- joint_rotation: Vector3 = Vector3(0, 0, 0)
- joint_type: int (PhysicalBone3D.JointType) = 0
- linear_damp: float = 0.0
- linear_damp_mode: int (PhysicalBone3D.DampMode) = 0
- linear_velocity: Vector3 = Vector3(0, 0, 0)
- mass: float = 1.0

- **angular_damp**: Damps the body's rotation. By default, the body will use the `ProjectSettings.physics/3d/default_angular_damp` project setting or any value override set by an Area3D the body is in. Depending on `angular_damp_mode`, you can set `angular_damp` to be added to or to replace the body's damping value. See `ProjectSettings.physics/3d/default_angular_damp` for more details about damping.
- **angular_damp_mode**: Defines how `angular_damp` is applied.
- **angular_velocity**: The PhysicalBone3D's rotational velocity in *radians* per second.
- **body_offset**: Sets the body's transform.
- **bounce**: The body's bounciness. Values range from `0` (no bounce) to `1` (full bounciness). **Note:** Even with `bounce` set to `1.0`, some energy will be lost over time due to linear and angular damping. To have a PhysicalBone3D that preserves all its energy over time, set `bounce` to `1.0`, `linear_damp_mode` to `DAMP_MODE_REPLACE`, `linear_damp` to `0.0`, `angular_damp_mode` to `DAMP_MODE_REPLACE`, and `angular_damp` to `0.0`.
- **can_sleep**: If `true`, the body is deactivated when there is no movement, so it will not take part in the simulation until it is awakened by an external force.
- **custom_integrator**: If `true`, the standard force integration (like gravity or damping) will be disabled for this body. Other than collision response, the body will only move as determined by the `_integrate_forces` method, if that virtual method is overridden. Setting this property will call the method `PhysicsServer3D.body_set_omit_force_integration` internally.
- **friction**: The body's friction, from `0` (frictionless) to `1` (max friction).
- **gravity_scale**: This is multiplied by `ProjectSettings.physics/3d/default_gravity` to produce this body's gravity. For example, a value of `1.0` will apply normal gravity, `2.0` will apply double the gravity, and `0.5` will apply half the gravity to this body.
- **joint_offset**: Sets the joint's transform.
- **joint_rotation**: Sets the joint's rotation in radians.
- **joint_type**: Sets the joint type.
- **linear_damp**: Damps the body's movement. By default, the body will use `ProjectSettings.physics/3d/default_linear_damp` or any value override set by an Area3D the body is in. Depending on `linear_damp_mode`, `linear_damp` may be added to or replace the body's damping value. See `ProjectSettings.physics/3d/default_linear_damp` for more details about damping.
- **linear_damp_mode**: Defines how `linear_damp` is applied.
- **linear_velocity**: The body's linear velocity in units per second. Can be used sporadically, but **don't set this every frame**, because physics may run in another thread and runs at a different granularity. Use `_integrate_forces` as your process loop for precise control of the body state.
- **mass**: The body's mass.

**Methods:**
- _integrate_forces(state: PhysicsDirectBodyState3D) - Called during physics processing, allowing you to read and safely modify the simulation state for the object. By default, it is called before the standard force integration, but the `custom_integrator` property allows you to disable the standard force integration and do fully custom force integration for a body.
- apply_central_impulse(impulse: Vector3) - Applies a directional impulse without affecting rotation. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_integrate_forces" functions otherwise). This is equivalent to using `apply_impulse` at the body's center of mass.
- apply_impulse(impulse: Vector3, position: Vector3 = Vector3(0, 0, 0)) - Applies a positioned impulse to the PhysicsBone3D. An impulse is time-independent! Applying an impulse every frame would result in a framerate-dependent force. For this reason, it should only be used when simulating one-time impacts (use the "_integrate_forces" functions otherwise). `position` is the offset from the PhysicsBone3D origin in global coordinates.
- get_bone_id() -> int - Returns the unique identifier of the PhysicsBone3D.
- get_simulate_physics() -> bool - Returns `true` if the PhysicsBone3D is allowed to simulate physics.
- is_simulating_physics() -> bool - Returns `true` if the PhysicsBone3D is currently simulating physics.

**Enums:**
**DampMode:** DAMP_MODE_COMBINE=0, DAMP_MODE_REPLACE=1
  - DAMP_MODE_COMBINE: In this mode, the body's damping value is added to any value set in areas or the default value.
  - DAMP_MODE_REPLACE: In this mode, the body's damping value replaces any value set in areas or the default value.
**JointType:** JOINT_TYPE_NONE=0, JOINT_TYPE_PIN=1, JOINT_TYPE_CONE=2, JOINT_TYPE_HINGE=3, JOINT_TYPE_SLIDER=4, JOINT_TYPE_6DOF=5
  - JOINT_TYPE_NONE: No joint is applied to the PhysicsBone3D.
  - JOINT_TYPE_PIN: A pin joint is applied to the PhysicsBone3D.
  - JOINT_TYPE_CONE: A cone joint is applied to the PhysicsBone3D.
  - JOINT_TYPE_HINGE: A hinge joint is applied to the PhysicsBone3D.
  - JOINT_TYPE_SLIDER: A slider joint is applied to the PhysicsBone3D.
  - JOINT_TYPE_6DOF: A 6 degrees of freedom joint is applied to the PhysicsBone3D.

