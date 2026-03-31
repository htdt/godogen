## SceneTreeTimer <- RefCounted

A one-shot timer managed by the scene tree, which emits `timeout` on completion. See also `SceneTree.create_timer`. As opposed to Timer, it does not require the instantiation of a node. Commonly used to create a one-shot delay timer as in the following example: The timer will be dereferenced after its time elapses. To preserve the timer, you can keep a reference to it. See RefCounted. **Note:** The timer is processed after all of the nodes in the current frame, i.e. node's `Node._process` method would be called before the timer (or `Node._physics_process` if `process_in_physics` in `SceneTree.create_timer` has been set to `true`).

**Props:**
- time_left: float

- **time_left**: The time remaining (in seconds).

**Signals:**
- timeout - Emitted when the timer reaches 0.

