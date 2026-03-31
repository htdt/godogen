## Parallax2D <- Node2D

A Parallax2D is used to create a parallax effect. It can move at a different speed relative to the camera movement using `scroll_scale`. This creates an illusion of depth in a 2D game. If manual scrolling is desired, the Camera2D position can be ignored with `ignore_camera_scroll`. **Note:** Any changes to this node's position made after it enters the scene tree will be overridden if `ignore_camera_scroll` is `false` or `screen_offset` is modified.

**Props:**
- autoscroll: Vector2 = Vector2(0, 0)
- follow_viewport: bool = true
- ignore_camera_scroll: bool = false
- limit_begin: Vector2 = Vector2(-10000000, -10000000)
- limit_end: Vector2 = Vector2(10000000, 10000000)
- physics_interpolation_mode: int (Node.PhysicsInterpolationMode) = 2
- repeat_size: Vector2 = Vector2(0, 0)
- repeat_times: int = 1
- screen_offset: Vector2 = Vector2(0, 0)
- scroll_offset: Vector2 = Vector2(0, 0)
- scroll_scale: Vector2 = Vector2(1, 1)

- **autoscroll**: Velocity at which the offset scrolls automatically, in pixels per second.
- **follow_viewport**: If `true`, this Parallax2D is offset by the current camera's position. If the Parallax2D is in a CanvasLayer separate from the current camera, it may be desired to match the value with `CanvasLayer.follow_viewport_enabled`.
- **ignore_camera_scroll**: If `true`, Parallax2D's position is not affected by the position of the camera.
- **limit_begin**: Top-left limits for scrolling to begin. If the camera is outside of this limit, the Parallax2D stops scrolling. Must be lower than `limit_end` minus the viewport size to work.
- **limit_end**: Bottom-right limits for scrolling to end. If the camera is outside of this limit, the Parallax2D will stop scrolling. Must be higher than `limit_begin` and the viewport size combined to work.
- **repeat_size**: Repeats the Texture2D of each of this node's children and offsets them by this value. When scrolling, the node's position loops, giving the illusion of an infinite scrolling background if the values are larger than the screen size. If an axis is set to `0`, the Texture2D will not be repeated.
- **repeat_times**: Overrides the amount of times the texture repeats. Each texture copy spreads evenly from the original by `repeat_size`. Useful for when zooming out with a camera.
- **screen_offset**: Offset used to scroll this Parallax2D. This value is updated automatically unless `ignore_camera_scroll` is `true`.
- **scroll_offset**: The Parallax2D's offset. Similar to `screen_offset` and `Node2D.position`, but will not be overridden. **Note:** Values will loop if `repeat_size` is set higher than `0`.
- **scroll_scale**: Multiplier to the final Parallax2D's offset. Can be used to simulate distance from the camera. For example, a value of `1` scrolls at the same speed as the camera. A value greater than `1` scrolls faster, making objects appear closer. Less than `1` scrolls slower, making objects appear further, and a value of `0` stops the objects completely.

