## SkeletonProfile <- Resource

This resource is used in EditorScenePostImport. Some parameters are referring to bones in Skeleton3D, Skin, Animation, and some other nodes are rewritten based on the parameters of SkeletonProfile. **Note:** These parameters need to be set only when creating a custom profile. In SkeletonProfileHumanoid, they are defined internally as read-only values.

**Props:**
- bone_size: int = 0
- group_size: int = 0
- root_bone: StringName = &""
- scale_base_bone: StringName = &""

- **bone_size**: The amount of bones in retargeting section's BoneMap editor. For example, SkeletonProfileHumanoid has 56 bones. The size of elements in BoneMap updates when changing this property in it's assigned SkeletonProfile.
- **group_size**: The amount of groups of bones in retargeting section's BoneMap editor. For example, SkeletonProfileHumanoid has 4 groups. This property exists to separate the bone list into several sections in the editor.
- **root_bone**: A bone name that will be used as the root bone in AnimationTree. This should be the bone of the parent of hips that exists at the world origin.
- **scale_base_bone**: A bone name which will use model's height as the coefficient for normalization. For example, SkeletonProfileHumanoid defines it as `Hips`.

**Methods:**
- find_bone(bone_name: StringName) -> int - Returns the bone index that matches `bone_name` as its name.
- get_bone_name(bone_idx: int) -> StringName - Returns the name of the bone at `bone_idx` that will be the key name in the BoneMap. In the retargeting process, the returned bone name is the bone name of the target skeleton.
- get_bone_parent(bone_idx: int) -> StringName - Returns the name of the bone which is the parent to the bone at `bone_idx`. The result is empty if the bone has no parent.
- get_bone_tail(bone_idx: int) -> StringName - Returns the name of the bone which is the tail of the bone at `bone_idx`.
- get_group(bone_idx: int) -> StringName - Returns the group of the bone at `bone_idx`.
- get_group_name(group_idx: int) -> StringName - Returns the name of the group at `group_idx` that will be the drawing group in the BoneMap editor.
- get_handle_offset(bone_idx: int) -> Vector2 - Returns the offset of the bone at `bone_idx` that will be the button position in the BoneMap editor. This is the offset with origin at the top left corner of the square.
- get_reference_pose(bone_idx: int) -> Transform3D - Returns the reference pose transform for bone `bone_idx`.
- get_tail_direction(bone_idx: int) -> int - Returns the tail direction of the bone at `bone_idx`.
- get_texture(group_idx: int) -> Texture2D - Returns the texture of the group at `group_idx` that will be the drawing group background image in the BoneMap editor.
- is_required(bone_idx: int) -> bool - Returns whether the bone at `bone_idx` is required for retargeting. This value is used by the bone map editor. If this method returns `true`, and no bone is assigned, the handle color will be red on the bone map editor.
- set_bone_name(bone_idx: int, bone_name: StringName) - Sets the name of the bone at `bone_idx` that will be the key name in the BoneMap. In the retargeting process, the setting bone name is the bone name of the target skeleton.
- set_bone_parent(bone_idx: int, bone_parent: StringName) - Sets the bone with name `bone_parent` as the parent of the bone at `bone_idx`. If an empty string is passed, then the bone has no parent.
- set_bone_tail(bone_idx: int, bone_tail: StringName) - Sets the bone with name `bone_tail` as the tail of the bone at `bone_idx`.
- set_group(bone_idx: int, group: StringName) - Sets the group of the bone at `bone_idx`.
- set_group_name(group_idx: int, group_name: StringName) - Sets the name of the group at `group_idx` that will be the drawing group in the BoneMap editor.
- set_handle_offset(bone_idx: int, handle_offset: Vector2) - Sets the offset of the bone at `bone_idx` that will be the button position in the BoneMap editor. This is the offset with origin at the top left corner of the square.
- set_reference_pose(bone_idx: int, bone_name: Transform3D) - Sets the reference pose transform for bone `bone_idx`.
- set_required(bone_idx: int, required: bool) - Sets the required status for bone `bone_idx` to `required`.
- set_tail_direction(bone_idx: int, tail_direction: int) - Sets the tail direction of the bone at `bone_idx`. **Note:** This only specifies the method of calculation. The actual coordinates required should be stored in an external skeleton, so the calculation itself needs to be done externally.
- set_texture(group_idx: int, texture: Texture2D) - Sets the texture of the group at `group_idx` that will be the drawing group background image in the BoneMap editor.

**Signals:**
- profile_updated - This signal is emitted when change the value in profile. This is used to update key name in the BoneMap and to redraw the BoneMap editor. **Note:** This signal is not connected directly to editor to simplify the reference, instead it is passed on to editor through the BoneMap.

**Enums:**
**TailDirection:** TAIL_DIRECTION_AVERAGE_CHILDREN=0, TAIL_DIRECTION_SPECIFIC_CHILD=1, TAIL_DIRECTION_END=2
  - TAIL_DIRECTION_AVERAGE_CHILDREN: Direction to the average coordinates of bone children.
  - TAIL_DIRECTION_SPECIFIC_CHILD: Direction to the coordinates of specified bone child.
  - TAIL_DIRECTION_END: Direction is not calculated.

