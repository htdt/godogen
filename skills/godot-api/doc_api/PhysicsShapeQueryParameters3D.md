## PhysicsShapeQueryParameters3D <- RefCounted

By changing various properties of this object, such as the shape, you can configure the parameters for PhysicsDirectSpaceState3D's methods.

**Props:**
- collide_with_areas: bool = false
- collide_with_bodies: bool = true
- collision_mask: int = 4294967295
- exclude: RID[] = []
- margin: float = 0.0
- motion: Vector3 = Vector3(0, 0, 0)
- shape: Resource
- shape_rid: RID = RID()
- transform: Transform3D = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)

- **collide_with_areas**: If `true`, the query will take Area3Ds into account.
- **collide_with_bodies**: If `true`, the query will take PhysicsBody3Ds into account.
- **collision_mask**: The physics layers the query will detect (as a bitmask). By default, all collision layers are detected. See in the documentation for more information.
- **exclude**: The list of object RIDs that will be excluded from collisions. Use `CollisionObject3D.get_rid` to get the RID associated with a CollisionObject3D-derived node. **Note:** The returned array is copied and any changes to it will not update the original property value. To update the value you need to modify the returned array, and then assign it to the property again.
- **margin**: The collision margin for the shape.
- **motion**: The motion of the shape being queried for.
- **shape**: The Shape3D that will be used for collision/intersection queries. This stores the actual reference which avoids the shape to be released while being used for queries, so always prefer using this over `shape_rid`.
- **shape_rid**: The queried shape's RID that will be used for collision/intersection queries. Use this over `shape` if you want to optimize for performance using the Servers API:
- **transform**: The queried shape's transform matrix.

