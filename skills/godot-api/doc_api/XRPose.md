## XRPose <- RefCounted

XR runtimes often identify multiple locations on devices such as controllers that are spatially tracked. Orientation, location, linear velocity and angular velocity are all provided for each pose by the XR runtime. This object contains this state of a pose.

**Props:**
- angular_velocity: Vector3 = Vector3(0, 0, 0)
- has_tracking_data: bool = false
- linear_velocity: Vector3 = Vector3(0, 0, 0)
- name: StringName = &""
- tracking_confidence: int (XRPose.TrackingConfidence) = 0
- transform: Transform3D = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)

- **angular_velocity**: The angular velocity for this pose.
- **has_tracking_data**: If `true` our tracking data is up to date. If `false` we're no longer receiving new tracking data and our state is whatever that last valid state was.
- **linear_velocity**: The linear velocity of this pose.
- **name**: The name of this pose. Usually, this name is derived from an action map set up by the user. Godot also suggests some pose names that XRInterface objects are expected to implement: - `root` is the root location, often used for tracked objects that do not have further nodes. - `aim` is the tip of a controller with its orientation pointing outwards, often used for raycasts. - `grip` is the location where the user grips the controller. - `skeleton` is the root location for a hand mesh, when using hand tracking and an animated skeleton is supplied by the XR runtime.
- **tracking_confidence**: The tracking confidence for this pose, provides insight on how accurate the spatial positioning of this record is.
- **transform**: The transform containing the original and transform as reported by the XR runtime.

**Methods:**
- get_adjusted_transform() -> Transform3D - Returns the `transform` with world scale and our reference frame applied. This is the transform used to position XRNode3D objects.

**Enums:**
**TrackingConfidence:** XR_TRACKING_CONFIDENCE_NONE=0, XR_TRACKING_CONFIDENCE_LOW=1, XR_TRACKING_CONFIDENCE_HIGH=2
  - XR_TRACKING_CONFIDENCE_NONE: No tracking information is available for this pose.
  - XR_TRACKING_CONFIDENCE_LOW: Tracking information may be inaccurate or estimated. For example, with inside out tracking this would indicate a controller may be (partially) obscured.
  - XR_TRACKING_CONFIDENCE_HIGH: Tracking information is considered accurate and up to date.

