## Area3D <- CollisionObject3D

Area3D is a region of 3D space defined by one or multiple CollisionShape3D or CollisionPolygon3D child nodes. It detects when other CollisionObject3Ds enter or exit it, and it also keeps track of which collision objects haven't exited it yet (i.e. which one are overlapping it). This node can also locally alter or override physics parameters (gravity, damping) and route audio to custom audio buses. **Note:** Areas and bodies created with PhysicsServer3D might not interact as expected with Area3Ds, and might not emit signals or track objects correctly. **Warning:** Using a ConcavePolygonShape3D inside a CollisionShape3D child of this node (created e.g. by using the **Create Trimesh Collision Sibling** option in the **Mesh** menu that appears when selecting a MeshInstance3D node) may give unexpected results, since this collision shape is hollow. If this is not desired, it has to be split into multiple ConvexPolygonShape3Ds or primitive shapes like BoxShape3D, or in some cases it may be replaceable by a CollisionPolygon3D.

**Props:**
- angular_damp: float = 0.1
- angular_damp_space_override: int (Area3D.SpaceOverride) = 0
- audio_bus_name: StringName = &"Master"
- audio_bus_override: bool = false
- gravity: float = 9.8
- gravity_direction: Vector3 = Vector3(0, -1, 0)
- gravity_point: bool = false
- gravity_point_center: Vector3 = Vector3(0, -1, 0)
- gravity_point_unit_distance: float = 0.0
- gravity_space_override: int (Area3D.SpaceOverride) = 0
- linear_damp: float = 0.1
- linear_damp_space_override: int (Area3D.SpaceOverride) = 0
- monitorable: bool = true
- monitoring: bool = true
- priority: int = 0
- reverb_bus_amount: float = 0.0
- reverb_bus_enabled: bool = false
- reverb_bus_name: StringName = &"Master"
- reverb_bus_uniformity: float = 0.0
- wind_attenuation_factor: float = 0.0
- wind_force_magnitude: float = 0.0
- wind_source_path: NodePath = NodePath("")

- **angular_damp**: The rate at which objects stop spinning in this area. Represents the angular velocity lost per second. See `ProjectSettings.physics/3d/default_angular_damp` for more details about damping.
- **angular_damp_space_override**: Override mode for angular damping calculations within this area.
- **audio_bus_name**: The name of the area's audio bus.
- **audio_bus_override**: If `true`, the area's audio bus overrides the default audio bus.
- **gravity**: The area's gravity intensity (in meters per second squared). This value multiplies the gravity direction. This is useful to alter the force of gravity without altering its direction.
- **gravity_direction**: The area's gravity vector (not normalized).
- **gravity_point**: If `true`, gravity is calculated from a point (set via `gravity_point_center`). See also `gravity_space_override`.
- **gravity_point_center**: If gravity is a point (see `gravity_point`), this will be the point of attraction.
- **gravity_point_unit_distance**: The distance at which the gravity strength is equal to `gravity`. For example, on a planet 100 meters in radius with a surface gravity of 4.0 m/s², set the `gravity` to 4.0 and the unit distance to 100.0. The gravity will have falloff according to the inverse square law, so in the example, at 200 meters from the center the gravity will be 1.0 m/s² (twice the distance, 1/4th the gravity), at 50 meters it will be 16.0 m/s² (half the distance, 4x the gravity), and so on. The above is true only when the unit distance is a positive number. When this is set to 0.0, the gravity will be constant regardless of distance.
- **gravity_space_override**: Override mode for gravity calculations within this area.
- **linear_damp**: The rate at which objects stop moving in this area. Represents the linear velocity lost per second. See `ProjectSettings.physics/3d/default_linear_damp` for more details about damping.
- **linear_damp_space_override**: Override mode for linear damping calculations within this area.
- **monitorable**: If `true`, other monitoring areas can detect this area.
- **monitoring**: If `true`, the area detects bodies or areas entering and exiting it.
- **priority**: The area's priority. Higher priority areas are processed first. The World3D's physics is always processed last, after all areas.
- **reverb_bus_amount**: The degree to which this area applies reverb to its associated audio. Ranges from `0` to `1` with `0.1` precision.
- **reverb_bus_enabled**: If `true`, the area applies reverb to its associated audio.
- **reverb_bus_name**: The name of the reverb bus to use for this area's associated audio.
- **reverb_bus_uniformity**: The degree to which this area's reverb is a uniform effect. Ranges from `0` to `1` with `0.1` precision.
- **wind_attenuation_factor**: The exponential rate at which wind force decreases with distance from its origin. **Note:** This wind force only applies to SoftBody3D nodes. Other physics bodies are currently not affected by wind.
- **wind_force_magnitude**: The magnitude of area-specific wind force. **Note:** This wind force only applies to SoftBody3D nodes. Other physics bodies are currently not affected by wind.
- **wind_source_path**: The Node3D which is used to specify the direction and origin of an area-specific wind force. The direction is opposite to the z-axis of the Node3D's local transform, and its origin is the origin of the Node3D's local transform. **Note:** This wind force only applies to SoftBody3D nodes. Other physics bodies are currently not affected by wind.

