## SkeletonModification2DTwoBoneIK <- SkeletonModification2D

This SkeletonModification2D uses an algorithm typically called TwoBoneIK. This algorithm works by leveraging the law of cosines and the lengths of the bones to figure out what rotation the bones currently have, and what rotation they need to make a complete triangle, where the first bone, the second bone, and the target form the three vertices of the triangle. Because the algorithm works by making a triangle, it can only operate on two bones. TwoBoneIK is great for arms, legs, and really any joints that can be represented by just two bones that bend to reach a target. This solver is more lightweight than SkeletonModification2DFABRIK, but gives similar, natural looking results.

**Props:**
- flip_bend_direction: bool = false
- target_maximum_distance: float = 0.0
- target_minimum_distance: float = 0.0
- target_nodepath: NodePath = NodePath("")

- **flip_bend_direction**: If `true`, the bones in the modification will bend outward as opposed to inwards when contracting. If `false`, the bones will bend inwards when contracting.
- **target_maximum_distance**: The maximum distance the target can be at. If the target is farther than this distance, the modification will solve as if it's at this maximum distance. When set to `0`, the modification will solve without distance constraints.
- **target_minimum_distance**: The minimum distance the target can be at. If the target is closer than this distance, the modification will solve as if it's at this minimum distance. When set to `0`, the modification will solve without distance constraints.
- **target_nodepath**: The NodePath to the node that is the target for the TwoBoneIK modification. This node is what the modification will use when bending the Bone2D nodes.

**Methods:**
- get_joint_one_bone2d_node() -> NodePath - Returns the Bone2D node that is being used as the first bone in the TwoBoneIK modification.
- get_joint_one_bone_idx() -> int - Returns the index of the Bone2D node that is being used as the first bone in the TwoBoneIK modification.
- get_joint_two_bone2d_node() -> NodePath - Returns the Bone2D node that is being used as the second bone in the TwoBoneIK modification.
- get_joint_two_bone_idx() -> int - Returns the index of the Bone2D node that is being used as the second bone in the TwoBoneIK modification.
- set_joint_one_bone2d_node(bone2d_node: NodePath) - Sets the Bone2D node that is being used as the first bone in the TwoBoneIK modification.
- set_joint_one_bone_idx(bone_idx: int) - Sets the index of the Bone2D node that is being used as the first bone in the TwoBoneIK modification.
- set_joint_two_bone2d_node(bone2d_node: NodePath) - Sets the Bone2D node that is being used as the second bone in the TwoBoneIK modification.
- set_joint_two_bone_idx(bone_idx: int) - Sets the index of the Bone2D node that is being used as the second bone in the TwoBoneIK modification.

