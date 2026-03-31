## Joint2D <- Node2D

Abstract base class for all joints in 2D physics. 2D joints bind together two physics bodies (`node_a` and `node_b`) and apply a constraint.

**Props:**
- bias: float = 0.0
- disable_collision: bool = true
- node_a: NodePath = NodePath("")
- node_b: NodePath = NodePath("")

- **bias**: When `node_a` and `node_b` move in different directions the `bias` controls how fast the joint pulls them back to their original position. The lower the `bias` the more the two bodies can pull on the joint. When set to `0`, the default value from `ProjectSettings.physics/2d/solver/default_constraint_bias` is used.
- **disable_collision**: If `true`, the two bodies bound together do not collide with each other.
- **node_a**: Path to the first body (A) attached to the joint. The node must inherit PhysicsBody2D.
- **node_b**: Path to the second body (B) attached to the joint. The node must inherit PhysicsBody2D.

**Methods:**
- get_rid() -> RID - Returns the joint's internal RID from the PhysicsServer2D.