**Methods:**
- get_overlapping_areas() -> Area3D[] - Returns a list of intersecting Area3Ds. The overlapping area's `CollisionObject3D.collision_layer` must be part of this area's `CollisionObject3D.collision_mask` in order to be detected. For performance reasons (collisions are all processed at the same time) this list is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.
- get_overlapping_bodies() -> Node3D[] - Returns a list of intersecting PhysicsBody3Ds, SoftBody3Ds, and GridMaps. The overlapping body's `CollisionObject3D.collision_layer` must be part of this area's `CollisionObject3D.collision_mask` in order to be detected. For performance reasons (collisions are all processed at the same time) this list is modified once during the physics step, not immediately after objects are moved. Consider using signals instead. **Note:** Godot Physics does not support reporting overlaps with SoftBody3D, so will not return any such bodies.
- has_overlapping_areas() -> bool - Returns `true` if intersecting any Area3Ds, otherwise returns `false`. The overlapping area's `CollisionObject3D.collision_layer` must be part of this area's `CollisionObject3D.collision_mask` in order to be detected. For performance reasons (collisions are all processed at the same time) the list of overlapping areas is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.
- has_overlapping_bodies() -> bool - Returns `true` if intersecting any PhysicsBody3Ds, SoftBody3Ds, or GridMaps, otherwise returns `false`. The overlapping body's `CollisionObject3D.collision_layer` must be part of this area's `CollisionObject3D.collision_mask` in order to be detected. For performance reasons (collisions are all processed at the same time) the list of overlapping bodies is modified once during the physics step, not immediately after objects are moved. Consider using signals instead. **Note:** Godot Physics does not support reporting overlaps with SoftBody3D, so will not consider such bodies.
- overlaps_area(area: Node) -> bool - Returns `true` if the given Area3D intersects or overlaps this Area3D, `false` otherwise. **Note:** The result of this test is not immediate after moving objects. For performance, list of overlaps is updated once per frame and before the physics step. Consider using signals instead.
- overlaps_body(body: Node) -> bool - Returns `true` if the given physics body intersects or overlaps this Area3D, `false` otherwise. `body` argument can either be a PhysicsBody3D, SoftBody3D, or a GridMap instance. While GridMaps are not physics body themselves, they register their tiles with collision shapes as a virtual physics body. **Note:** The result of this test is not immediate after moving objects. For performance, list of overlaps is updated once per frame and before the physics step. Consider using signals instead. **Note:** Godot Physics does not support reporting overlaps with SoftBody3D, so will return `false` in such cases.

