## PhysicsPointQueryParameters2D <- RefCounted

By changing various properties of this object, such as the point position, you can configure the parameters for `PhysicsDirectSpaceState2D.intersect_point`.

**Props:**
- canvas_instance_id: int = 0
- collide_with_areas: bool = false
- collide_with_bodies: bool = true
- collision_mask: int = 4294967295
- exclude: RID[] = []
- position: Vector2 = Vector2(0, 0)

- **canvas_instance_id**: If different from `0`, restricts the query to a specific canvas layer specified by its instance ID. See `Object.get_instance_id`. If `0`, restricts the query to the Viewport's default canvas layer.
- **collide_with_areas**: If `true`, the query will take Area2Ds into account.
- **collide_with_bodies**: If `true`, the query will take PhysicsBody2Ds into account.
- **collision_mask**: The physics layers the query will detect (as a bitmask). By default, all collision layers are detected. See in the documentation for more information.
- **exclude**: The list of object RIDs that will be excluded from collisions. Use `CollisionObject2D.get_rid` to get the RID associated with a CollisionObject2D-derived node. **Note:** The returned array is copied and any changes to it will not update the original property value. To update the value you need to modify the returned array, and then assign it to the property again.
- **position**: The position being queried for, in global coordinates.

