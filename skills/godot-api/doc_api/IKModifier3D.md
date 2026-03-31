## IKModifier3D <- SkeletonModifier3D

Base class of SkeletonModifier3Ds that has some joint lists and applies inverse kinematics. This class has some structs, enums, and helper methods which are useful to solve inverse kinematics.

**Props:**
- mutable_bone_axes: bool = true

- **mutable_bone_axes**: If `true`, the solver retrieves the bone axis from the bone pose every frame. If `false`, the solver retrieves the bone axis from the bone rest and caches it, which increases performance slightly, but position changes in the bone pose made before processing this IKModifier3D are ignored.

**Methods:**
- clear_settings() - Clears all settings.
- get_setting_count() -> int - Returns the number of settings.
- reset() - Resets a state with respect to the current bone pose.
- set_setting_count(count: int) - Sets the number of settings.

