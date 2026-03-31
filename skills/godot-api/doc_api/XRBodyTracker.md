## XRBodyTracker <- XRPositionalTracker

A body tracking system will create an instance of this object and add it to the XRServer. This tracking system will then obtain skeleton data, convert it to the Godot Humanoid skeleton and store this data on the XRBodyTracker object. Use XRBodyModifier3D to animate a body mesh using body tracking data.

**Props:**
- body_flags: int (XRBodyTracker.BodyFlags) = 0
- has_tracking_data: bool = false
- type: int (XRServer.TrackerType) = 32

- **body_flags**: The type of body tracking data captured.
- **has_tracking_data**: If `true`, the body tracking data is valid.

**Methods:**
- get_joint_flags(joint: int) -> int - Returns flags about the validity of the tracking data for the given body joint.
- get_joint_transform(joint: int) -> Transform3D - Returns the transform for the given body joint.
- set_joint_flags(joint: int, flags: int) - Sets flags about the validity of the tracking data for the given body joint.
- set_joint_transform(joint: int, transform: Transform3D) - Sets the transform for the given body joint.

**Enums:**
**BodyFlags:** BODY_FLAG_UPPER_BODY_SUPPORTED=1, BODY_FLAG_LOWER_BODY_SUPPORTED=2, BODY_FLAG_HANDS_SUPPORTED=4
  - BODY_FLAG_UPPER_BODY_SUPPORTED: Upper body tracking supported.
  - BODY_FLAG_LOWER_BODY_SUPPORTED: Lower body tracking supported.
  - BODY_FLAG_HANDS_SUPPORTED: Hand tracking supported.
