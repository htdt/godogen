## PhysicalBoneSimulator3D <- SkeletonModifier3D

Node that can be the parent of PhysicalBone3D and can apply the simulation results to Skeleton3D.

**Methods:**
- is_simulating_physics() -> bool - Returns a boolean that indicates whether the PhysicalBoneSimulator3D is running and simulating.
- physical_bones_add_collision_exception(exception: RID) - Adds a collision exception to the physical bone. Works just like the RigidBody3D node.
- physical_bones_remove_collision_exception(exception: RID) - Removes a collision exception to the physical bone. Works just like the RigidBody3D node.
- physical_bones_start_simulation(bones: StringName[] = []) - Tells the PhysicalBone3D nodes in the Skeleton to start simulating and reacting to the physics world. Optionally, a list of bone names can be passed-in, allowing only the passed-in bones to be simulated.
- physical_bones_stop_simulation() - Tells the PhysicalBone3D nodes in the Skeleton to stop simulating.

