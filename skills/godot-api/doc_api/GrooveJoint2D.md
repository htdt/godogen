## GrooveJoint2D <- Joint2D

A physics joint that restricts the movement of two 2D physics bodies to a fixed axis. For example, a StaticBody2D representing a piston base can be attached to a RigidBody2D representing the piston head, moving up and down.

**Props:**
- initial_offset: float = 25.0
- length: float = 50.0

- **initial_offset**: The body B's initial anchor position defined by the joint's origin and a local offset `initial_offset` along the joint's Y axis (along the groove).
- **length**: The groove's length. The groove is from the joint's origin towards `length` along the joint's local Y axis.

