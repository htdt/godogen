## Performance <- Object

This class provides access to a number of different monitors related to performance, such as memory usage, draw calls, and FPS. These are the same as the values displayed in the **Monitor** tab in the editor's **Debugger** panel. By using the `get_monitor` method of this class, you can access this data from your code. You can add custom monitors using the `add_custom_monitor` method. Custom monitors are available in **Monitor** tab in the editor's **Debugger** panel together with built-in monitors. **Note:** Some of the built-in monitors are only available in debug mode and will always return `0` when used in a project exported in release mode. **Note:** Some of the built-in monitors are not updated in real-time for performance reasons, so there may be a delay of up to 1 second between changes. **Note:** Custom monitors do not support negative values. Negative values are clamped to 0.

**Methods:**
- add_custom_monitor(id: StringName, callable: Callable, arguments: Array = [], type: int = 0) - Adds a custom monitor with the name `id`. You can specify the category of the monitor using slash delimiters in `id` (for example: `"Game/NumberOfNPCs"`). If there is more than one slash delimiter, then the default category is used. The default category is `"Custom"`. Prints an error if given `id` is already present. The debugger calls the callable to get the value of custom monitor. The callable must return a zero or positive integer or floating-point number. Callables are called with arguments supplied in argument array.
- get_custom_monitor(id: StringName) -> Variant - Returns the value of custom monitor with given `id`. The callable is called to get the value of custom monitor. See also `has_custom_monitor`. Prints an error if the given `id` is absent.
- get_custom_monitor_names() -> StringName[] - Returns the names of active custom monitors in an Array.
- get_custom_monitor_types() -> PackedInt32Array - Returns the `MonitorType` values of active custom monitors in an Array.
- get_monitor(monitor: int) -> float - Returns the value of one of the available built-in monitors. You should provide one of the `Monitor` constants as the argument, like this: See `get_custom_monitor` to query custom performance monitors' values.
- get_monitor_modification_time() -> int - Returns the last tick in which custom monitor was added/removed (in microseconds since the engine started). This is set to `Time.get_ticks_usec` when the monitor is updated.
- has_custom_monitor(id: StringName) -> bool - Returns `true` if custom monitor with the given `id` is present, `false` otherwise.
- remove_custom_monitor(id: StringName) - Removes the custom monitor with given `id`. Prints an error if the given `id` is already absent.

