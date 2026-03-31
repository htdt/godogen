## PhysicsPointQueryParameters3D <- RefCounted

By changing various properties of this object, such as the point position, you can configure the parameters for `PhysicsDirectSpaceState3D.intersect_point`.

**Props:**
- collide_with_areas: bool = false
- collide_with_bodies: bool = true
- collision_mask: int = 4294967295
- exclude: RID[] = []
- position: Vector3 = Vector3(0, 0, 0)

- **collide_with_areas**: If `true`, the query will take Area3Ds into account.
- **collide_with_bodies**: If `true`, the query will take PhysicsBody3Ds into account.
- **collision_mask**: The physics layers the query will detect (as a bitmask). By default, all collision layers are detected. See in the documentation for more information.
- **exclude**: The list of object RIDs that will be excluded from collisions. Use `CollisionObject3D.get_rid` to get the RID associated with a CollisionObject3D-derived node. **Note:** The returned array is copied and any changes to it will not update the original property value. To update the value you need to modify the returned array, and then assign it to the property again.
- **position**: The position being queried for, in global coordinates.

