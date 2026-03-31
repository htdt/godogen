## SpringBoneCollision3D <- Node3D

A collision can be a child of SpringBoneSimulator3D. If it is not a child of SpringBoneSimulator3D, it has no effect. The colliding and sliding are done in the SpringBoneSimulator3D's modification process in order of its collision list which is set by `SpringBoneSimulator3D.set_collision_path`. If `SpringBoneSimulator3D.are_all_child_collisions_enabled` is `true`, the order matches SceneTree. If `bone` is set, it synchronizes with the bone pose of the ancestor Skeleton3D, which is done in before the SpringBoneSimulator3D's modification process as the pre-process. **Warning:** A scaled SpringBoneCollision3D will likely not behave as expected. Make sure that the parent Skeleton3D and its bones are not scaled.

**Props:**
- bone: int = -1
- bone_name: String = ""
- position_offset: Vector3
- rotation_offset: Quaternion

- **bone**: The index of the attached bone.
- **bone_name**: The name of the attached bone.
- **position_offset**: The offset of the position from Skeleton3D's `bone` pose position.
- **rotation_offset**: The offset of the rotation from Skeleton3D's `bone` pose rotation.

**Methods:**
- get_skeleton() -> Skeleton3D - Get parent Skeleton3D node of the parent SpringBoneSimulator3D if found.

