## Area2D <- CollisionObject2D

Area2D is a region of 2D space defined by one or multiple CollisionShape2D or CollisionPolygon2D child nodes. It detects when other CollisionObject2Ds enter or exit it, and it also keeps track of which collision objects haven't exited it yet (i.e. which one are overlapping it). This node can also locally alter or override physics parameters (gravity, damping) and route audio to custom audio buses. **Note:** Areas and bodies created with PhysicsServer2D might not interact as expected with Area2Ds, and might not emit signals or track objects correctly.

**Props:**
- angular_damp: float = 1.0
- angular_damp_space_override: int (Area2D.SpaceOverride) = 0
- audio_bus_name: StringName = &"Master"
- audio_bus_override: bool = false
- gravity: float = 980.0
- gravity_direction: Vector2 = Vector2(0, 1)
- gravity_point: bool = false
- gravity_point_center: Vector2 = Vector2(0, 1)
- gravity_point_unit_distance: float = 0.0
- gravity_space_override: int (Area2D.SpaceOverride) = 0
- linear_damp: float = 0.1
- linear_damp_space_override: int (Area2D.SpaceOverride) = 0
- monitorable: bool = true
- monitoring: bool = true
- priority: int = 0

- **angular_damp**: The rate at which objects stop spinning in this area. Represents the angular velocity lost per second. See `ProjectSettings.physics/2d/default_angular_damp` for more details about damping.
- **angular_damp_space_override**: Override mode for angular damping calculations within this area.
- **audio_bus_name**: The name of the area's audio bus.
- **audio_bus_override**: If `true`, the area's audio bus overrides the default audio bus.
- **gravity**: The area's gravity intensity (in pixels per second squared). This value multiplies the gravity direction. This is useful to alter the force of gravity without altering its direction.
- **gravity_direction**: The area's gravity vector (not normalized).
- **gravity_point**: If `true`, gravity is calculated from a point (set via `gravity_point_center`). See also `gravity_space_override`.
- **gravity_point_center**: If gravity is a point (see `gravity_point`), this will be the point of attraction.
- **gravity_point_unit_distance**: The distance at which the gravity strength is equal to `gravity`. For example, on a planet 100 pixels in radius with a surface gravity of 4.0 px/s², set the `gravity` to 4.0 and the unit distance to 100.0. The gravity will have falloff according to the inverse square law, so in the example, at 200 pixels from the center the gravity will be 1.0 px/s² (twice the distance, 1/4th the gravity), at 50 pixels it will be 16.0 px/s² (half the distance, 4x the gravity), and so on. The above is true only when the unit distance is a positive number. When this is set to 0.0, the gravity will be constant regardless of distance.
- **gravity_space_override**: Override mode for gravity calculations within this area.
- **linear_damp**: The rate at which objects stop moving in this area. Represents the linear velocity lost per second. See `ProjectSettings.physics/2d/default_linear_damp` for more details about damping.
- **linear_damp_space_override**: Override mode for linear damping calculations within this area.
- **monitorable**: If `true`, other monitoring areas can detect this area.
- **monitoring**: If `true`, the area detects bodies or areas entering and exiting it.
- **priority**: The area's priority. Higher priority areas are processed first. The World2D's physics is always processed last, after all areas.

**Methods:**
- get_overlapping_areas() -> Area2D[] - Returns a list of intersecting Area2Ds. The overlapping area's `CollisionObject2D.collision_layer` must be part of this area's `CollisionObject2D.collision_mask` in order to be detected. For performance reasons (collisions are all processed at the same time) this list is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.
- get_overlapping_bodies() -> Node2D[] - Returns a list of intersecting PhysicsBody2Ds and TileMaps. The overlapping body's `CollisionObject2D.collision_layer` must be part of this area's `CollisionObject2D.collision_mask` in order to be detected. For performance reasons (collisions are all processed at the same time) this list is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.
- has_overlapping_areas() -> bool - Returns `true` if intersecting any Area2Ds, otherwise returns `false`. The overlapping area's `CollisionObject2D.collision_layer` must be part of this area's `CollisionObject2D.collision_mask` in order to be detected. For performance reasons (collisions are all processed at the same time) the list of overlapping areas is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.
- has_overlapping_bodies() -> bool - Returns `true` if intersecting any PhysicsBody2Ds or TileMaps, otherwise returns `false`. The overlapping body's `CollisionObject2D.collision_layer` must be part of this area's `CollisionObject2D.collision_mask` in order to be detected. For performance reasons (collisions are all processed at the same time) the list of overlapping bodies is modified once during the physics step, not immediately after objects are moved. Consider using signals instead.
- overlaps_area(area: Node) -> bool - Returns `true` if the given Area2D intersects or overlaps this Area2D, `false` otherwise. **Note:** The result of this test is not immediate after moving objects. For performance, the list of overlaps is updated once per frame and before the physics step. Consider using signals instead.
- overlaps_body(body: Node) -> bool - Returns `true` if the given physics body intersects or overlaps this Area2D, `false` otherwise. **Note:** The result of this test is not immediate after moving objects. For performance, list of overlaps is updated once per frame and before the physics step. Consider using signals instead. The `body` argument can either be a PhysicsBody2D or a TileMap instance. While TileMaps are not physics bodies themselves, they register their tiles with collision shapes as a virtual physics body.

