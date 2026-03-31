## PhysicsTestMotionParameters2D <- RefCounted

By changing various properties of this object, such as the motion, you can configure the parameters for `PhysicsServer2D.body_test_motion`.

**Props:**
- collide_separation_ray: bool = false
- exclude_bodies: RID[] = []
- exclude_objects: int[] = []
- from: Transform2D = Transform2D(1, 0, 0, 1, 0, 0)
- margin: float = 0.08
- motion: Vector2 = Vector2(0, 0)
- recovery_as_collision: bool = false

- **collide_separation_ray**: If set to `true`, shapes of type `PhysicsServer2D.SHAPE_SEPARATION_RAY` are used to detect collisions and can stop the motion. Can be useful when snapping to the ground. If set to `false`, shapes of type `PhysicsServer2D.SHAPE_SEPARATION_RAY` are only used for separation when overlapping with other bodies. That's the main use for separation ray shapes.
- **exclude_bodies**: Optional array of body RID to exclude from collision. Use `CollisionObject2D.get_rid` to get the RID associated with a CollisionObject2D-derived node.
- **exclude_objects**: Optional array of object unique instance ID to exclude from collision. See `Object.get_instance_id`.
- **from**: Transform in global space where the motion should start. Usually set to `Node2D.global_transform` for the current body's transform.
- **margin**: Increases the size of the shapes involved in the collision detection.
- **motion**: Motion vector to define the length and direction of the motion to test.
- **recovery_as_collision**: If set to `true`, any depenetration from the recovery phase is reported as a collision; this is used e.g. by CharacterBody2D for improving floor detection during floor snapping. If set to `false`, only collisions resulting from the motion are reported, which is generally the desired behavior.

