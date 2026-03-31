## SplineIK3D <- ChainIK3D

A SkeletonModifier3D for aligning bones along a Path3D. The smoothness of the fitting depends on the `Curve3D.bake_interval`. If you want the Path3D to attach to a specific bone, it is recommended to place a ModifierBoneTarget3D before the SplineIK3D in the SkeletonModifier3D list (children of the Skeleton3D), and then place a Path3D as the ModifierBoneTarget3D's child. Bone twist is determined based on the `Curve3D.get_point_tilt`. If the root bone joint and the start point of the Curve3D are separated, it assumes that there is a linear line segment between them. This means that the vector pointing toward the start point of the Curve3D takes precedence over the shortest intersection point along the Curve3D. If the end bone joint exceeds the path length, it is bent as close as possible to the end point of the Curve3D. **Note:** All the methods in this class take an `index` parameter. This parameter specifies which setting list entry to return if the IK has multiple entries (e.g. `settings/<index>/root_bone_name`).

**Props:**
- setting_count: int = 0

- **setting_count**: The number of settings.

**Methods:**
- get_path_3d(index: int) -> NodePath - Returns the node path of the Path3D which is describing the path.
- get_tilt_fade_in(index: int) -> int - Returns the tilt interpolation method used between the root bone and the start point of the Curve3D when they are apart. See also `set_tilt_fade_in`.
- get_tilt_fade_out(index: int) -> int - Returns the tilt interpolation method used between the end bone and the end point of the Curve3D when they are apart. See also `set_tilt_fade_out`.
- is_tilt_enabled(index: int) -> bool - Returns if the tilt property of the Curve3D affects the bone twist.
- set_path_3d(index: int, path_3d: NodePath) - Sets the node path of the Path3D which is describing the path.
- set_tilt_enabled(index: int, enabled: bool) - Sets if the tilt property of the Curve3D should affect the bone twist.
- set_tilt_fade_in(index: int, size: int) - If `size` is greater than `0`, the tilt is interpolated between `size` start bones from the start point of the Curve3D when they are apart. If `size` is equal `0`, the tilts between the root bone head and the start point of the Curve3D are unified with a tilt of the start point of the Curve3D. If `size` is less than `0`, the tilts between the root bone and the start point of the Curve3D are `0.0`.
- set_tilt_fade_out(index: int, size: int) - If `size` is greater than `0`, the tilt is interpolated between `size` end bones from the end point of the Curve3D when they are apart. If `size` is equal `0`, the tilts between the end bone tail and the end point of the Curve3D are unified with a tilt of the end point of the Curve3D. If `size` is less than `0`, the tilts between the end bone and the end point of the Curve3D are `0.0`.

