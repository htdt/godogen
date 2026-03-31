## GodotInstance <- Object

GodotInstance represents a running Godot instance that is controlled from an outside codebase, without a perpetual main loop. It is created by the C API `libgodot_create_godot_instance`. Only one may be created per process.

**Methods:**
- focus_in() - Notifies the instance that it is now in focus.
- focus_out() - Notifies the instance that it is now not in focus.
- is_started() -> bool - Returns `true` if this instance has been fully started.
- iteration() -> bool - Runs a single iteration of the main loop. Returns `true` if the engine is attempting to quit.
- pause() - Notifies the instance that it is going to be paused.
- resume() - Notifies the instance that it is being resumed.
- start() -> bool - Finishes this instance's startup sequence. Returns `true` on success.

