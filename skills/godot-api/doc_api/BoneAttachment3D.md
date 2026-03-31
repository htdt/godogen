## BoneAttachment3D <- Node3D

This node selects a bone in a Skeleton3D and attaches to it. This means that the BoneAttachment3D node will either dynamically copy or override the 3D transform of the selected bone.

**Props:**
- bone_idx: int = -1
- bone_name: String = ""
- external_skeleton: NodePath
- override_pose: bool = false
- physics_interpolation_mode: int (Node.PhysicsInterpolationMode) = 2
- use_external_skeleton: bool = false

- **bone_idx**: The index of the attached bone.
- **bone_name**: The name of the attached bone.
- **external_skeleton**: The NodePath to the external Skeleton3D node.
- **override_pose**: Whether the BoneAttachment3D node will override the bone pose of the bone it is attached to. When set to `true`, the BoneAttachment3D node can change the pose of the bone. When set to `false`, the BoneAttachment3D will always be set to the bone's transform. **Note:** This override performs interruptively in the skeleton update process using signals due to the old design. It may cause unintended behavior when used at the same time with SkeletonModifier3D.
- **use_external_skeleton**: Whether the BoneAttachment3D node will use an external Skeleton3D node rather than attempting to use its parent node as the Skeleton3D. When set to `true`, the BoneAttachment3D node will use the external Skeleton3D node set in `external_skeleton`.

**Methods:**
- get_skeleton() -> Skeleton3D - Returns the parent or external Skeleton3D node if it exists, otherwise returns `null`.
- on_skeleton_update() - A function that is called automatically when the Skeleton3D is updated. This function is where the BoneAttachment3D node updates its position so it is correctly bound when it is *not* set to override the bone pose.

