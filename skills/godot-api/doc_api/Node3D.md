## Node3D <- Node

The Node3D node is the base representation of a node in 3D space. All other 3D nodes inherit from this class. Affine operations (translation, rotation, scale) are calculated in the coordinate system relative to the parent, unless the Node3D's `top_level` is `true`. In this coordinate system, affine operations correspond to direct affine operations on the Node3D's `transform`. The term *parent space* refers to this coordinate system. The coordinate system that is attached to the Node3D itself is referred to as object-local coordinate system, or *local space*. **Note:** Unless otherwise specified, all methods that need angle parameters must receive angles in *radians*. To convert degrees to radians, use `@GlobalScope.deg_to_rad`. **Note:** In Godot 3 and older, Node3D was named *Spatial*.

**Props:**
- basis: Basis
- global_basis: Basis
- global_position: Vector3
- global_rotation: Vector3
- global_rotation_degrees: Vector3
- global_transform: Transform3D
- position: Vector3 = Vector3(0, 0, 0)
- quaternion: Quaternion
- rotation: Vector3 = Vector3(0, 0, 0)
- rotation_degrees: Vector3
- rotation_edit_mode: int (Node3D.RotationEditMode) = 0
- rotation_order: int (EulerOrder) = 2
- scale: Vector3 = Vector3(1, 1, 1)
- top_level: bool = false
- transform: Transform3D = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)
- visibility_parent: NodePath = NodePath("")
- visible: bool = true

- **basis**: Basis of the `transform` property. Represents the rotation, scale, and shear of this node in parent space (relative to the parent node).
- **global_basis**: Basis of the `global_transform` property. Represents the rotation, scale, and shear of this node in global space (relative to the world). **Note:** If the node is not inside the tree, getting this property fails and returns `Basis.IDENTITY`.
- **global_position**: Global position (translation) of this node in global space (relative to the world). This is equivalent to the `global_transform`'s `Transform3D.origin`. **Note:** If the node is not inside the tree, getting this property fails and returns `Vector3.ZERO`.
- **global_rotation**: Global rotation of this node as , in radians and in global space (relative to the world). This value is obtained from `global_basis`'s rotation. - The `Vector3.x` is the angle around the global X axis (pitch); - The `Vector3.y` is the angle around the global Y axis (yaw); - The `Vector3.z` is the angle around the global Z axis (roll). **Note:** Unlike `rotation`, this property always follows the YXZ convention (`EULER_ORDER_YXZ`). **Note:** If the node is not inside the tree, getting this property fails and returns `Vector3.ZERO`.
- **global_rotation_degrees**: The `global_rotation` of this node, in degrees instead of radians. **Note:** If the node is not inside the tree, getting this property fails and returns `Vector3.ZERO`.
- **global_transform**: The transformation of this node, in global space (relative to the world). Contains and represents this node's `global_position`, `global_rotation`, and global scale. **Note:** If the node is not inside the tree, getting this property fails and returns `Transform3D.IDENTITY`.
- **position**: Position (translation) of this node in parent space (relative to the parent node). This is equivalent to the `transform`'s `Transform3D.origin`.
- **quaternion**: Rotation of this node represented as a Quaternion in parent space (relative to the parent node). This value is obtained from `basis`'s rotation. **Note:** Quaternions are much more suitable for 3D math but are less intuitive. Setting this property can be useful for interpolation (see `Quaternion.slerp`).
- **rotation**: Rotation of this node as , in radians and in parent space (relative to the parent node). This value is obtained from `basis`'s rotation. - The `Vector3.x` is the angle around the local X axis (pitch); - The `Vector3.y` is the angle around the local Y axis (yaw); - The `Vector3.z` is the angle around the local Z axis (roll). The order of each consecutive rotation can be changed with `rotation_order` (see `EulerOrder` constants). By default, the YXZ convention is used (`EULER_ORDER_YXZ`). **Note:** This property is edited in degrees in the inspector. If you want to use degrees in a script, use `rotation_degrees`.
- **rotation_degrees**: The `rotation` of this node, in degrees instead of radians. **Note:** This is **not** the property available in the Inspector dock.
- **rotation_edit_mode**: How this node's rotation and scale are displayed in the Inspector dock.
- **rotation_order**: The axis rotation order of the `rotation` property. The final orientation is calculated by rotating around the local X, Y, and Z axis in this order.
- **scale**: Scale of this node in local space (relative to this node). This value is obtained from `basis`'s scale. **Note:** The behavior of some 3D node types is not affected by this property. These include Light3D, Camera3D, AudioStreamPlayer3D, and more. **Warning:** The scale's components must either be all positive or all negative, and **not** exactly `0.0`. Otherwise, it won't be possible to obtain the scale from the `basis`. This may cause the intended scale to be lost when reloaded from disk, and potentially other unstable behavior.
- **top_level**: If `true`, the node does not inherit its transformations from its parent. As such, node transformations will only be in global space, which also means that `global_transform` and `transform` will be identical.
- **transform**: The local transformation of this node, in parent space (relative to the parent node). Contains and represents this node's `position`, `rotation`, and `scale`.
- **visibility_parent**: Path to the visibility range parent for this node and its descendants. The visibility parent must be a GeometryInstance3D. Any visual instance will only be visible if the visibility parent (and all of its visibility ancestors) is hidden by being closer to the camera than its own `GeometryInstance3D.visibility_range_begin`. Nodes hidden via the `Node3D.visible` property are essentially removed from the visibility dependency tree, so dependent instances will not take the hidden node or its descendants into account.
- **visible**: If `true`, this node can be visible. The node is only rendered when all of its ancestors are visible, as well. That means `is_visible_in_tree` must return `true`.

