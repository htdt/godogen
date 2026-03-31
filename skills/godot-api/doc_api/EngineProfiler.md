## EngineProfiler <- RefCounted

This class can be used to implement custom profilers that are able to interact with the engine and editor debugger. See EngineDebugger and EditorDebuggerPlugin for more information.

**Methods:**
- _add_frame(data: Array) - Called when data is added to profiler using `EngineDebugger.profiler_add_frame_data`.
- _tick(frame_time: float, process_time: float, physics_time: float, physics_frame_time: float) - Called once every engine iteration when the profiler is active with information about the current frame. All time values are in seconds. Lower values represent faster processing times and are therefore considered better.
- _toggle(enable: bool, options: Array) - Called when the profiler is enabled/disabled, along with a set of `options`.

