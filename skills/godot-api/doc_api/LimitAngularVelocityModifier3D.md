## LimitAngularVelocityModifier3D <- SkeletonModifier3D

This modifier limits bone rotation angular velocity by comparing poses between previous and current frame. You can add bone chains by specifying their root and end bones, then add the bones between them to a list. Modifier processes either that list or the bones excluding those in the list depending on the option `exclude`. **Note:** Most methods in this class take an `index` parameter. This parameter specifies which setting list entry to return if the IK has multiple entries (e.g. `settings/<index>/root_bone_name`).

**Props:**
- chain_count: int = 0
- exclude: bool = false
- joint_count: int = 0
- max_angular_velocity: float = 6.2831855

- **chain_count**: The number of chains.
- **exclude**: If `true`, the modifier processes bones not included in the bone list. If `false`, the bones processed by the modifier are equal to the bone list.
- **joint_count**: The number of joints in the list which created by chains dynamically.
- **max_angular_velocity**: The maximum angular velocity per second.

**Methods:**
- clear_chains() - Clear all chains.
- get_end_bone(index: int) -> int - Returns the end bone index of the bone chain.
- get_end_bone_name(index: int) -> String - Returns the end bone name of the bone chain.
- get_root_bone(index: int) -> int - Returns the root bone index of the bone chain.
- get_root_bone_name(index: int) -> String - Returns the root bone name of the bone chain.
- reset() - Sets the reference pose for angle comparison to the current pose with the influence of constraints removed. This function is automatically triggered when joints change or upon activation.
- set_end_bone(index: int, bone: int) - Sets the end bone index of the bone chain.
- set_end_bone_name(index: int, bone_name: String) - Sets the end bone name of the bone chain. **Note:** End bone must be the root bone or a child of the root bone.
- set_root_bone(index: int, bone: int) - Sets the root bone index of the bone chain.
- set_root_bone_name(index: int, bone_name: String) - Sets the root bone name of the bone chain.