**Methods:**
- add_gizmo(gizmo: Node3DGizmo) - Attaches the given `gizmo` to this node. Only works in the editor. **Note:** `gizmo` should be an EditorNode3DGizmo. The argument type is Node3DGizmo to avoid depending on editor classes in Node3D.
- clear_gizmos() - Clears all EditorNode3DGizmo objects attached to this node. Only works in the editor.
- clear_subgizmo_selection() - Deselects all subgizmos for this node. Useful to call when the selected subgizmo may no longer exist after a property change. Only works in the editor.
- force_update_transform() - Forces the node's `global_transform` to update, by sending `NOTIFICATION_TRANSFORM_CHANGED`. Fails if the node is not inside the tree. **Note:** For performance reasons, transform changes are usually accumulated and applied *once* at the end of the frame. The update propagates through Node3D children, as well. Therefore, use this method only when you need an up-to-date transform (such as during physics operations).
- get_gizmos() -> Node3DGizmo[] - Returns all the EditorNode3DGizmo objects attached to this node. Only works in the editor.
- get_global_transform_interpolated() -> Transform3D - When using physics interpolation, there will be circumstances in which you want to know the interpolated (displayed) transform of a node rather than the standard transform (which may only be accurate to the most recent physics tick). This is particularly important for frame-based operations that take place in `Node._process`, rather than `Node._physics_process`. Examples include Camera3Ds focusing on a node, or finding where to fire lasers from on a frame rather than physics tick. **Note:** This function creates an interpolation pump on the Node3D the first time it is called, which can respond to physics interpolation resets. If you get problems with "streaking" when initially following a Node3D, be sure to call `get_global_transform_interpolated` at least once *before* resetting the Node3D physics interpolation.
- get_parent_node_3d() -> Node3D - Returns the parent Node3D that directly affects this node's `global_transform`. Returns `null` if no parent exists, the parent is not a Node3D, or `top_level` is `true`. **Note:** This method is not always equivalent to `Node.get_parent`, which does not take `top_level` into account.
- get_world_3d() -> World3D - Returns the World3D this node is registered to. Usually, this is the same as the world used by this node's viewport (see `Node.get_viewport` and `Viewport.find_world_3d`).
- global_rotate(axis: Vector3, angle: float) - Rotates this node's `global_basis` around the global `axis` by the given `angle`, in radians. This operation is calculated in global space (relative to the world) and preserves the `global_position`.
- global_scale(scale: Vector3) - Scales this node's `global_basis` by the given `scale` factor. This operation is calculated in global space (relative to the world) and preserves the `global_position`. **Note:** This method is not to be confused with the `scale` property.
- global_translate(offset: Vector3) - Adds the given translation `offset` to the node's `global_position` in global space (relative to the world).
- hide() - Prevents this node from being rendered. Equivalent to setting `visible` to `false`. This is the opposite of `show`.
- is_local_transform_notification_enabled() -> bool - Returns `true` if the node receives `NOTIFICATION_LOCAL_TRANSFORM_CHANGED` whenever `transform` changes. This is enabled with `set_notify_local_transform`.
- is_scale_disabled() -> bool - Returns `true` if this node's `global_transform` is automatically orthonormalized. This results in this node not appearing distorted, as if its global scale were set to `Vector3.ONE` (or its negative counterpart). See also `set_disable_scale` and `orthonormalize`. **Note:** `transform` is not affected by this setting.
- is_transform_notification_enabled() -> bool - Returns `true` if the node receives `NOTIFICATION_TRANSFORM_CHANGED` whenever `global_transform` changes. This is enabled with `set_notify_transform`.
- is_visible_in_tree() -> bool - Returns `true` if this node is inside the scene tree and the `visible` property is `true` for this node and all of its Node3D ancestors *in sequence*. An ancestor of any other type (such as Node or Node2D) breaks the sequence. See also `Node.get_parent`. **Note:** This method cannot take `VisualInstance3D.layers` into account, so even if this method returns `true`, the node may not be rendered.
- look_at(target: Vector3, up: Vector3 = Vector3(0, 1, 0), use_model_front: bool = false) - Rotates the node so that the local forward axis (-Z, `Vector3.FORWARD`) points toward the `target` position. This operation is calculated in global space (relative to the world). The local up axis (+Y) points as close to the `up` vector as possible while staying perpendicular to the local forward axis. The resulting transform is orthogonal, and the scale is preserved. Non-uniform scaling may not work correctly. The `target` position cannot be the same as the node's position, the `up` vector cannot be `Vector3.ZERO`. Furthermore, the direction from the node's position to the `target` position cannot be parallel to the `up` vector, to avoid an unintended rotation around the local Z axis. If `use_model_front` is `true`, the +Z axis (asset front) is treated as forward (implies +X is left) and points toward the `target` position. By default, the -Z axis (camera forward) is treated as forward (implies +X is right). **Note:** This method fails if the node is not in the scene tree. If necessary, use `look_at_from_position` instead.
- look_at_from_position(position: Vector3, target: Vector3, up: Vector3 = Vector3(0, 1, 0), use_model_front: bool = false) - Moves the node to the specified `position`, then rotates the node to point toward the `target` position, similar to `look_at`. This operation is calculated in global space (relative to the world).
- orthonormalize() - Orthonormalizes this node's `basis`. This method sets this node's `scale` to `Vector3.ONE` (or its negative counterpart), but preserves the `position` and `rotation`. See also `Transform3D.orthonormalized`.
- rotate(axis: Vector3, angle: float) - Rotates this node's `basis` around the `axis` by the given `angle`, in radians. This operation is calculated in parent space (relative to the parent) and preserves the `position`.
- rotate_object_local(axis: Vector3, angle: float) - Rotates this node's `basis` around the `axis` by the given `angle`, in radians. This operation is calculated in local space (relative to this node) and preserves the `position`.
- rotate_x(angle: float) - Rotates this node's `basis` around the X axis by the given `angle`, in radians. This operation is calculated in parent space (relative to the parent) and preserves the `position`.
- rotate_y(angle: float) - Rotates this node's `basis` around the Y axis by the given `angle`, in radians. This operation is calculated in parent space (relative to the parent) and preserves the `position`.
- rotate_z(angle: float) - Rotates this node's `basis` around the Z axis by the given `angle`, in radians. This operation is calculated in parent space (relative to the parent) and preserves the `position`.
- scale_object_local(scale: Vector3) - Scales this node's `basis` by the given `scale` factor. This operation is calculated in local space (relative to this node) and preserves the `position`.
- set_disable_scale(disable: bool) - If `true`, this node's `global_transform` is automatically orthonormalized. This results in this node not appearing distorted, as if its global scale were set to `Vector3.ONE` (or its negative counterpart). See also `is_scale_disabled` and `orthonormalize`. **Note:** `transform` is not affected by this setting.
- set_identity() - Sets this node's `transform` to `Transform3D.IDENTITY`, which resets all transformations in parent space (`position`, `rotation`, and `scale`).
- set_ignore_transform_notification(enabled: bool) - If `true`, the node will not receive `NOTIFICATION_TRANSFORM_CHANGED` or `NOTIFICATION_LOCAL_TRANSFORM_CHANGED`. It may useful to call this method when handling these notifications to prevent infinite recursion.
- set_notify_local_transform(enable: bool) - If `true`, the node will receive `NOTIFICATION_LOCAL_TRANSFORM_CHANGED` whenever `transform` changes. **Note:** Some 3D nodes such as CSGShape3D or CollisionShape3D automatically enable this to function correctly.
- set_notify_transform(enable: bool) - If `true`, the node will receive `NOTIFICATION_TRANSFORM_CHANGED` whenever `global_transform` changes. **Note:** Most 3D nodes such as VisualInstance3D or CollisionObject3D automatically enable this to function correctly. **Note:** In the editor, nodes will propagate this notification to their children if a gizmo is attached (see `add_gizmo`).
- set_subgizmo_selection(gizmo: Node3DGizmo, id: int, transform: Transform3D) - Selects the `gizmo`'s subgizmo with the given `id` and sets its transform. Only works in the editor. **Note:** The gizmo object would typically be an instance of EditorNode3DGizmo, but the argument type is kept generic to avoid creating a dependency on editor classes in Node3D.
- show() - Allows this node to be rendered. Equivalent to setting `visible` to `true`. This is the opposite of `hide`.
- to_global(local_point: Vector3) -> Vector3 - Returns the `local_point` converted from this node's local space to global space. This is the opposite of `to_local`.
- to_local(global_point: Vector3) -> Vector3 - Returns the `global_point` converted from global space to this node's local space. This is the opposite of `to_global`.
- translate(offset: Vector3) - Adds the given translation `offset` to the node's position, in local space (relative to this node). **Note:** Prefer using `translate_object_local`, instead, as this method may be changed in a future release. **Note:** Despite the naming convention, this operation is **not** calculated in parent space for compatibility reasons. To translate in parent space, add `offset` to the `position` (`node_3d.position += offset`).
- translate_object_local(offset: Vector3) - Adds the given translation `offset` to the node's position, in local space (relative to this node).
- update_gizmos() - Updates all the EditorNode3DGizmo objects attached to this node. Only works in the editor.

