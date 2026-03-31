## ChainIK3D <- IKModifier3D

Base class of SkeletonModifier3D that automatically generates a joint list from the bones between the root bone and the end bone. **Note:** All the methods in this class take an `index` parameter. This parameter specifies which setting list entry to return if the IK has multiple entries (e.g. `settings/<index>/root_bone_name`).

**Methods:**
- get_end_bone(index: int) -> int - Returns the end bone index of the bone chain.
- get_end_bone_direction(index: int) -> int - Returns the tail direction of the end bone of the bone chain when `is_end_bone_extended` is `true`.
- get_end_bone_length(index: int) -> float - Returns the end bone tail length of the bone chain when `is_end_bone_extended` is `true`.
- get_end_bone_name(index: int) -> String - Returns the end bone name of the bone chain.
- get_joint_bone(index: int, joint: int) -> int - Returns the bone index at `joint` in the bone chain's joint list.
- get_joint_bone_name(index: int, joint: int) -> String - Returns the bone name at `joint` in the bone chain's joint list.
- get_joint_count(index: int) -> int - Returns the joint count of the bone chain's joint list.
- get_root_bone(index: int) -> int - Returns the root bone index of the bone chain.
- get_root_bone_name(index: int) -> String - Returns the root bone name of the bone chain.
- is_end_bone_extended(index: int) -> bool - Returns `true` if the end bone is extended to have a tail.
- set_end_bone(index: int, bone: int) - Sets the end bone index of the bone chain.
- set_end_bone_direction(index: int, bone_direction: int) - Sets the end bone tail direction of the bone chain when `is_end_bone_extended` is `true`.
- set_end_bone_length(index: int, length: float) - Sets the end bone tail length of the bone chain when `is_end_bone_extended` is `true`.
- set_end_bone_name(index: int, bone_name: String) - Sets the end bone name of the bone chain. **Note:** The end bone must be the root bone or a child of the root bone. If they are the same, the tail must be extended by `set_extend_end_bone` to modify the bone.
- set_extend_end_bone(index: int, enabled: bool) - If `enabled` is `true`, the end bone is extended to have a tail. The extended tail config is allocated to the last element in the joint list. In other words, if you set `enabled` to `false`, the config of the last element in the joint list has no effect in the simulated result.
- set_root_bone(index: int, bone: int) - Sets the root bone index of the bone chain.
- set_root_bone_name(index: int, bone_name: String) - Sets the root bone name of the bone chain.

