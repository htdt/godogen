## AnimationLibrary <- Resource

An animation library stores a set of animations accessible through StringName keys, for use with AnimationPlayer nodes.

**Methods:**
- add_animation(name: StringName, animation: Animation) -> int - Adds the `animation` to the library, accessible by the key `name`.
- get_animation(name: StringName) -> Animation - Returns the Animation with the key `name`. If the animation does not exist, `null` is returned and an error is logged.
- get_animation_list() -> StringName[] - Returns the keys for the Animations stored in the library.
- get_animation_list_size() -> int - Returns the key count for the Animations stored in the library.
- has_animation(name: StringName) -> bool - Returns `true` if the library stores an Animation with `name` as the key.
- remove_animation(name: StringName) - Removes the Animation with the key `name`.
- rename_animation(name: StringName, newname: StringName) - Changes the key of the Animation associated with the key `name` to `newname`.

**Signals:**
- animation_added(name: StringName) - Emitted when an Animation is added, under the key `name`.
- animation_changed(name: StringName) - Emitted when there's a change in one of the animations, e.g. tracks are added, moved or have changed paths. `name` is the key of the animation that was changed. See also `Resource.changed`, which this acts as a relay for.
- animation_removed(name: StringName) - Emitted when an Animation stored with the key `name` is removed.
- animation_renamed(name: StringName, to_name: StringName) - Emitted when the key for an Animation is changed, from `name` to `to_name`.