**Joint:** JOINT_ROOT=0, JOINT_HIPS=1, JOINT_SPINE=2, JOINT_CHEST=3, JOINT_UPPER_CHEST=4, JOINT_NECK=5, JOINT_HEAD=6, JOINT_HEAD_TIP=7, JOINT_LEFT_SHOULDER=8, JOINT_LEFT_UPPER_ARM=9, ...
  - JOINT_ROOT: Root joint.
  - JOINT_HIPS: Hips joint.
  - JOINT_SPINE: Spine joint.
  - JOINT_CHEST: Chest joint.
  - JOINT_UPPER_CHEST: Upper chest joint.
  - JOINT_NECK: Neck joint.
  - JOINT_HEAD: Head joint.
  - JOINT_HEAD_TIP: Head tip joint.
  - JOINT_LEFT_SHOULDER: Left shoulder joint.
  - JOINT_LEFT_UPPER_ARM: Left upper arm joint.
  - JOINT_LEFT_LOWER_ARM: Left lower arm joint.
  - JOINT_RIGHT_SHOULDER: Right shoulder joint.
  - JOINT_RIGHT_UPPER_ARM: Right upper arm joint.
  - JOINT_RIGHT_LOWER_ARM: Right lower arm joint.
  - JOINT_LEFT_UPPER_LEG: Left upper leg joint.
  - JOINT_LEFT_LOWER_LEG: Left lower leg joint.
  - JOINT_LEFT_FOOT: Left foot joint.
  - JOINT_LEFT_TOES: Left toes joint.
  - JOINT_RIGHT_UPPER_LEG: Right upper leg joint.
  - JOINT_RIGHT_LOWER_LEG: Right lower leg joint.
  - JOINT_RIGHT_FOOT: Right foot joint.
  - JOINT_RIGHT_TOES: Right toes joint.
  - JOINT_LEFT_HAND: Left hand joint.
  - JOINT_LEFT_PALM: Left palm joint.
  - JOINT_LEFT_WRIST: Left wrist joint.
  - JOINT_LEFT_THUMB_METACARPAL: Left thumb metacarpal joint.
  - JOINT_LEFT_THUMB_PHALANX_PROXIMAL: Left thumb phalanx proximal joint.
  - JOINT_LEFT_THUMB_PHALANX_DISTAL: Left thumb phalanx distal joint.
  - JOINT_LEFT_THUMB_TIP: Left thumb tip joint.
  - JOINT_LEFT_INDEX_FINGER_METACARPAL: Left index finger metacarpal joint.
  - JOINT_LEFT_INDEX_FINGER_PHALANX_PROXIMAL: Left index finger phalanx proximal joint.
  - JOINT_LEFT_INDEX_FINGER_PHALANX_INTERMEDIATE: Left index finger phalanx intermediate joint.
  - JOINT_LEFT_INDEX_FINGER_PHALANX_DISTAL: Left index finger phalanx distal joint.
  - JOINT_LEFT_INDEX_FINGER_TIP: Left index finger tip joint.
  - JOINT_LEFT_MIDDLE_FINGER_METACARPAL: Left middle finger metacarpal joint.
  - JOINT_LEFT_MIDDLE_FINGER_PHALANX_PROXIMAL: Left middle finger phalanx proximal joint.
  - JOINT_LEFT_MIDDLE_FINGER_PHALANX_INTERMEDIATE: Left middle finger phalanx intermediate joint.
  - JOINT_LEFT_MIDDLE_FINGER_PHALANX_DISTAL: Left middle finger phalanx distal joint.
  - JOINT_LEFT_MIDDLE_FINGER_TIP: Left middle finger tip joint.
  - JOINT_LEFT_RING_FINGER_METACARPAL: Left ring finger metacarpal joint.
  - JOINT_LEFT_RING_FINGER_PHALANX_PROXIMAL: Left ring finger phalanx proximal joint.
  - JOINT_LEFT_RING_FINGER_PHALANX_INTERMEDIATE: Left ring finger phalanx intermediate joint.
  - JOINT_LEFT_RING_FINGER_PHALANX_DISTAL: Left ring finger phalanx distal joint.
  - JOINT_LEFT_RING_FINGER_TIP: Left ring finger tip joint.
  - JOINT_LEFT_PINKY_FINGER_METACARPAL: Left pinky finger metacarpal joint.
  - JOINT_LEFT_PINKY_FINGER_PHALANX_PROXIMAL: Left pinky finger phalanx proximal joint.
  - JOINT_LEFT_PINKY_FINGER_PHALANX_INTERMEDIATE: Left pinky finger phalanx intermediate joint.
  - JOINT_LEFT_PINKY_FINGER_PHALANX_DISTAL: Left pinky finger phalanx distal joint.
  - JOINT_LEFT_PINKY_FINGER_TIP: Left pinky finger tip joint.
  - JOINT_RIGHT_HAND: Right hand joint.
  - JOINT_RIGHT_PALM: Right palm joint.
  - JOINT_RIGHT_WRIST: Right wrist joint.
  - JOINT_RIGHT_THUMB_METACARPAL: Right thumb metacarpal joint.
  - JOINT_RIGHT_THUMB_PHALANX_PROXIMAL: Right thumb phalanx proximal joint.
  - JOINT_RIGHT_THUMB_PHALANX_DISTAL: Right thumb phalanx distal joint.
  - JOINT_RIGHT_THUMB_TIP: Right thumb tip joint.
  - JOINT_RIGHT_INDEX_FINGER_METACARPAL: Right index finger metacarpal joint.
  - JOINT_RIGHT_INDEX_FINGER_PHALANX_PROXIMAL: Right index finger phalanx proximal joint.
  - JOINT_RIGHT_INDEX_FINGER_PHALANX_INTERMEDIATE: Right index finger phalanx intermediate joint.
  - JOINT_RIGHT_INDEX_FINGER_PHALANX_DISTAL: Right index finger phalanx distal joint.
  - JOINT_RIGHT_INDEX_FINGER_TIP: Right index finger tip joint.
  - JOINT_RIGHT_MIDDLE_FINGER_METACARPAL: Right middle finger metacarpal joint.
  - JOINT_RIGHT_MIDDLE_FINGER_PHALANX_PROXIMAL: Right middle finger phalanx proximal joint.
  - JOINT_RIGHT_MIDDLE_FINGER_PHALANX_INTERMEDIATE: Right middle finger phalanx intermediate joint.
  - JOINT_RIGHT_MIDDLE_FINGER_PHALANX_DISTAL: Right middle finger phalanx distal joint.
  - JOINT_RIGHT_MIDDLE_FINGER_TIP: Right middle finger tip joint.
  - JOINT_RIGHT_RING_FINGER_METACARPAL: Right ring finger metacarpal joint.
  - JOINT_RIGHT_RING_FINGER_PHALANX_PROXIMAL: Right ring finger phalanx proximal joint.
  - JOINT_RIGHT_RING_FINGER_PHALANX_INTERMEDIATE: Right ring finger phalanx intermediate joint.
  - JOINT_RIGHT_RING_FINGER_PHALANX_DISTAL: Right ring finger phalanx distal joint.
  - JOINT_RIGHT_RING_FINGER_TIP: Right ring finger tip joint.
  - JOINT_RIGHT_PINKY_FINGER_METACARPAL: Right pinky finger metacarpal joint.
  - JOINT_RIGHT_PINKY_FINGER_PHALANX_PROXIMAL: Right pinky finger phalanx proximal joint.
  - JOINT_RIGHT_PINKY_FINGER_PHALANX_INTERMEDIATE: Right pinky finger phalanx intermediate joint.
  - JOINT_RIGHT_PINKY_FINGER_PHALANX_DISTAL: Right pinky finger phalanx distal joint.
  - JOINT_RIGHT_PINKY_FINGER_TIP: Right pinky finger tip joint.
  - JOINT_LOWER_CHEST: Lower chest joint.
  - JOINT_LEFT_SCAPULA: Left scapula joint.
  - JOINT_LEFT_WRIST_TWIST: Left wrist twist joint.
  - JOINT_RIGHT_SCAPULA: Right scapula joint.
  - JOINT_RIGHT_WRIST_TWIST: Right wrist twist joint.
  - JOINT_LEFT_FOOT_TWIST: Left foot twist joint.
  - JOINT_LEFT_HEEL: Left heel joint.
  - JOINT_LEFT_MIDDLE_FOOT: Left middle foot joint.
  - JOINT_RIGHT_FOOT_TWIST: Right foot twist joint.
  - JOINT_RIGHT_HEEL: Right heel joint.
  - JOINT_RIGHT_MIDDLE_FOOT: Right middle foot joint.
  - JOINT_MAX: Represents the size of the `Joint` enum.
**JointFlags:** JOINT_FLAG_ORIENTATION_VALID=1, JOINT_FLAG_ORIENTATION_TRACKED=2, JOINT_FLAG_POSITION_VALID=4, JOINT_FLAG_POSITION_TRACKED=8
  - JOINT_FLAG_ORIENTATION_VALID: The joint's orientation data is valid.
  - JOINT_FLAG_ORIENTATION_TRACKED: The joint's orientation is actively tracked. May not be set if tracking has been temporarily lost.
  - JOINT_FLAG_POSITION_VALID: The joint's position data is valid.
  - JOINT_FLAG_POSITION_TRACKED: The joint's position is actively tracked. May not be set if tracking has been temporarily lost.

