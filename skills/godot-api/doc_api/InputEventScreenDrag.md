## InputEventScreenDrag <- InputEventFromWindow

Stores information about screen drag events. See `Node._input`.

**Props:**
- index: int = 0
- pen_inverted: bool = false
- position: Vector2 = Vector2(0, 0)
- pressure: float = 0.0
- relative: Vector2 = Vector2(0, 0)
- screen_relative: Vector2 = Vector2(0, 0)
- screen_velocity: Vector2 = Vector2(0, 0)
- tilt: Vector2 = Vector2(0, 0)
- velocity: Vector2 = Vector2(0, 0)

- **index**: The drag event index in the case of a multi-drag event.
- **pen_inverted**: Returns `true` when using the eraser end of a stylus pen.
- **position**: The drag position in the viewport the node is in, using the coordinate system of this viewport.
- **pressure**: Represents the pressure the user puts on the pen. Ranges from `0.0` to `1.0`.
- **relative**: The drag position relative to the previous position (position at the last frame). **Note:** `relative` is automatically scaled according to the content scale factor, which is defined by the project's stretch mode settings. This means touch sensitivity will appear different depending on resolution when using `relative` in a script that handles touch aiming. To avoid this, use `screen_relative` instead.
- **screen_relative**: The unscaled drag position relative to the previous position in screen coordinates (position at the last frame). This position is *not* scaled according to the content scale factor or calls to `InputEvent.xformed_by`. This should be preferred over `relative` for touch aiming regardless of the project's stretch mode.
- **screen_velocity**: The unscaled drag velocity in pixels per second in screen coordinates. This velocity is *not* scaled according to the content scale factor or calls to `InputEvent.xformed_by`. This should be preferred over `velocity` for touch aiming regardless of the project's stretch mode.
- **tilt**: Represents the angles of tilt of the pen. Positive X-coordinate value indicates a tilt to the right. Positive Y-coordinate value indicates a tilt toward the user. Ranges from `-1.0` to `1.0` for both axes.
- **velocity**: The drag velocity. **Note:** `velocity` is automatically scaled according to the content scale factor, which is defined by the project's stretch mode settings. This means touch sensitivity will appear different depending on resolution when using `velocity` in a script that handles touch aiming. To avoid this, use `screen_velocity` instead.

