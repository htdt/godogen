## XRHandModifier3D <- SkeletonModifier3D

This node uses hand tracking data from an XRHandTracker to pose the skeleton of a hand mesh. Positioning of hands is performed by creating an XRNode3D ancestor of the hand mesh driven by the same XRHandTracker. The hand tracking position-data is scaled by `Skeleton3D.motion_scale` when applied to the skeleton, which can be used to adjust the tracked hand to match the scale of the hand model.

**Props:**
- bone_update: int (XRHandModifier3D.BoneUpdate) = 0
- hand_tracker: StringName = &"/user/hand_tracker/left"

- **bone_update**: Specifies the type of updates to perform on the bones.
- **hand_tracker**: The name of the XRHandTracker registered with XRServer to obtain the hand tracking data from.

**Enums:**
**BoneUpdate:** BONE_UPDATE_FULL=0, BONE_UPDATE_ROTATION_ONLY=1, BONE_UPDATE_MAX=2
  - BONE_UPDATE_FULL: The skeleton's bones are fully updated (both position and rotation) to match the tracked bones.
  - BONE_UPDATE_ROTATION_ONLY: The skeleton's bones are only rotated to align with the tracked bones, preserving bone length.
  - BONE_UPDATE_MAX: Represents the size of the `BoneUpdate` enum.

