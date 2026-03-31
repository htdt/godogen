## SkeletonModification2DCCDIK <- SkeletonModification2D

This SkeletonModification2D uses an algorithm called Cyclic Coordinate Descent Inverse Kinematics, or CCDIK, to manipulate a chain of bones in a Skeleton2D so it reaches a defined target. CCDIK works by rotating a set of bones, typically called a "bone chain", on a single axis. Each bone is rotated to face the target from the tip (by default), which over a chain of bones allow it to rotate properly to reach the target. Because the bones only rotate on a single axis, CCDIK *can* look more robotic than other IK solvers. **Note:** The CCDIK modifier has `ccdik_joints`, which are the data objects that hold the data for each joint in the CCDIK chain. This is different from a bone! CCDIK joints hold the data needed for each bone in the bone chain used by CCDIK. CCDIK also fully supports angle constraints, allowing for more control over how a solution is met.

**Props:**
- ccdik_data_chain_length: int = 0
- target_nodepath: NodePath = NodePath("")
- tip_nodepath: NodePath = NodePath("")

- **ccdik_data_chain_length**: The number of CCDIK joints in the CCDIK modification.
- **target_nodepath**: The NodePath to the node that is the target for the CCDIK modification. This node is what the CCDIK chain will attempt to rotate the bone chain to.
- **tip_nodepath**: The end position of the CCDIK chain. Typically, this should be a child of a Bone2D node attached to the final Bone2D in the CCDIK chain.

**Methods:**
- get_ccdik_joint_bone2d_node(joint_idx: int) -> NodePath - Returns the Bone2D node assigned to the CCDIK joint at `joint_idx`.
- get_ccdik_joint_bone_index(joint_idx: int) -> int - Returns the index of the Bone2D node assigned to the CCDIK joint at `joint_idx`.
- get_ccdik_joint_constraint_angle_invert(joint_idx: int) -> bool - Returns whether the CCDIK joint at `joint_idx` uses an inverted joint constraint. See `set_ccdik_joint_constraint_angle_invert` for details.
- get_ccdik_joint_constraint_angle_max(joint_idx: int) -> float - Returns the maximum angle constraint for the joint at `joint_idx`.
- get_ccdik_joint_constraint_angle_min(joint_idx: int) -> float - Returns the minimum angle constraint for the joint at `joint_idx`.
- get_ccdik_joint_enable_constraint(joint_idx: int) -> bool - Returns whether angle constraints on the CCDIK joint at `joint_idx` are enabled.
- get_ccdik_joint_rotate_from_joint(joint_idx: int) -> bool - Returns whether the joint at `joint_idx` is set to rotate from the joint, `true`, or to rotate from the tip, `false`. The default is to rotate from the tip.
- set_ccdik_joint_bone2d_node(joint_idx: int, bone2d_nodepath: NodePath) - Sets the Bone2D node assigned to the CCDIK joint at `joint_idx`.
- set_ccdik_joint_bone_index(joint_idx: int, bone_idx: int) - Sets the bone index, `bone_idx`, of the CCDIK joint at `joint_idx`. When possible, this will also update the `bone2d_node` of the CCDIK joint based on data provided by the linked skeleton.
- set_ccdik_joint_constraint_angle_invert(joint_idx: int, invert: bool) - Sets whether the CCDIK joint at `joint_idx` uses an inverted joint constraint. An inverted joint constraint only constraints the CCDIK joint to the angles *outside of* the inputted minimum and maximum angles. For this reason, it is referred to as an inverted joint constraint, as it constraints the joint to the outside of the inputted values.
- set_ccdik_joint_constraint_angle_max(joint_idx: int, angle_max: float) - Sets the maximum angle constraint for the joint at `joint_idx`.
- set_ccdik_joint_constraint_angle_min(joint_idx: int, angle_min: float) - Sets the minimum angle constraint for the joint at `joint_idx`.
- set_ccdik_joint_enable_constraint(joint_idx: int, enable_constraint: bool) - Determines whether angle constraints on the CCDIK joint at `joint_idx` are enabled. When `true`, constraints will be enabled and taken into account when solving.
- set_ccdik_joint_rotate_from_joint(joint_idx: int, rotate_from_joint: bool) - Sets whether the joint at `joint_idx` is set to rotate from the joint, `true`, or to rotate from the tip, `false`.