**Signals:**
- area_entered(area: Area3D) - Emitted when the received `area` enters this area. Requires `monitoring` to be set to `true`.
- area_exited(area: Area3D) - Emitted when the received `area` exits this area. Requires `monitoring` to be set to `true`.
- area_shape_entered(area_rid: RID, area: Area3D, area_shape_index: int, local_shape_index: int) - Emitted when a Shape3D of the received `area` enters a shape of this area. Requires `monitoring` to be set to `true`. `local_shape_index` and `area_shape_index` contain indices of the interacting shapes from this area and the other area, respectively. `area_rid` contains the RID of the other area. These values can be used with the PhysicsServer3D. **Example:** Get the CollisionShape3D node from the shape index:
- area_shape_exited(area_rid: RID, area: Area3D, area_shape_index: int, local_shape_index: int) - Emitted when a Shape3D of the received `area` exits a shape of this area. Requires `monitoring` to be set to `true`. See also `area_shape_entered`.
- body_entered(body: Node3D) - Emitted when the received `body` enters this area. `body` can be a PhysicsBody3D, SoftBody3D or GridMap. GridMaps are detected if their MeshLibrary has collision shapes configured. Requires `monitoring` to be set to `true`. **Note:** Godot Physics does not support reporting overlaps with SoftBody3D, so will not emit this signal in such cases.
- body_exited(body: Node3D) - Emitted when the received `body` exits this area. `body` can be a PhysicsBody3D, SoftBody3D or GridMap. GridMaps are detected if their MeshLibrary has collision shapes configured. Requires `monitoring` to be set to `true`. **Note:** Godot Physics does not support reporting overlaps with SoftBody3D, so will not emit this signal in such cases.
- body_shape_entered(body_rid: RID, body: Node3D, body_shape_index: int, local_shape_index: int) - Emitted when a Shape3D of the received `body` enters a shape of this area. `body` can be a PhysicsBody3D, SoftBody3D or GridMap. GridMaps are detected if their MeshLibrary has collision shapes configured. Requires `monitoring` to be set to `true`. `local_shape_index` and `body_shape_index` contain indices of the interacting shapes from this area and the interacting body, respectively. `body_rid` contains the RID of the body. These values can be used with the PhysicsServer3D. **Note:** Godot Physics does not support reporting overlaps with SoftBody3D, so will not emit this signal in such cases. **Example:** Get the CollisionShape3D node from the shape index:
- body_shape_exited(body_rid: RID, body: Node3D, body_shape_index: int, local_shape_index: int) - Emitted when a Shape3D of the received `body` exits a shape of this area. `body` can be a PhysicsBody3D, SoftBody3D or GridMap. GridMaps are detected if their MeshLibrary has collision shapes configured. Requires `monitoring` to be set to `true`. See also `body_shape_entered`. **Note:** Godot Physics does not support reporting overlaps with SoftBody3D, so will not emit this signal in such cases.

**Enums:**
**SpaceOverride:** SPACE_OVERRIDE_DISABLED=0, SPACE_OVERRIDE_COMBINE=1, SPACE_OVERRIDE_COMBINE_REPLACE=2, SPACE_OVERRIDE_REPLACE=3, SPACE_OVERRIDE_REPLACE_COMBINE=4
  - SPACE_OVERRIDE_DISABLED: This area does not affect gravity/damping.
  - SPACE_OVERRIDE_COMBINE: This area adds its gravity/damping values to whatever has been calculated so far (in `priority` order).
  - SPACE_OVERRIDE_COMBINE_REPLACE: This area adds its gravity/damping values to whatever has been calculated so far (in `priority` order), ignoring any lower priority areas.
  - SPACE_OVERRIDE_REPLACE: This area replaces any gravity/damping, even the defaults, ignoring any lower priority areas.
  - SPACE_OVERRIDE_REPLACE_COMBINE: This area replaces any gravity/damping calculated so far (in `priority` order), but keeps calculating the rest of the areas.

