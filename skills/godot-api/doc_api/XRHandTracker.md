## XRHandTracker <- XRPositionalTracker

A hand tracking system will create an instance of this object and add it to the XRServer. This tracking system will then obtain skeleton data, convert it to the Godot Humanoid hand skeleton and store this data on the XRHandTracker object. Use XRHandModifier3D to animate a hand mesh using hand tracking data.

**Props:**
- hand: int (XRPositionalTracker.TrackerHand) = 1
- hand_tracking_source: int (XRHandTracker.HandTrackingSource) = 0
- has_tracking_data: bool = false
- type: int (XRServer.TrackerType) = 16

- **hand_tracking_source**: The source of the hand tracking data.
- **has_tracking_data**: If `true`, the hand tracking data is valid.

**Methods:**
- get_hand_joint_angular_velocity(joint: int) -> Vector3 - Returns the angular velocity for the given hand joint.
- get_hand_joint_flags(joint: int) -> int - Returns flags about the validity of the tracking data for the given hand joint.
- get_hand_joint_linear_velocity(joint: int) -> Vector3 - Returns the linear velocity for the given hand joint.
- get_hand_joint_radius(joint: int) -> float - Returns the radius of the given hand joint.
- get_hand_joint_transform(joint: int) -> Transform3D - Returns the transform for the given hand joint.
- set_hand_joint_angular_velocity(joint: int, angular_velocity: Vector3) - Sets the angular velocity for the given hand joint.
- set_hand_joint_flags(joint: int, flags: int) - Sets flags about the validity of the tracking data for the given hand joint.
- set_hand_joint_linear_velocity(joint: int, linear_velocity: Vector3) - Sets the linear velocity for the given hand joint.
- set_hand_joint_radius(joint: int, radius: float) - Sets the radius of the given hand joint.
- set_hand_joint_transform(joint: int, transform: Transform3D) - Sets the transform for the given hand joint.

**Enums:**
**HandTrackingSource:** HAND_TRACKING_SOURCE_UNKNOWN=0, HAND_TRACKING_SOURCE_UNOBSTRUCTED=1, HAND_TRACKING_SOURCE_CONTROLLER=2, HAND_TRACKING_SOURCE_NOT_TRACKED=3, HAND_TRACKING_SOURCE_MAX=4
  - HAND_TRACKING_SOURCE_UNKNOWN: The source of hand tracking data is unknown.
  - HAND_TRACKING_SOURCE_UNOBSTRUCTED: The source of hand tracking data is unobstructed, meaning that an accurate method of hand tracking is used. These include optical hand tracking, data gloves, etc.
  - HAND_TRACKING_SOURCE_CONTROLLER: The source of hand tracking data is a controller, meaning that joint positions are inferred from controller inputs.
  - HAND_TRACKING_SOURCE_NOT_TRACKED: No hand tracking data is tracked, this either means the hand is obscured, the controller is turned off, or tracking is not supported for the current input type.
  - HAND_TRACKING_SOURCE_MAX: Represents the size of the `HandTrackingSource` enum.