**Signals:**
- area_entered(area: Area2D) - Emitted when the received `area` enters this area. Requires `monitoring` to be set to `true`.
- area_exited(area: Area2D) - Emitted when the received `area` exits this area. Requires `monitoring` to be set to `true`.
- area_shape_entered(area_rid: RID, area: Area2D, area_shape_index: int, local_shape_index: int) - Emitted when a Shape2D of the received `area` enters a shape of this area. Requires `monitoring` to be set to `true`. `local_shape_index` and `area_shape_index` contain indices of the interacting shapes from this area and the other area, respectively. `area_rid` contains the RID of the other area. These values can be used with the PhysicsServer2D. **Example:** Get the CollisionShape2D node from the shape index:
- area_shape_exited(area_rid: RID, area: Area2D, area_shape_index: int, local_shape_index: int) - Emitted when a Shape2D of the received `area` exits a shape of this area. Requires `monitoring` to be set to `true`. See also `area_shape_entered`.
- body_entered(body: Node2D) - Emitted when the received `body` enters this area. `body` can be a PhysicsBody2D or a TileMap. TileMaps are detected if their TileSet has collision shapes configured. Requires `monitoring` to be set to `true`.
- body_exited(body: Node2D) - Emitted when the received `body` exits this area. `body` can be a PhysicsBody2D or a TileMap. TileMaps are detected if their TileSet has collision shapes configured. Requires `monitoring` to be set to `true`.
- body_shape_entered(body_rid: RID, body: Node2D, body_shape_index: int, local_shape_index: int) - Emitted when a Shape2D of the received `body` enters a shape of this area. `body` can be a PhysicsBody2D or a TileMap. TileMaps are detected if their TileSet has collision shapes configured. Requires `monitoring` to be set to `true`. `local_shape_index` and `body_shape_index` contain indices of the interacting shapes from this area and the interacting body, respectively. `body_rid` contains the RID of the body. These values can be used with the PhysicsServer2D. **Example:** Get the CollisionShape2D node from the shape index:
- body_shape_exited(body_rid: RID, body: Node2D, body_shape_index: int, local_shape_index: int) - Emitted when a Shape2D of the received `body` exits a shape of this area. `body` can be a PhysicsBody2D or a TileMap. TileMaps are detected if their TileSet has collision shapes configured. Requires `monitoring` to be set to `true`. See also `body_shape_entered`.

**Enums:**
**SpaceOverride:** SPACE_OVERRIDE_DISABLED=0, SPACE_OVERRIDE_COMBINE=1, SPACE_OVERRIDE_COMBINE_REPLACE=2, SPACE_OVERRIDE_REPLACE=3, SPACE_OVERRIDE_REPLACE_COMBINE=4
  - SPACE_OVERRIDE_DISABLED: This area does not affect gravity/damping.
  - SPACE_OVERRIDE_COMBINE: This area adds its gravity/damping values to whatever has been calculated so far (in `priority` order).
  - SPACE_OVERRIDE_COMBINE_REPLACE: This area adds its gravity/damping values to whatever has been calculated so far (in `priority` order), ignoring any lower priority areas.
  - SPACE_OVERRIDE_REPLACE: This area replaces any gravity/damping, even the defaults, ignoring any lower priority areas.
  - SPACE_OVERRIDE_REPLACE_COMBINE: This area replaces any gravity/damping calculated so far (in `priority` order), but keeps calculating the rest of the areas.

