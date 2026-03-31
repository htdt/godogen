## Joint3D <- Node3D

Abstract base class for all joints in 3D physics. 3D joints bind together two physics bodies (`node_a` and `node_b`) and apply a constraint. If only one body is defined, it is attached to a fixed StaticBody3D without collision shapes.

**Props:**
- exclude_nodes_from_collision: bool = true
- node_a: NodePath = NodePath("")
- node_b: NodePath = NodePath("")
- solver_priority: int = 1

- **exclude_nodes_from_collision**: If `true`, the two bodies bound together do not collide with each other.
- **node_a**: Path to the first node (A) attached to the joint. The node must inherit PhysicsBody3D. If left empty and `node_b` is set, the body is attached to a fixed StaticBody3D without collision shapes.
- **node_b**: Path to the second node (B) attached to the joint. The node must inherit PhysicsBody3D. If left empty and `node_a` is set, the body is attached to a fixed StaticBody3D without collision shapes.
- **solver_priority**: The priority used to define which solver is executed first for multiple joints. The lower the value, the higher the priority. **Note:** Only supported when using GodotPhysics3D. This property is ignored when using Jolt Physics.

**Methods:**
- get_rid() -> RID - Returns the joint's internal RID from the PhysicsServer3D.

