## SpringArm3D <- Node3D

SpringArm3D casts a ray or a shape along its Z axis and moves all its direct children to the collision point, with an optional margin. This is useful for 3rd person cameras that move closer to the player when inside a tight space (you may need to exclude the player's collider from the SpringArm3D's collision check).

**Props:**
- collision_mask: int = 1
- margin: float = 0.01
- shape: Shape3D
- spring_length: float = 1.0

- **collision_mask**: The layers against which the collision check will be done. See in the documentation for more information.
- **margin**: When the collision check is made, a candidate length for the SpringArm3D is given. The margin is then subtracted to this length and the translation is applied to the child objects of the SpringArm3D. This margin is useful for when the SpringArm3D has a Camera3D as a child node: without the margin, the Camera3D would be placed on the exact point of collision, while with the margin the Camera3D would be placed close to the point of collision.
- **shape**: The Shape3D to use for the SpringArm3D. When the shape is set, the SpringArm3D will cast the Shape3D on its z axis instead of performing a ray cast.
- **spring_length**: The maximum extent of the SpringArm3D. This is used as a length for both the ray and the shape cast used internally to calculate the desired position of the SpringArm3D's child nodes. To know more about how to perform a shape cast or a ray cast, please consult the PhysicsDirectSpaceState3D documentation.

**Methods:**
- add_excluded_object(RID: RID) - Adds the PhysicsBody3D object with the given RID to the list of PhysicsBody3D objects excluded from the collision check.
- clear_excluded_objects() - Clears the list of PhysicsBody3D objects excluded from the collision check.
- get_hit_length() -> float - Returns the spring arm's current length.
- remove_excluded_object(RID: RID) -> bool - Removes the given RID from the list of PhysicsBody3D objects excluded from the collision check.

