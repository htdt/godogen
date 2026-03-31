## IterateIK3D <- ChainIK3D

Base class of SkeletonModifier3D to approach the goal by repeating small rotations. Each bone chain (setting) has one effector, which is processed in order of the setting list. You can set some limitations for each joint. **Note:** All the methods in this class take an `index` parameter. This parameter specifies which setting list entry to return if the IK has multiple entries (e.g. `settings/<index>/target_node`).

**Props:**
- angular_delta_limit: float = 0.034906585
- deterministic: bool = false
- max_iterations: int = 4
- min_distance: float = 0.001
- setting_count: int = 0

- **angular_delta_limit**: The maximum amount each bone can rotate in a single iteration. **Note:** This limitation is applied during each iteration. For example, if `max_iterations` is `4` and `angular_delta_limit` is `5` degrees, the maximum rotation possible in a single frame is `20` degrees.
- **deterministic**: If `false`, the result is calculated from the previous frame's IterateIK3D result as the initial state. If `true`, the previous frame's IterateIK3D result is discarded. At this point, the new result is calculated from the bone pose excluding the IterateIK3D as the initial state. This means the result will be always equal as long as the target position and the previous bone pose are the same. However, if `angular_delta_limit` and `max_iterations` are set too small, the end bone of the chain will never reach the target.
- **max_iterations**: The number of iteration loops used by the IK solver to produce more accurate results.
- **min_distance**: The minimum distance between the end bone and the target. If the distance is below this value, the IK solver stops any further iterations.
- **setting_count**: The number of settings.

**Methods:**
- get_joint_limitation(index: int, joint: int) -> JointLimitation3D - Returns the joint limitation at `joint` in the bone chain's joint list.
- get_joint_limitation_right_axis(index: int, joint: int) -> int - Returns the joint limitation right axis at `joint` in the bone chain's joint list.
- get_joint_limitation_right_axis_vector(index: int, joint: int) -> Vector3 - Returns the joint limitation right axis vector at `joint` in the bone chain's joint list. If `get_joint_limitation_right_axis` is `SkeletonModifier3D.SECONDARY_DIRECTION_NONE`, this method returns `Vector3(0, 0, 0)`.
- get_joint_limitation_rotation_offset(index: int, joint: int) -> Quaternion - Returns the joint limitation rotation offset at `joint` in the bone chain's joint list. Rotation is done in the local space which is constructed by the bone direction (in general parent to child) as the +Y axis and `get_joint_limitation_right_axis_vector` as the +X axis. If the +X and +Y axes are not orthogonal, the +X axis is implicitly modified to make it orthogonal. Also, if the length of `get_joint_limitation_right_axis_vector` is zero, the space is created by rotating the bone rest using the shortest arc that rotates the +Y axis of the bone rest to match the bone direction.
- get_joint_rotation_axis(index: int, joint: int) -> int - Returns the rotation axis at `joint` in the bone chain's joint list.
- get_joint_rotation_axis_vector(index: int, joint: int) -> Vector3 - Returns the rotation axis vector for the specified joint in the bone chain. This vector represents the axis around which the joint can rotate. It is determined based on the rotation axis set for the joint. If `get_joint_rotation_axis` is `SkeletonModifier3D.ROTATION_AXIS_ALL`, this method returns `Vector3(0, 0, 0)`.
- get_target_node(index: int) -> NodePath - Returns the target node that the end bone is trying to reach.
- set_joint_limitation(index: int, joint: int, limitation: JointLimitation3D) - Sets the joint limitation at `joint` in the bone chain's joint list.
- set_joint_limitation_right_axis(index: int, joint: int, direction: int) - Sets the joint limitation right axis at `joint` in the bone chain's joint list.
- set_joint_limitation_right_axis_vector(index: int, joint: int, vector: Vector3) - Sets the optional joint limitation right axis vector at `joint` in the bone chain's joint list.
- set_joint_limitation_rotation_offset(index: int, joint: int, offset: Quaternion) - Sets the joint limitation rotation offset at `joint` in the bone chain's joint list. Rotation is done in the local space which is constructed by the bone direction (in general parent to child) as the +Y axis and `get_joint_limitation_right_axis_vector` as the +X axis. If the +X and +Y axes are not orthogonal, the +X axis is implicitly modified to make it orthogonal. Also, if the length of `get_joint_limitation_right_axis_vector` is zero, the space is created by rotating the bone rest using the shortest arc that rotates the +Y axis of the bone rest to match the bone direction.
- set_joint_rotation_axis(index: int, joint: int, axis: int) - Sets the rotation axis at `joint` in the bone chain's joint list. The axes are based on the `Skeleton3D.get_bone_rest`'s space, if `axis` is `SkeletonModifier3D.ROTATION_AXIS_CUSTOM`, you can specify any axis. **Note:** The rotation axis and the forward vector shouldn't be colinear to avoid unintended rotation since ChainIK3D does not factor in twisting forces.
- set_joint_rotation_axis_vector(index: int, joint: int, axis_vector: Vector3) - Sets the rotation axis vector for the specified joint in the bone chain. This vector is normalized by an internal process and represents the axis around which the bone chain can rotate. If the vector length is `0`, it is considered synonymous with `SkeletonModifier3D.ROTATION_AXIS_ALL`.
- set_target_node(index: int, target_node: NodePath) - Sets the target node that the end bone is trying to reach.

