## XRBodyModifier3D <- SkeletonModifier3D

This node uses body tracking data from an XRBodyTracker to pose the skeleton of a body mesh. Positioning of the body is performed by creating an XRNode3D ancestor of the body mesh driven by the same XRBodyTracker. The body tracking position-data is scaled by `Skeleton3D.motion_scale` when applied to the skeleton, which can be used to adjust the tracked body to match the scale of the body model.

**Props:**
- body_tracker: StringName = &"/user/body_tracker"
- body_update: int (XRBodyModifier3D.BodyUpdate) = 7
- bone_update: int (XRBodyModifier3D.BoneUpdate) = 0

- **body_tracker**: The name of the XRBodyTracker registered with XRServer to obtain the body tracking data from.
- **body_update**: Specifies the body parts to update.
- **bone_update**: Specifies the type of updates to perform on the bones.

**Enums:**
**BodyUpdate:** BODY_UPDATE_UPPER_BODY=1, BODY_UPDATE_LOWER_BODY=2, BODY_UPDATE_HANDS=4
  - BODY_UPDATE_UPPER_BODY: The skeleton's upper body joints are updated.
  - BODY_UPDATE_LOWER_BODY: The skeleton's lower body joints are updated.
  - BODY_UPDATE_HANDS: The skeleton's hand joints are updated.
**BoneUpdate:** BONE_UPDATE_FULL=0, BONE_UPDATE_ROTATION_ONLY=1, BONE_UPDATE_MAX=2
  - BONE_UPDATE_FULL: The skeleton's bones are fully updated (both position and rotation) to match the tracked bones.
  - BONE_UPDATE_ROTATION_ONLY: The skeleton's bones are only rotated to align with the tracked bones, preserving bone length.
  - BONE_UPDATE_MAX: Represents the size of the `BoneUpdate` enum.

