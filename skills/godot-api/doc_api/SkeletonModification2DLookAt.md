## SkeletonModification2DLookAt <- SkeletonModification2D

This SkeletonModification2D rotates a bone to look a target. This is extremely helpful for moving character's head to look at the player, rotating a turret to look at a target, or any other case where you want to make a bone rotate towards something quickly and easily.

**Props:**
- bone2d_node: NodePath = NodePath("")
- bone_index: int = -1
- target_nodepath: NodePath = NodePath("")

- **bone2d_node**: The Bone2D node that the modification will operate on.
- **bone_index**: The index of the Bone2D node that the modification will operate on.
- **target_nodepath**: The NodePath to the node that is the target for the LookAt modification. This node is what the modification will rotate the Bone2D to.

**Methods:**
- get_additional_rotation() -> float - Returns the amount of additional rotation that is applied after the LookAt modification executes.
- get_constraint_angle_invert() -> bool - Returns whether the constraints to this modification are inverted or not.
- get_constraint_angle_max() -> float - Returns the constraint's maximum allowed angle.
- get_constraint_angle_min() -> float - Returns the constraint's minimum allowed angle.
- get_enable_constraint() -> bool - Returns `true` if the LookAt modification is using constraints.
- set_additional_rotation(rotation: float) - Sets the amount of additional rotation that is to be applied after executing the modification. This allows for offsetting the results by the inputted rotation amount.
- set_constraint_angle_invert(invert: bool) - When `true`, the modification will use an inverted joint constraint. An inverted joint constraint only constraints the Bone2D to the angles *outside of* the inputted minimum and maximum angles. For this reason, it is referred to as an inverted joint constraint, as it constraints the joint to the outside of the inputted values.
- set_constraint_angle_max(angle_max: float) - Sets the constraint's maximum allowed angle.
- set_constraint_angle_min(angle_min: float) - Sets the constraint's minimum allowed angle.
- set_enable_constraint(enable_constraint: bool) - Sets whether this modification will use constraints or not. When `true`, constraints will be applied when solving the LookAt modification.

