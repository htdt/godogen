## PinJoint3D <- Joint3D

A physics joint that attaches two 3D physics bodies at a single point, allowing them to freely rotate. For example, a RigidBody3D can be attached to a StaticBody3D to create a pendulum or a seesaw.

**Props:**
- params/bias: float = 0.3
- params/damping: float = 1.0
- params/impulse_clamp: float = 0.0

- **params/bias**: The force with which the pinned objects stay in positional relation to each other. The higher, the stronger.
- **params/damping**: The force with which the pinned objects stay in velocity relation to each other. The higher, the stronger.
- **params/impulse_clamp**: If above 0, this value is the maximum value for an impulse that this Joint3D produces.

**Methods:**
- get_param(param: int) -> float - Returns the value of the specified parameter.
- set_param(param: int, value: float) - Sets the value of the specified parameter.

**Enums:**
**Param:** PARAM_BIAS=0, PARAM_DAMPING=1, PARAM_IMPULSE_CLAMP=2
  - PARAM_BIAS: The force with which the pinned objects stay in positional relation to each other. The higher, the stronger.
  - PARAM_DAMPING: The force with which the pinned objects stay in velocity relation to each other. The higher, the stronger.
  - PARAM_IMPULSE_CLAMP: If above 0, this value is the maximum value for an impulse that this Joint3D produces.

