## BoneConstraint3D <- SkeletonModifier3D

Base class of SkeletonModifier3D that modifies the bone set in `set_apply_bone` based on the transform of the bone retrieved by `get_reference_bone`. **Note:** Most methods in this class take an `index` parameter. This parameter specifies which setting list entry to return if the IK has multiple entries (e.g. `settings/<index>/amount`).

**Methods:**
- clear_setting() - Clear all settings.
- get_amount(index: int) -> float - Returns the apply amount of the setting at `index`.
- get_apply_bone(index: int) -> int - Returns the apply bone of the setting at `index`. This bone will be modified.
- get_apply_bone_name(index: int) -> String - Returns the apply bone name of the setting at `index`. This bone will be modified.
- get_reference_bone(index: int) -> int - Returns the reference bone of the setting at `index`. This bone will be only referenced and not modified by this modifier.
- get_reference_bone_name(index: int) -> String - Returns the reference bone name of the setting at `index`. This bone will be only referenced and not modified by this modifier.
- get_reference_node(index: int) -> NodePath - Returns the reference node path of the setting at `index`. This node will be only referenced and not modified by this modifier.
- get_reference_type(index: int) -> int - Returns the reference target type of the setting at `index`. See also `ReferenceType`.
- get_setting_count() -> int - Returns the number of settings in the modifier.
- set_amount(index: int, amount: float) - Sets the apply amount of the setting at `index` to `amount`.
- set_apply_bone(index: int, bone: int) - Sets the apply bone of the setting at `index` to `bone`. This bone will be modified.
- set_apply_bone_name(index: int, bone_name: String) - Sets the apply bone of the setting at `index` to `bone_name`. This bone will be modified.
- set_reference_bone(index: int, bone: int) - Sets the reference bone of the setting at `index` to `bone`. This bone will be only referenced and not modified by this modifier.
- set_reference_bone_name(index: int, bone_name: String) - Sets the reference bone of the setting at `index` to `bone_name`. This bone will be only referenced and not modified by this modifier.
- set_reference_node(index: int, node: NodePath) - Sets the reference node path of the setting at `index` to `node`. This node will be only referenced and not modified by this modifier.
- set_reference_type(index: int, type: int) - Sets the reference target type of the setting at `index` to `type`. See also `ReferenceType`.
- set_setting_count(count: int) - Sets the number of settings in the modifier.

**Enums:**
**ReferenceType:** REFERENCE_TYPE_BONE=0, REFERENCE_TYPE_NODE=1
  - REFERENCE_TYPE_BONE: The reference target is a bone. In this case, the reference target spaces is local space.
  - REFERENCE_TYPE_NODE: The reference target is a Node3D. In this case, the reference target spaces is model space. In other words, the reference target's coordinates are treated as if it were placed directly under Skeleton3D which parent of the BoneConstraint3D.

