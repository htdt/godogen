## LookAtModifier3D <- SkeletonModifier3D

This SkeletonModifier3D rotates a bone to look at a target. This is helpful for moving a character's head to look at the player, rotating a turret to look at a target, or any other case where you want to make a bone rotate towards something quickly and easily. When applying multiple LookAtModifier3Ds, the LookAtModifier3D assigned to the parent bone must be put above the LookAtModifier3D assigned to the child bone in the list in order for the child bone results to be correct.

**Props:**
- bone: int = -1
- bone_name: String = ""
- duration: float = 0.0
- ease_type: int (Tween.EaseType) = 0
- forward_axis: int (SkeletonModifier3D.BoneAxis) = 4
- origin_bone: int
- origin_bone_name: String
- origin_external_node: NodePath
- origin_from: int (LookAtModifier3D.OriginFrom) = 0
- origin_offset: Vector3 = Vector3(0, 0, 0)
- origin_safe_margin: float = 0.1
- primary_damp_threshold: float
- primary_limit_angle: float
- primary_negative_damp_threshold: float
- primary_negative_limit_angle: float
- primary_positive_damp_threshold: float
- primary_positive_limit_angle: float
- primary_rotation_axis: int (Vector3.Axis) = 1
- relative: bool = false
- secondary_damp_threshold: float
- secondary_limit_angle: float
- secondary_negative_damp_threshold: float
- secondary_negative_limit_angle: float
- secondary_positive_damp_threshold: float
- secondary_positive_limit_angle: float
- symmetry_limitation: bool
- target_node: NodePath = NodePath("")
- transition_type: int (Tween.TransitionType) = 0
- use_angle_limitation: bool = false
- use_secondary_rotation: bool = true