**HandJoint:** HAND_JOINT_PALM=0, HAND_JOINT_WRIST=1, HAND_JOINT_THUMB_METACARPAL=2, HAND_JOINT_THUMB_PHALANX_PROXIMAL=3, HAND_JOINT_THUMB_PHALANX_DISTAL=4, HAND_JOINT_THUMB_TIP=5, HAND_JOINT_INDEX_FINGER_METACARPAL=6, HAND_JOINT_INDEX_FINGER_PHALANX_PROXIMAL=7, HAND_JOINT_INDEX_FINGER_PHALANX_INTERMEDIATE=8, HAND_JOINT_INDEX_FINGER_PHALANX_DISTAL=9, ...
  - HAND_JOINT_PALM: Palm joint.
  - HAND_JOINT_WRIST: Wrist joint.
  - HAND_JOINT_THUMB_METACARPAL: Thumb metacarpal joint.
  - HAND_JOINT_THUMB_PHALANX_PROXIMAL: Thumb phalanx proximal joint.
  - HAND_JOINT_THUMB_PHALANX_DISTAL: Thumb phalanx distal joint.
  - HAND_JOINT_THUMB_TIP: Thumb tip joint.
  - HAND_JOINT_INDEX_FINGER_METACARPAL: Index finger metacarpal joint.
  - HAND_JOINT_INDEX_FINGER_PHALANX_PROXIMAL: Index finger phalanx proximal joint.
  - HAND_JOINT_INDEX_FINGER_PHALANX_INTERMEDIATE: Index finger phalanx intermediate joint.
  - HAND_JOINT_INDEX_FINGER_PHALANX_DISTAL: Index finger phalanx distal joint.
  - HAND_JOINT_INDEX_FINGER_TIP: Index finger tip joint.
  - HAND_JOINT_MIDDLE_FINGER_METACARPAL: Middle finger metacarpal joint.
  - HAND_JOINT_MIDDLE_FINGER_PHALANX_PROXIMAL: Middle finger phalanx proximal joint.
  - HAND_JOINT_MIDDLE_FINGER_PHALANX_INTERMEDIATE: Middle finger phalanx intermediate joint.
  - HAND_JOINT_MIDDLE_FINGER_PHALANX_DISTAL: Middle finger phalanx distal joint.
  - HAND_JOINT_MIDDLE_FINGER_TIP: Middle finger tip joint.
  - HAND_JOINT_RING_FINGER_METACARPAL: Ring finger metacarpal joint.
  - HAND_JOINT_RING_FINGER_PHALANX_PROXIMAL: Ring finger phalanx proximal joint.
  - HAND_JOINT_RING_FINGER_PHALANX_INTERMEDIATE: Ring finger phalanx intermediate joint.
  - HAND_JOINT_RING_FINGER_PHALANX_DISTAL: Ring finger phalanx distal joint.
  - HAND_JOINT_RING_FINGER_TIP: Ring finger tip joint.
  - HAND_JOINT_PINKY_FINGER_METACARPAL: Pinky finger metacarpal joint.
  - HAND_JOINT_PINKY_FINGER_PHALANX_PROXIMAL: Pinky finger phalanx proximal joint.
  - HAND_JOINT_PINKY_FINGER_PHALANX_INTERMEDIATE: Pinky finger phalanx intermediate joint.
  - HAND_JOINT_PINKY_FINGER_PHALANX_DISTAL: Pinky finger phalanx distal joint.
  - HAND_JOINT_PINKY_FINGER_TIP: Pinky finger tip joint.
  - HAND_JOINT_MAX: Represents the size of the `HandJoint` enum.
**HandJointFlags:** HAND_JOINT_FLAG_ORIENTATION_VALID=1, HAND_JOINT_FLAG_ORIENTATION_TRACKED=2, HAND_JOINT_FLAG_POSITION_VALID=4, HAND_JOINT_FLAG_POSITION_TRACKED=8, HAND_JOINT_FLAG_LINEAR_VELOCITY_VALID=16, HAND_JOINT_FLAG_ANGULAR_VELOCITY_VALID=32
  - HAND_JOINT_FLAG_ORIENTATION_VALID: The hand joint's orientation data is valid.
  - HAND_JOINT_FLAG_ORIENTATION_TRACKED: The hand joint's orientation is actively tracked. May not be set if tracking has been temporarily lost.
  - HAND_JOINT_FLAG_POSITION_VALID: The hand joint's position data is valid.
  - HAND_JOINT_FLAG_POSITION_TRACKED: The hand joint's position is actively tracked. May not be set if tracking has been temporarily lost.
  - HAND_JOINT_FLAG_LINEAR_VELOCITY_VALID: The hand joint's linear velocity data is valid.
  - HAND_JOINT_FLAG_ANGULAR_VELOCITY_VALID: The hand joint's angular velocity data is valid.

