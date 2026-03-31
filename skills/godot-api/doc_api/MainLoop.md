## MainLoop <- Object

MainLoop is the abstract base class for a Godot project's game loop. It is inherited by SceneTree, which is the default game loop implementation used in Godot projects, though it is also possible to write and use one's own MainLoop subclass instead of the scene tree. Upon the application start, a MainLoop implementation must be provided to the OS; otherwise, the application will exit. This happens automatically (and a SceneTree is created) unless a MainLoop Script is provided from the command line (with e.g. `godot -s my_loop.gd`) or the `ProjectSettings.application/run/main_loop_type` project setting is overwritten. Here is an example script implementing a simple MainLoop:

**Methods:**
- _finalize() - Called before the program exits.
- _initialize() - Called once during initialization.
- _physics_process(delta: float) -> bool - Called each physics tick. `delta` is the logical time between physics ticks in seconds and is equal to `Engine.time_scale` / `Engine.physics_ticks_per_second`. Equivalent to `Node._physics_process`. If implemented, the method must return a boolean value. `true` ends the main loop, while `false` lets it proceed to the next step. **Note:** `_physics_process` may be called up to `Engine.max_physics_steps_per_frame` times per (idle) frame. This step limit may be reached when the engine is suffering performance issues. **Note:** Accumulated `delta` may diverge from real world seconds.
- _process(delta: float) -> bool - Called on each idle frame, prior to rendering, and after physics ticks have been processed. `delta` is the time between frames in seconds. Equivalent to `Node._process`. If implemented, the method must return a boolean value. `true` ends the main loop, while `false` lets it proceed to the next frame. **Note:** When the engine is struggling and the frame rate is lowered, `delta` will increase. When `delta` is increased, it's capped at a maximum of `Engine.time_scale` * `Engine.max_physics_steps_per_frame` / `Engine.physics_ticks_per_second`. As a result, accumulated `delta` may not represent real world time. **Note:** When `--fixed-fps` is enabled or the engine is running in Movie Maker mode (see MovieWriter), process `delta` will always be the same for every frame, regardless of how much time the frame took to render. **Note:** Frame delta may be post-processed by `OS.delta_smoothing` if this is enabled for the project.

**Signals:**
- on_request_permissions_result(permission: String, granted: bool) - Emitted when a user responds to a permission request.

**Enums:**
**Constants:** NOTIFICATION_OS_MEMORY_WARNING=2009, NOTIFICATION_TRANSLATION_CHANGED=2010, NOTIFICATION_WM_ABOUT=2011, NOTIFICATION_CRASH=2012, NOTIFICATION_OS_IME_UPDATE=2013, NOTIFICATION_APPLICATION_RESUMED=2014, NOTIFICATION_APPLICATION_PAUSED=2015, NOTIFICATION_APPLICATION_FOCUS_IN=2016, NOTIFICATION_APPLICATION_FOCUS_OUT=2017, NOTIFICATION_TEXT_SERVER_CHANGED=2018, ...
  - NOTIFICATION_OS_MEMORY_WARNING: Notification received from the OS when the application is exceeding its allocated memory. Specific to the iOS platform.
  - NOTIFICATION_TRANSLATION_CHANGED: Notification received when translations may have changed. Can be triggered by the user changing the locale. Can be used to respond to language changes, for example to change the UI strings on the fly. Useful when working with the built-in translation support, like `Object.tr`.
  - NOTIFICATION_WM_ABOUT: Notification received from the OS when a request for "About" information is sent. Specific to the macOS platform.
  - NOTIFICATION_CRASH: Notification received from Godot's crash handler when the engine is about to crash. Implemented on desktop platforms if the crash handler is enabled.
  - NOTIFICATION_OS_IME_UPDATE: Notification received from the OS when an update of the Input Method Engine occurs (e.g. change of IME cursor position or composition string). Implemented on desktop and web platforms.
  - NOTIFICATION_APPLICATION_RESUMED: Notification received from the OS when the application is resumed. Specific to the Android and iOS platforms.
  - NOTIFICATION_APPLICATION_PAUSED: Notification received from the OS when the application is paused. Specific to the Android and iOS platforms. **Note:** On iOS, you only have approximately 5 seconds to finish a task started by this signal. If you go over this allotment, iOS will kill the app instead of pausing it.
  - NOTIFICATION_APPLICATION_FOCUS_IN: Notification received from the OS when the application is focused, i.e. when changing the focus from the OS desktop or a thirdparty application to any open window of the Godot instance. Implemented on desktop and mobile platforms.
  - NOTIFICATION_APPLICATION_FOCUS_OUT: Notification received from the OS when the application is defocused, i.e. when changing the focus from any open window of the Godot instance to the OS desktop or a thirdparty application. Implemented on desktop and mobile platforms.
  - NOTIFICATION_TEXT_SERVER_CHANGED: Notification received when text server is changed.
  - NOTIFICATION_APPLICATION_PIP_MODE_ENTERED: Notification received when the application enters picture-in-picture mode.
  - NOTIFICATION_APPLICATION_PIP_MODE_EXITED: Notification received when the application exits picture-in-picture mode.

