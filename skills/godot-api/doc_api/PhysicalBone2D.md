## PhysicalBone2D <- RigidBody2D

The PhysicalBone2D node is a RigidBody2D-based node that can be used to make Bone2Ds in a Skeleton2D react to physics. **Note:** To make the Bone2Ds visually follow the PhysicalBone2D node, use a SkeletonModification2DPhysicalBones modification on the Skeleton2D parent. **Note:** The PhysicalBone2D node does not automatically create a Joint2D node to keep PhysicalBone2D nodes together. They must be created manually. For most cases, you want to use a PinJoint2D node. The PhysicalBone2D node will automatically configure the Joint2D node once it's been added as a child node.

**Props:**
- auto_configure_joint: bool = true
- bone2d_index: int = -1
- bone2d_nodepath: NodePath = NodePath("")
- follow_bone_when_simulating: bool = false
- simulate_physics: bool = false

- **auto_configure_joint**: If `true`, the PhysicalBone2D will automatically configure the first Joint2D child node. The automatic configuration is limited to setting up the node properties and positioning the Joint2D.
- **bone2d_index**: The index of the Bone2D that this PhysicalBone2D should simulate.
- **bone2d_nodepath**: The NodePath to the Bone2D that this PhysicalBone2D should simulate.
- **follow_bone_when_simulating**: If `true`, the PhysicalBone2D will keep the transform of the bone it is bound to when simulating physics.
- **simulate_physics**: If `true`, the PhysicalBone2D will start simulating using physics. If `false`, the PhysicalBone2D will follow the transform of the Bone2D node. **Note:** To have the Bone2Ds visually follow the PhysicalBone2D, use a SkeletonModification2DPhysicalBones modification on the Skeleton2D node with the Bone2D nodes.

**Methods:**
- get_joint() -> Joint2D - Returns the first Joint2D child node, if one exists. This is mainly a helper function to make it easier to get the Joint2D that the PhysicalBone2D is autoconfiguring.
- is_simulating_physics() -> bool - Returns a boolean that indicates whether the PhysicalBone2D is running and simulating using the Godot 2D physics engine. When `true`, the PhysicalBone2D node is using physics.

