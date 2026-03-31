## UndoRedo <- Object

UndoRedo works by registering methods and property changes inside "actions". You can create an action, then provide ways to do and undo this action using function calls and property changes, then commit the action. When an action is committed, all of the `do_*` methods will run. If the `undo` method is used, the `undo_*` methods will run. If the `redo` method is used, once again, all of the `do_*` methods will run. Here's an example on how to add an action: Before calling any of the `add_(un)do_*` methods, you need to first call `create_action`. Afterwards you need to call `commit_action`. If you don't need to register a method, you can leave `add_do_method` and `add_undo_method` out; the same goes for properties. You can also register more than one method/property. If you are making an EditorPlugin and want to integrate into the editor's undo history, use EditorUndoRedoManager instead. If you are registering multiple properties/method which depend on one another, be aware that by default undo operation are called in the same order they have been added. Therefore instead of grouping do operation with their undo operations it is better to group do on one side and undo on the other as shown below.

**Props:**
- max_steps: int = 0

- **max_steps**: The maximum number of steps that can be stored in the undo/redo history. If the number of stored steps exceeds this limit, older steps are removed from history and can no longer be reached by calling `undo`. A value of `0` or lower means no limit.

**Methods:**
- add_do_method(callable: Callable) - Register a Callable that will be called when the action is committed.
- add_do_property(object: Object, property: StringName, value: Variant) - Register a `property` that would change its value to `value` when the action is committed.
- add_do_reference(object: Object) - Register a reference to an object that will be erased if the "do" history is deleted. This is useful for objects added by the "do" action and removed by the "undo" action. When the "do" history is deleted, if the object is a RefCounted, it will be unreferenced. Otherwise, it will be freed. Do not use for resources.
- add_undo_method(callable: Callable) - Register a Callable that will be called when the action is undone.
- add_undo_property(object: Object, property: StringName, value: Variant) - Register a `property` that would change its value to `value` when the action is undone.
- add_undo_reference(object: Object) - Register a reference to an object that will be erased if the "undo" history is deleted. This is useful for objects added by the "undo" action and removed by the "do" action. When the "undo" history is deleted, if the object is a RefCounted, it will be unreferenced. Otherwise, it will be freed. Do not use for resources.
- clear_history(increase_version: bool = true) - Clear the undo/redo history and associated references. Passing `false` to `increase_version` will prevent the version number from increasing when the history is cleared.
- commit_action(execute: bool = true) - Commit the action. If `execute` is `true` (which it is by default), all "do" methods/properties are called/set when this function is called.
- create_action(name: String, merge_mode: int = 0, backward_undo_ops: bool = false) - Create a new action. After this is called, do all your calls to `add_do_method`, `add_undo_method`, `add_do_property`, and `add_undo_property`, then commit the action with `commit_action`. The way actions are merged is dictated by `merge_mode`. The way undo operation are ordered in actions is dictated by `backward_undo_ops`. When `backward_undo_ops` is `false` undo option are ordered in the same order they were added. Which means the first operation to be added will be the first to be undone.
- end_force_keep_in_merge_ends() - Stops marking operations as to be processed even if the action gets merged with another in the `MERGE_ENDS` mode. See `start_force_keep_in_merge_ends`.
- get_action_name(id: int) -> String - Gets the action name from its index.
- get_current_action() -> int - Gets the index of the current action.
- get_current_action_name() -> String - Gets the name of the current action, equivalent to `get_action_name(get_current_action())`.
- get_history_count() -> int - Returns how many elements are in the history.
- get_version() -> int - Gets the version. Every time a new action is committed, the UndoRedo's version number is increased automatically. This is useful mostly to check if something changed from a saved version.
- has_redo() -> bool - Returns `true` if a "redo" action is available.
- has_undo() -> bool - Returns `true` if an "undo" action is available.
- is_committing_action() -> bool - Returns `true` if the UndoRedo is currently committing the action, i.e. running its "do" method or property change (see `commit_action`).
- redo() -> bool - Redo the last action.
- start_force_keep_in_merge_ends() - Marks the next "do" and "undo" operations to be processed even if the action gets merged with another in the `MERGE_ENDS` mode. Return to normal operation using `end_force_keep_in_merge_ends`.
- undo() -> bool - Undo the last action.

**Signals:**
- version_changed - Called when `undo` or `redo` was called.

**Enums:**
**MergeMode:** MERGE_DISABLE=0, MERGE_ENDS=1, MERGE_ALL=2
  - MERGE_DISABLE: Makes "do"/"undo" operations stay in separate actions.
  - MERGE_ENDS: Merges this action with the previous one if they have the same name. Keeps only the first action's "undo" operations and the last action's "do" operations. Useful for sequential changes to a single value.
  - MERGE_ALL: Merges this action with the previous one if they have the same name.