**Signals:**
- visibility_changed - Emitted when this node's visibility changes (see `visible` and `is_visible_in_tree`). This signal is emitted *after* the related `NOTIFICATION_VISIBILITY_CHANGED` notification.

**Enums:**
**Constants:** NOTIFICATION_TRANSFORM_CHANGED=2000, NOTIFICATION_ENTER_WORLD=41, NOTIFICATION_EXIT_WORLD=42, NOTIFICATION_VISIBILITY_CHANGED=43, NOTIFICATION_LOCAL_TRANSFORM_CHANGED=44
  - NOTIFICATION_TRANSFORM_CHANGED: Notification received when this node's `global_transform` changes, if `is_transform_notification_enabled` is `true`. See also `set_notify_transform`. **Note:** Most 3D nodes such as VisualInstance3D or CollisionObject3D automatically enable this to function correctly. **Note:** In the editor, nodes will propagate this notification to their children if a gizmo is attached (see `add_gizmo`).
  - NOTIFICATION_ENTER_WORLD: Notification received when this node is registered to a new World3D (see `get_world_3d`).
  - NOTIFICATION_EXIT_WORLD: Notification received when this node is unregistered from the current World3D (see `get_world_3d`). This notification is sent in reversed order.
  - NOTIFICATION_VISIBILITY_CHANGED: Notification received when this node's visibility changes (see `visible` and `is_visible_in_tree`). This notification is received *before* the related `visibility_changed` signal.
  - NOTIFICATION_LOCAL_TRANSFORM_CHANGED: Notification received when this node's `transform` changes, if `is_local_transform_notification_enabled` is `true`. This is not received when a parent Node3D's `transform` changes. See also `set_notify_local_transform`. **Note:** Some 3D nodes such as CSGShape3D or CollisionShape3D automatically enable this to function correctly.
**RotationEditMode:** ROTATION_EDIT_MODE_EULER=0, ROTATION_EDIT_MODE_QUATERNION=1, ROTATION_EDIT_MODE_BASIS=2
  - ROTATION_EDIT_MODE_EULER: The rotation is edited using a Vector3 in .
  - ROTATION_EDIT_MODE_QUATERNION: The rotation is edited using a Quaternion.
  - ROTATION_EDIT_MODE_BASIS: The rotation is edited using a Basis. In this mode, the raw `basis`'s axes can be freely modified, but the `scale` property is not available.

