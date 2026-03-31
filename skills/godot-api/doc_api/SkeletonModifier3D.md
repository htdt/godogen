## SkeletonModifier3D <- Node3D

SkeletonModifier3D retrieves a target Skeleton3D by having a Skeleton3D parent. If there is an AnimationMixer, a modification always performs after playback process of the AnimationMixer. This node should be used to implement custom IK solvers, constraints, or skeleton physics.

**Props:**
- active: bool = true
- influence: float = 1.0

- **active**: If `true`, the SkeletonModifier3D will be processing.
- **influence**: Sets the influence of the modification. **Note:** This value is used by Skeleton3D to blend, so the SkeletonModifier3D should always apply only 100% of the result without interpolation.

**Methods:**
- _process_modification() - Override this virtual method to implement a custom skeleton modifier. You should do things like get the Skeleton3D's current pose and apply the pose here. `_process_modification` must not apply `influence` to bone poses because the Skeleton3D automatically applies influence to all bone poses set by the modifier.
- _process_modification_with_delta(delta: float) - Override this virtual method to implement a custom skeleton modifier. You should do things like get the Skeleton3D's current pose and apply the pose here. `_process_modification_with_delta` must not apply `influence` to bone poses because the Skeleton3D automatically applies influence to all bone poses set by the modifier. `delta` is passed from parent Skeleton3D. See also `Skeleton3D.advance`. **Note:** This method may be called outside `Node._process` and `Node._physics_process` with `delta` is `0.0`, since the modification should be processed immediately after initialization of the Skeleton3D.
- _skeleton_changed(old_skeleton: Skeleton3D, new_skeleton: Skeleton3D) - Called when the skeleton is changed.
- _validate_bone_names() - Called when bone names and indices need to be validated, such as when entering the scene tree or changing skeleton.
- get_skeleton() -> Skeleton3D - Returns the parent Skeleton3D node if it exists. Otherwise, returns `null`.

**Signals:**
- modification_processed - Notifies when the modification have been finished. **Note:** If you want to get the modified bone pose by the modifier, you must use `Skeleton3D.get_bone_pose` or `Skeleton3D.get_bone_global_pose` at the moment this signal is fired.

**Enums:**
**BoneAxis:** BONE_AXIS_PLUS_X=0, BONE_AXIS_MINUS_X=1, BONE_AXIS_PLUS_Y=2, BONE_AXIS_MINUS_Y=3, BONE_AXIS_PLUS_Z=4, BONE_AXIS_MINUS_Z=5
  - BONE_AXIS_PLUS_X: Enumerated value for the +X axis.
  - BONE_AXIS_MINUS_X: Enumerated value for the -X axis.
  - BONE_AXIS_PLUS_Y: Enumerated value for the +Y axis.
  - BONE_AXIS_MINUS_Y: Enumerated value for the -Y axis.
  - BONE_AXIS_PLUS_Z: Enumerated value for the +Z axis.
  - BONE_AXIS_MINUS_Z: Enumerated value for the -Z axis.
**BoneDirection:** BONE_DIRECTION_PLUS_X=0, BONE_DIRECTION_MINUS_X=1, BONE_DIRECTION_PLUS_Y=2, BONE_DIRECTION_MINUS_Y=3, BONE_DIRECTION_PLUS_Z=4, BONE_DIRECTION_MINUS_Z=5, BONE_DIRECTION_FROM_PARENT=6
  - BONE_DIRECTION_PLUS_X: Enumerated value for the +X axis.
  - BONE_DIRECTION_MINUS_X: Enumerated value for the -X axis.
  - BONE_DIRECTION_PLUS_Y: Enumerated value for the +Y axis.
  - BONE_DIRECTION_MINUS_Y: Enumerated value for the -Y axis.
  - BONE_DIRECTION_PLUS_Z: Enumerated value for the +Z axis.
  - BONE_DIRECTION_MINUS_Z: Enumerated value for the -Z axis.
  - BONE_DIRECTION_FROM_PARENT: Enumerated value for the axis from a parent bone to the child bone.
**SecondaryDirection:** SECONDARY_DIRECTION_NONE=0, SECONDARY_DIRECTION_PLUS_X=1, SECONDARY_DIRECTION_MINUS_X=2, SECONDARY_DIRECTION_PLUS_Y=3, SECONDARY_DIRECTION_MINUS_Y=4, SECONDARY_DIRECTION_PLUS_Z=5, SECONDARY_DIRECTION_MINUS_Z=6, SECONDARY_DIRECTION_CUSTOM=7
  - SECONDARY_DIRECTION_NONE: Enumerated value for the case when the axis is undefined.
  - SECONDARY_DIRECTION_PLUS_X: Enumerated value for the +X axis.
  - SECONDARY_DIRECTION_MINUS_X: Enumerated value for the -X axis.
  - SECONDARY_DIRECTION_PLUS_Y: Enumerated value for the +Y axis.
  - SECONDARY_DIRECTION_MINUS_Y: Enumerated value for the -Y axis.
  - SECONDARY_DIRECTION_PLUS_Z: Enumerated value for the +Z axis.
  - SECONDARY_DIRECTION_MINUS_Z: Enumerated value for the -Z axis.
  - SECONDARY_DIRECTION_CUSTOM: Enumerated value for an optional axis.
**RotationAxis:** ROTATION_AXIS_X=0, ROTATION_AXIS_Y=1, ROTATION_AXIS_Z=2, ROTATION_AXIS_ALL=3, ROTATION_AXIS_CUSTOM=4
  - ROTATION_AXIS_X: Enumerated value for the rotation of the X axis.
  - ROTATION_AXIS_Y: Enumerated value for the rotation of the Y axis.
  - ROTATION_AXIS_Z: Enumerated value for the rotation of the Z axis.
  - ROTATION_AXIS_ALL: Enumerated value for the unconstrained rotation.
  - ROTATION_AXIS_CUSTOM: Enumerated value for an optional rotation axis.

