## SkeletonModification2DPhysicalBones <- SkeletonModification2D

This modification takes the transforms of PhysicalBone2D nodes and applies them to Bone2D nodes. This allows the Bone2D nodes to react to physics thanks to the linked PhysicalBone2D nodes.

**Props:**
- physical_bone_chain_length: int = 0

- **physical_bone_chain_length**: The number of PhysicalBone2D nodes linked in this modification.

**Methods:**
- fetch_physical_bones() - Empties the list of PhysicalBone2D nodes and populates it with all PhysicalBone2D nodes that are children of the Skeleton2D.
- get_physical_bone_node(joint_idx: int) -> NodePath - Returns the PhysicalBone2D node at `joint_idx`.
- set_physical_bone_node(joint_idx: int, physicalbone2d_node: NodePath) - Sets the PhysicalBone2D node at `joint_idx`. **Note:** This is just the index used for this modification, not the bone index used in the Skeleton2D.
- start_simulation(bones: StringName[] = []) - Tell the PhysicalBone2D nodes to start simulating and interacting with the physics world. Optionally, an array of bone names can be passed to this function, and that will cause only PhysicalBone2D nodes with those names to start simulating.
- stop_simulation(bones: StringName[] = []) - Tell the PhysicalBone2D nodes to stop simulating and interacting with the physics world. Optionally, an array of bone names can be passed to this function, and that will cause only PhysicalBone2D nodes with those names to stop simulating.

