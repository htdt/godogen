## DampedSpringJoint2D <- Joint2D

A physics joint that connects two 2D physics bodies with a spring-like force. This behaves like a spring that always wants to stretch to a given length.

**Props:**
- damping: float = 1.0
- length: float = 50.0
- rest_length: float = 0.0
- stiffness: float = 20.0

- **damping**: The spring joint's damping ratio. A value between `0` and `1`. When the two bodies move into different directions the system tries to align them to the spring axis again. A high `damping` value forces the attached bodies to align faster.
- **length**: The spring joint's maximum length. The two attached bodies cannot stretch it past this value.
- **rest_length**: When the bodies attached to the spring joint move they stretch or squash it. The joint always tries to resize towards this length.
- **stiffness**: The higher the value, the less the bodies attached to the joint will deform it. The joint applies an opposing force to the bodies, the product of the stiffness multiplied by the size difference from its resting length.

