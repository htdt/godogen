## TwoBoneIK3D <- IKModifier3D

This IKModifier3D requires a pole target. It provides deterministic results by constructing a plane from each joint and pole target and finding the intersection of two circles (disks in 3D). This IK can handle twist by setting the pole direction. If there are more than one bone between each set bone, their rotations are ignored, and the straight line connecting the root-middle and middle-end joints are treated as virtual bones. **Note:** All the methods in this class take an `index` parameter. This parameter specifies which setting list entry to return if the IK has multiple entries (e.g. `settings/<index>/root_bone_name`).

**Props:**
- setting_count: int = 0

- **setting_count**: The number of settings.

**Methods:**
- get_end_bone(index: int) -> int - Returns the end bone index.
- get_end_bone_direction(index: int) -> int - Returns the end bone's tail direction when `is_end_bone_extended` is `true`.
- get_end_bone_length(index: int) -> float - Returns the end bone tail length of the bone chain when `is_end_bone_extended` is `true`.
- get_end_bone_name(index: int) -> String - Returns the end bone name.
- get_middle_bone(index: int) -> int - Returns the middle bone index.
- get_middle_bone_name(index: int) -> String - Returns the middle bone name.
- get_pole_direction(index: int) -> int - Returns the pole direction.
- get_pole_direction_vector(index: int) -> Vector3 - Returns the pole direction vector. If `get_pole_direction` is `SkeletonModifier3D.SECONDARY_DIRECTION_NONE`, this method returns `Vector3(0, 0, 0)`.
- get_pole_node(index: int) -> NodePath - Returns the pole target node that constructs a plane which the joints are all on and the pole is trying to direct.
- get_root_bone(index: int) -> int - Returns the root bone index.
- get_root_bone_name(index: int) -> String - Returns the root bone name.
- get_target_node(index: int) -> NodePath - Returns the target node that the end bone is trying to reach.
- is_end_bone_extended(index: int) -> bool - Returns `true` if the end bone is extended to have a tail.
- is_using_virtual_end(index: int) -> bool - Returns `true` if the end bone is extended from the middle bone as a virtual bone.
- set_end_bone(index: int, bone: int) - Sets the end bone index.
- set_end_bone_direction(index: int, bone_direction: int) - Sets the end bone tail direction when `is_end_bone_extended` is `true`.
- set_end_bone_length(index: int, length: float) - Sets the end bone tail length when `is_end_bone_extended` is `true`.
- set_end_bone_name(index: int, bone_name: String) - Sets the end bone name. **Note:** The end bone must be a child of the middle bone.
- set_extend_end_bone(index: int, enabled: bool) - If `enabled` is `true`, the end bone is extended to have a tail.
- set_middle_bone(index: int, bone: int) - Sets the middle bone index.
- set_middle_bone_name(index: int, bone_name: String) - Sets the middle bone name. **Note:** The middle bone must be a child of the root bone.
- set_pole_direction(index: int, direction: int) - Sets the pole direction. The pole is on the middle bone and will direct to the pole target. The rotation axis is a vector that is orthogonal to this and the forward vector. **Note:** The pole direction and the forward vector shouldn't be colinear to avoid unintended rotation.
- set_pole_direction_vector(index: int, vector: Vector3) - Sets the pole direction vector. This vector is normalized by an internal process. If the vector length is `0`, it is considered synonymous with `SkeletonModifier3D.SECONDARY_DIRECTION_NONE`.
- set_pole_node(index: int, pole_node: NodePath) - Sets the pole target node that constructs a plane which the joints are all on and the pole is trying to direct.
- set_root_bone(index: int, bone: int) - Sets the root bone index.
- set_root_bone_name(index: int, bone_name: String) - Sets the root bone name.
- set_target_node(index: int, target_node: NodePath) - Sets the target node that the end bone is trying to reach.
- set_use_virtual_end(index: int, enabled: bool) - If `enabled` is `true`, the end bone is extended from the middle bone as a virtual bone.

