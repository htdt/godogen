## ConeTwistJoint3D <- Joint3D

A physics joint that connects two 3D physics bodies in a way that simulates a ball-and-socket joint. The twist axis is initiated as the X axis of the ConeTwistJoint3D. Once the physics bodies swing, the twist axis is calculated as the middle of the X axes of the joint in the local space of the two physics bodies. Useful for limbs like shoulders and hips, lamps hanging off a ceiling, etc.

**Props:**
- bias: float = 0.3
- relaxation: float = 1.0
- softness: float = 0.8
- swing_span: float = 0.7853982
- twist_span: float = 3.1415927

- **bias**: The speed with which the swing or twist will take place. The higher, the faster.
- **relaxation**: Defines, how fast the swing- and twist-speed-difference on both sides gets synced.
- **softness**: The ease with which the joint starts to twist. If it's too low, it takes more force to start twisting the joint.
- **swing_span**: Swing is rotation from side to side, around the axis perpendicular to the twist axis. The swing span defines, how much rotation will not get corrected along the swing axis. Could be defined as looseness in the ConeTwistJoint3D. If below 0.05, this behavior is locked.
- **twist_span**: Twist is the rotation around the twist axis, this value defined how far the joint can twist. Twist is locked if below 0.05.

**Methods:**
- get_param(param: int) -> float - Returns the value of the specified parameter.
- set_param(param: int, value: float) - Sets the value of the specified parameter.

**Enums:**
**Param:** PARAM_SWING_SPAN=0, PARAM_TWIST_SPAN=1, PARAM_BIAS=2, PARAM_SOFTNESS=3, PARAM_RELAXATION=4, PARAM_MAX=5
  - PARAM_SWING_SPAN: Swing is rotation from side to side, around the axis perpendicular to the twist axis. The swing span defines, how much rotation will not get corrected along the swing axis. Could be defined as looseness in the ConeTwistJoint3D. If below 0.05, this behavior is locked.
  - PARAM_TWIST_SPAN: Twist is the rotation around the twist axis, this value defined how far the joint can twist. Twist is locked if below 0.05.
  - PARAM_BIAS: The speed with which the swing or twist will take place. The higher, the faster.
  - PARAM_SOFTNESS: The ease with which the joint starts to twist. If it's too low, it takes more force to start twisting the joint.
  - PARAM_RELAXATION: Defines, how fast the swing- and twist-speed-difference on both sides gets synced.
  - PARAM_MAX: Represents the size of the `Param` enum.

