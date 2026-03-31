## Logger <- RefCounted

Custom logger to receive messages from the internal error/warning stream. Loggers are registered via `OS.add_logger`.

**Methods:**
- _log_error(function: String, file: String, line: int, code: String, rationale: String, editor_notify: bool, error_type: int, script_backtraces: ScriptBacktrace[]) - Called when an error is logged. The error provides the `function`, `file`, and `line` that it originated from, as well as either the `code` that generated the error or a `rationale`. The type of error provided by `error_type` is described in the `ErrorType` enumeration. Additionally, `script_backtraces` provides backtraces for each of the script languages. These will only contain stack frames in editor builds and debug builds by default. To enable them for release builds as well, you need to enable `ProjectSettings.debug/settings/gdscript/always_track_call_stacks`. **Warning:** This method will be called from threads other than the main thread, possibly at the same time, so you will need to have some kind of thread-safety in your implementation of it, like a Mutex. **Note:** `script_backtraces` will not contain any captured variables, due to its prohibitively high cost. To get those, you will need to capture the backtraces yourself, from within the Logger virtual methods, using `Engine.capture_script_backtraces`. **Note:** Logging errors from this method using functions like `@GlobalScope.push_error` or `@GlobalScope.push_warning` is not supported, as it could cause infinite recursion. These errors will only show up in the console output.
- _log_message(message: String, error: bool) - Called when a message is logged. If `error` is `true`, then this message was meant to be sent to `stderr`. **Warning:** This method will be called from threads other than the main thread, possibly at the same time, so you will need to have some kind of thread-safety in your implementation of it, like a Mutex. **Note:** Logging another message from this method using functions like `@GlobalScope.print` is not supported, as it could cause infinite recursion. These messages will only show up in the console output.

**Enums:**
**ErrorType:** ERROR_TYPE_ERROR=0, ERROR_TYPE_WARNING=1, ERROR_TYPE_SCRIPT=2, ERROR_TYPE_SHADER=3
  - ERROR_TYPE_ERROR: The message received is an error.
  - ERROR_TYPE_WARNING: The message received is a warning.
  - ERROR_TYPE_SCRIPT: The message received is a script error.
  - ERROR_TYPE_SHADER: The message received is a shader error.

