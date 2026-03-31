## FoldableGroup <- Resource

A group of FoldableContainer-derived nodes. Only one container can be expanded at a time.

**Props:**
- allow_folding_all: bool = false
- resource_local_to_scene: bool = true

- **allow_folding_all**: If `true`, it is possible to fold all containers in this FoldableGroup.

**Methods:**
- get_containers() -> FoldableContainer[] - Returns an Array of FoldableContainers that have this as their FoldableGroup (see `FoldableContainer.foldable_group`). This is equivalent to ButtonGroup but for FoldableContainers.
- get_expanded_container() -> FoldableContainer - Returns the current expanded container.

**Signals:**
- expanded(container: FoldableContainer) - Emitted when one of the containers of the group is expanded.