**Enums:**
**Monitor:** TIME_FPS=0, TIME_PROCESS=1, TIME_PHYSICS_PROCESS=2, TIME_NAVIGATION_PROCESS=3, MEMORY_STATIC=4, MEMORY_STATIC_MAX=5, MEMORY_MESSAGE_BUFFER_MAX=6, OBJECT_COUNT=7, OBJECT_RESOURCE_COUNT=8, OBJECT_NODE_COUNT=9, ...
  - TIME_FPS: The number of frames rendered in the last second. This metric is only updated once per second, even if queried more often. *Higher is better.*
  - TIME_PROCESS: Time it took to complete one frame, in seconds. *Lower is better.*
  - TIME_PHYSICS_PROCESS: Time it took to complete one physics frame, in seconds. *Lower is better.*
  - TIME_NAVIGATION_PROCESS: Time it took to complete one navigation step, in seconds. This includes navigation map updates as well as agent avoidance calculations. *Lower is better.*
  - MEMORY_STATIC: Static memory currently used, in bytes. Not available in release builds. *Lower is better.*
  - MEMORY_STATIC_MAX: Available static memory. Not available in release builds. *Lower is better.*
  - MEMORY_MESSAGE_BUFFER_MAX: Largest amount of memory the message queue buffer has used, in bytes. The message queue is used for deferred functions calls and notifications. *Lower is better.*
  - OBJECT_COUNT: Number of objects currently instantiated (including nodes). *Lower is better.*
  - OBJECT_RESOURCE_COUNT: Number of resources currently used. *Lower is better.*
  - OBJECT_NODE_COUNT: Number of nodes currently instantiated in the scene tree. This also includes the root node. *Lower is better.*
  - OBJECT_ORPHAN_NODE_COUNT: Number of orphan nodes, i.e. nodes which are not parented to a node of the scene tree. *Lower is better.* **Note:** This is only available in debug mode and will always return `0` when used in a project exported in release mode.
  - RENDER_TOTAL_OBJECTS_IN_FRAME: The total number of objects in the last rendered frame. This metric doesn't include culled objects (either via hiding nodes, frustum culling or occlusion culling). *Lower is better.*
  - RENDER_TOTAL_PRIMITIVES_IN_FRAME: The total number of vertices or indices rendered in the last rendered frame. This metric doesn't include primitives from culled objects (either via hiding nodes, frustum culling or occlusion culling). Due to the depth prepass and shadow passes, the number of primitives is always higher than the actual number of vertices in the scene (typically double or triple the original vertex count). *Lower is better.*
  - RENDER_TOTAL_DRAW_CALLS_IN_FRAME: The total number of draw calls performed in the last rendered frame. This metric doesn't include culled objects (either via hiding nodes, frustum culling or occlusion culling), since they do not result in draw calls. *Lower is better.*
  - RENDER_VIDEO_MEM_USED: The amount of video memory used (texture and vertex memory combined, in bytes). Since this metric also includes miscellaneous allocations, this value is always greater than the sum of `RENDER_TEXTURE_MEM_USED` and `RENDER_BUFFER_MEM_USED`. *Lower is better.*
  - RENDER_TEXTURE_MEM_USED: The amount of texture memory used (in bytes). *Lower is better.*
  - RENDER_BUFFER_MEM_USED: The amount of render buffer memory used (in bytes). *Lower is better.*
  - PHYSICS_2D_ACTIVE_OBJECTS: Number of active RigidBody2D nodes in the game. *Lower is better.*
  - PHYSICS_2D_COLLISION_PAIRS: Number of collision pairs in the 2D physics engine. *Lower is better.*
  - PHYSICS_2D_ISLAND_COUNT: Number of islands in the 2D physics engine. *Lower is better.*
  - PHYSICS_3D_ACTIVE_OBJECTS: Number of active RigidBody3D and VehicleBody3D nodes in the game. *Lower is better.*
  - PHYSICS_3D_COLLISION_PAIRS: Number of collision pairs in the 3D physics engine. *Lower is better.*
  - PHYSICS_3D_ISLAND_COUNT: Number of islands in the 3D physics engine. *Lower is better.*
  - AUDIO_OUTPUT_LATENCY: Output latency of the AudioServer. Equivalent to calling `AudioServer.get_output_latency`, it is not recommended to call this every frame.
  - NAVIGATION_ACTIVE_MAPS: Number of active navigation maps in NavigationServer2D and NavigationServer3D. This also includes the empty default navigation maps created by World2D and World3D instances.
  - NAVIGATION_REGION_COUNT: Number of active navigation regions in NavigationServer2D and NavigationServer3D.
  - NAVIGATION_AGENT_COUNT: Number of active navigation agents processing avoidance in NavigationServer2D and NavigationServer3D.
  - NAVIGATION_LINK_COUNT: Number of active navigation links in NavigationServer2D and NavigationServer3D.
  - NAVIGATION_POLYGON_COUNT: Number of navigation mesh polygons in NavigationServer2D and NavigationServer3D.
  - NAVIGATION_EDGE_COUNT: Number of navigation mesh polygon edges in NavigationServer2D and NavigationServer3D.
  - NAVIGATION_EDGE_MERGE_COUNT: Number of navigation mesh polygon edges that were merged due to edge key overlap in NavigationServer2D and NavigationServer3D.
  - NAVIGATION_EDGE_CONNECTION_COUNT: Number of polygon edges that are considered connected by edge proximity NavigationServer2D and NavigationServer3D.
  - NAVIGATION_EDGE_FREE_COUNT: Number of navigation mesh polygon edges that could not be merged in NavigationServer2D and NavigationServer3D. The edges still may be connected by edge proximity or with links.
  - NAVIGATION_OBSTACLE_COUNT: Number of active navigation obstacles in the NavigationServer2D and NavigationServer3D.
  - PIPELINE_COMPILATIONS_CANVAS: Number of pipeline compilations that were triggered by the 2D canvas renderer.
  - PIPELINE_COMPILATIONS_MESH: Number of pipeline compilations that were triggered by loading meshes. These compilations will show up as longer loading times the first time a user runs the game and the pipeline is required.
  - PIPELINE_COMPILATIONS_SURFACE: Number of pipeline compilations that were triggered by building the surface cache before rendering the scene. These compilations will show up as a stutter when loading a scene the first time a user runs the game and the pipeline is required.
  - PIPELINE_COMPILATIONS_DRAW: Number of pipeline compilations that were triggered while drawing the scene. These compilations will show up as stutters during gameplay the first time a user runs the game and the pipeline is required.
  - PIPELINE_COMPILATIONS_SPECIALIZATION: Number of pipeline compilations that were triggered to optimize the current scene. These compilations are done in the background and should not cause any stutters whatsoever.
  - NAVIGATION_2D_ACTIVE_MAPS: Number of active navigation maps in the NavigationServer2D. This also includes the empty default navigation maps created by World2D instances.
  - NAVIGATION_2D_REGION_COUNT: Number of active navigation regions in the NavigationServer2D.
  - NAVIGATION_2D_AGENT_COUNT: Number of active navigation agents processing avoidance in the NavigationServer2D.
  - NAVIGATION_2D_LINK_COUNT: Number of active navigation links in the NavigationServer2D.
  - NAVIGATION_2D_POLYGON_COUNT: Number of navigation mesh polygons in the NavigationServer2D.
  - NAVIGATION_2D_EDGE_COUNT: Number of navigation mesh polygon edges in the NavigationServer2D.
  - NAVIGATION_2D_EDGE_MERGE_COUNT: Number of navigation mesh polygon edges that were merged due to edge key overlap in the NavigationServer2D.
  - NAVIGATION_2D_EDGE_CONNECTION_COUNT: Number of polygon edges that are considered connected by edge proximity NavigationServer2D.
  - NAVIGATION_2D_EDGE_FREE_COUNT: Number of navigation mesh polygon edges that could not be merged in the NavigationServer2D. The edges still may be connected by edge proximity or with links.
  - NAVIGATION_2D_OBSTACLE_COUNT: Number of active navigation obstacles in the NavigationServer2D.
  - NAVIGATION_3D_ACTIVE_MAPS: Number of active navigation maps in the NavigationServer3D. This also includes the empty default navigation maps created by World3D instances.
  - NAVIGATION_3D_REGION_COUNT: Number of active navigation regions in the NavigationServer3D.
  - NAVIGATION_3D_AGENT_COUNT: Number of active navigation agents processing avoidance in the NavigationServer3D.
  - NAVIGATION_3D_LINK_COUNT: Number of active navigation links in the NavigationServer3D.
  - NAVIGATION_3D_POLYGON_COUNT: Number of navigation mesh polygons in the NavigationServer3D.
  - NAVIGATION_3D_EDGE_COUNT: Number of navigation mesh polygon edges in the NavigationServer3D.
  - NAVIGATION_3D_EDGE_MERGE_COUNT: Number of navigation mesh polygon edges that were merged due to edge key overlap in the NavigationServer3D.
  - NAVIGATION_3D_EDGE_CONNECTION_COUNT: Number of polygon edges that are considered connected by edge proximity NavigationServer3D.
  - NAVIGATION_3D_EDGE_FREE_COUNT: Number of navigation mesh polygon edges that could not be merged in the NavigationServer3D. The edges still may be connected by edge proximity or with links.
  - NAVIGATION_3D_OBSTACLE_COUNT: Number of active navigation obstacles in the NavigationServer3D.
  - MONITOR_MAX: Represents the size of the `Monitor` enum.
**MonitorType:** MONITOR_TYPE_QUANTITY=0, MONITOR_TYPE_MEMORY=1, MONITOR_TYPE_TIME=2, MONITOR_TYPE_PERCENTAGE=3
  - MONITOR_TYPE_QUANTITY: Monitor output is formatted as an integer value.
  - MONITOR_TYPE_MEMORY: Monitor output is formatted as computer memory. Submitted values should represent a number of bytes.
  - MONITOR_TYPE_TIME: Monitor output is formatted as time in milliseconds. Submitted values should represent a time in seconds (not milliseconds).
  - MONITOR_TYPE_PERCENTAGE: Monitor output is formatted as a percentage. Submitted values should represent a fractional value rather than the percentage directly, e.g. `0.5` for `50.00%`.

