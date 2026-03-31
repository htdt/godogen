## SkeletonModification2DStackHolder <- SkeletonModification2D

This SkeletonModification2D holds a reference to a SkeletonModificationStack2D, allowing you to use multiple modification stacks on a single Skeleton2D. **Note:** The modifications in the held SkeletonModificationStack2D will only be executed if their execution mode matches the execution mode of the SkeletonModification2DStackHolder.

**Methods:**
- get_held_modification_stack() -> SkeletonModificationStack2D - Returns the SkeletonModificationStack2D that this modification is holding.
- set_held_modification_stack(held_modification_stack: SkeletonModificationStack2D) - Sets the SkeletonModificationStack2D that this modification is holding. This modification stack will then be executed when this modification is executed.