- **bone**: Index of the `bone_name` in the parent Skeleton3D.
- **bone_name**: The bone name of the Skeleton3D that the modification will operate on.
- **duration**: The duration of the time-based interpolation. Interpolation is triggered at the following cases: - When the target node is changed - When an axis is flipped due to angle limitation **Note:** The flipping occurs when the target is outside the angle limitation and the internally computed secondary rotation axis of the forward vector is flipped. Visually, it occurs when the target is outside the angle limitation and crosses the plane of the `forward_axis` and `primary_rotation_axis`.
- **ease_type**: The ease type of the time-based interpolation. See also `Tween.EaseType`.
- **forward_axis**: The forward axis of the bone. This SkeletonModifier3D modifies the bone so that this axis points toward the `target_node`.
- **origin_bone**: Index of the `origin_bone_name` in the parent Skeleton3D.
- **origin_bone_name**: If `origin_from` is `ORIGIN_FROM_SPECIFIC_BONE`, the bone global pose position specified for this is used as origin.
- **origin_external_node**: If `origin_from` is `ORIGIN_FROM_EXTERNAL_NODE`, the global position of the Node3D specified for this is used as origin.
- **origin_from**: This value determines from what origin is retrieved for use in the calculation of the forward vector.
- **origin_offset**: The offset of the bone pose origin. Matching the origins by offset is useful for cases where multiple bones must always face the same direction, such as the eyes. **Note:** This value indicates the local position of the object set in `origin_from`.
- **origin_safe_margin**: If the target passes through too close to the origin than this value, time-based interpolation is used even if the target is within the angular limitations, to prevent the angular velocity from becoming too high.
- **primary_damp_threshold**: The threshold to start damping for `primary_limit_angle`. It provides non-linear (b-spline) interpolation, let it feel more resistance the more it rotate to the edge limit. This is useful for simulating the limits of human motion. If `1.0`, no damping is performed. If `0.0`, damping is always performed.
- **primary_limit_angle**: The limit angle of the primary rotation when `symmetry_limitation` is `true`, in radians.
- **primary_negative_damp_threshold**: The threshold to start damping for `primary_negative_limit_angle`.
- **primary_negative_limit_angle**: The limit angle of negative side of the primary rotation when `symmetry_limitation` is `false`, in radians.
- **primary_positive_damp_threshold**: The threshold to start damping for `primary_positive_limit_angle`.
- **primary_positive_limit_angle**: The limit angle of positive side of the primary rotation when `symmetry_limitation` is `false`, in radians.
- **primary_rotation_axis**: The axis of the first rotation. This SkeletonModifier3D works by compositing the rotation by Euler angles to prevent to rotate the `forward_axis`.
- **relative**: The relative option. If `true`, the rotation is applied relative to the pose. If `false`, the rotation is applied relative to the rest. It means to replace the current pose with the LookAtModifier3D's result. **Note:** This option affects the base angle for `use_angle_limitation` unlike IterateIK3D's JointLimitation3D. Since the LookAtModifier3D relies strongly on Euler rotation, the axis that determines the limitation and the actual rotation are strongly tied together.
- **secondary_damp_threshold**: The threshold to start damping for `secondary_limit_angle`.
- **secondary_limit_angle**: The limit angle of the secondary rotation when `symmetry_limitation` is `true`, in radians.
- **secondary_negative_damp_threshold**: The threshold to start damping for `secondary_negative_limit_angle`.
- **secondary_negative_limit_angle**: The limit angle of negative side of the secondary rotation when `symmetry_limitation` is `false`, in radians.
- **secondary_positive_damp_threshold**: The threshold to start damping for `secondary_positive_limit_angle`.
- **secondary_positive_limit_angle**: The limit angle of positive side of the secondary rotation when `symmetry_limitation` is `false`, in radians.
- **symmetry_limitation**: If `true`, the limitations are spread from the bone symmetrically. If `false`, the limitation can be specified separately for each side of the bone rest.
- **target_node**: The NodePath to the node that is the target for the look at modification. This node is what the modification will rotate the bone to.
- **transition_type**: The transition type of the time-based interpolation. See also `Tween.TransitionType`.
- **use_angle_limitation**: If `true`, limits the amount of rotation. For example, this helps to prevent a character's neck from rotating 360 degrees. **Note:** As with AnimationTree blending, interpolation is provided that favors `Skeleton3D.get_bone_rest` or `Skeleton3D.get_bone_pose` depends on the `relative` option. This means that interpolation does not select the shortest path in some cases. **Note:** Some values for `transition_type` (such as `Tween.TRANS_BACK`, `Tween.TRANS_ELASTIC`, and `Tween.TRANS_SPRING`) may exceed the limitations. If interpolation occurs while overshooting the limitations, the result might not respect the bone rest.
- **use_secondary_rotation**: If `true`, provides rotation by two axes.

**Methods:**
- get_interpolation_remaining() -> float - Returns the remaining seconds of the time-based interpolation.
- is_interpolating() -> bool - Returns `true` if time-based interpolation is running. If `true`, it is equivalent to `get_interpolation_remaining` returning `0.0`. This is useful to determine whether a LookAtModifier3D can be removed safely.
- is_target_within_limitation() -> bool - Returns whether the target is within the angle limitations. It is useful for unsetting the `target_node` when the target is outside of the angle limitations. **Note:** The value is updated after `SkeletonModifier3D._process_modification`. To retrieve this value correctly, we recommend using the signal `SkeletonModifier3D.modification_processed`.

**Enums:**
**OriginFrom:** ORIGIN_FROM_SELF=0, ORIGIN_FROM_SPECIFIC_BONE=1, ORIGIN_FROM_EXTERNAL_NODE=2
  - ORIGIN_FROM_SELF: The bone rest position of the bone specified in `bone` is used as origin.
  - ORIGIN_FROM_SPECIFIC_BONE: The bone global pose position of the bone specified in `origin_bone` is used as origin. **Note:** It is recommended that you select only the parent bone unless you are familiar with the bone processing process. The specified bone pose at the time the LookAtModifier3D is processed is used as a reference. In other words, if you specify a child bone and the LookAtModifier3D causes the child bone to move, the rendered result and direction will not match.
  - ORIGIN_FROM_EXTERNAL_NODE: The global position of the Node3D specified in `origin_external_node` is used as origin. **Note:** Same as `ORIGIN_FROM_SPECIFIC_BONE`, when specifying a BoneAttachment3D with a child bone assigned, the rendered result and direction will not match.

