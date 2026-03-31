## Camera2D <- Node2D

Camera node for 2D scenes. It forces the screen (current layer) to scroll following this node. This makes it easier (and faster) to program scrollable scenes than manually changing the position of CanvasItem-based nodes. Cameras register themselves in the nearest Viewport node (when ascending the tree). Only one camera can be active per viewport. If no viewport is available ascending the tree, the camera will register in the global viewport. This node is intended to be a simple helper to get things going quickly, but more functionality may be desired to change how the camera works. To make your own custom camera node, inherit it from Node2D and change the transform of the canvas by setting `Viewport.canvas_transform` in Viewport (you can obtain the current Viewport by using `Node.get_viewport`). Note that the Camera2D node's `Node2D.global_position` doesn't represent the actual position of the screen, which may differ due to applied smoothing or limits. You can use `get_screen_center_position` to get the real position. Same for the node's `Node2D.global_rotation` which may be different due to applied rotation smoothing. You can use `get_screen_rotation` to get the current rotation of the screen.

**Props:**
- anchor_mode: int (Camera2D.AnchorMode) = 1
- custom_viewport: Node
- drag_bottom_margin: float = 0.2
- drag_horizontal_enabled: bool = false
- drag_horizontal_offset: float = 0.0
- drag_left_margin: float = 0.2
- drag_right_margin: float = 0.2
- drag_top_margin: float = 0.2
- drag_vertical_enabled: bool = false
- drag_vertical_offset: float = 0.0
- editor_draw_drag_margin: bool = false
- editor_draw_limits: bool = false
- editor_draw_screen: bool = true
- enabled: bool = true
- ignore_rotation: bool = true
- limit_bottom: int = 10000000
- limit_enabled: bool = true
- limit_left: int = -10000000
- limit_right: int = 10000000
- limit_smoothed: bool = false
- limit_top: int = -10000000
- offset: Vector2 = Vector2(0, 0)
- position_smoothing_enabled: bool = false
- position_smoothing_speed: float = 5.0
- process_callback: int (Camera2D.Camera2DProcessCallback) = 1
- rotation_smoothing_enabled: bool = false
- rotation_smoothing_speed: float = 5.0
- zoom: Vector2 = Vector2(1, 1)

- **anchor_mode**: The Camera2D's anchor point.
- **custom_viewport**: The custom Viewport node attached to the Camera2D. If `null` or not a Viewport, uses the default viewport instead.
- **drag_bottom_margin**: Bottom margin needed to drag the camera. A value of `1` makes the camera move only when reaching the bottom edge of the screen.
- **drag_horizontal_enabled**: If `true`, the camera only moves when reaching the horizontal (left and right) drag margins. If `false`, the camera moves horizontally regardless of margins.
- **drag_horizontal_offset**: The relative horizontal drag offset of the camera between the right (`-1`) and left (`1`) drag margins. **Note:** Used to set the initial horizontal drag offset; determine the current offset; or force the current offset. It's not automatically updated when `drag_horizontal_enabled` is `true` or the drag margins are changed.
- **drag_left_margin**: Left margin needed to drag the camera. A value of `1` makes the camera move only when reaching the left edge of the screen.
- **drag_right_margin**: Right margin needed to drag the camera. A value of `1` makes the camera move only when reaching the right edge of the screen.
- **drag_top_margin**: Top margin needed to drag the camera. A value of `1` makes the camera move only when reaching the top edge of the screen.
- **drag_vertical_enabled**: If `true`, the camera only moves when reaching the vertical (top and bottom) drag margins. If `false`, the camera moves vertically regardless of the drag margins.
- **drag_vertical_offset**: The relative vertical drag offset of the camera between the bottom (`-1`) and top (`1`) drag margins. **Note:** Used to set the initial vertical drag offset; determine the current offset; or force the current offset. It's not automatically updated when `drag_vertical_enabled` is `true` or the drag margins are changed.
- **editor_draw_drag_margin**: If `true`, draws the camera's drag margin rectangle in the editor.
- **editor_draw_limits**: If `true`, draws the camera's limits rectangle in the editor.
- **editor_draw_screen**: If `true`, draws the camera's screen rectangle in the editor.
- **enabled**: Controls whether the camera can be active or not. If `true`, the Camera2D will become the main camera when it enters the scene tree and there is no active camera currently (see `Viewport.get_camera_2d`). When the camera is currently active and `enabled` is set to `false`, the next enabled Camera2D in the scene tree will become active.
- **ignore_rotation**: If `true`, the camera's rendered view is not affected by its `Node2D.rotation` and `Node2D.global_rotation`.
- **limit_bottom**: Bottom scroll limit in pixels. The camera stops moving when reaching this value, but `offset` can push the view past the limit.
- **limit_enabled**: If `true`, the limits will be enabled. Disabling this will allow the camera to focus anywhere, when the four `limit_*` properties will not work.
- **limit_left**: Left scroll limit in pixels. The camera stops moving when reaching this value, but `offset` can push the view past the limit.
- **limit_right**: Right scroll limit in pixels. The camera stops moving when reaching this value, but `offset` can push the view past the limit.
- **limit_smoothed**: If `true`, the camera smoothly stops when reaches its limits. This property has no effect if `position_smoothing_enabled` is `false`. **Note:** To immediately update the camera's position to be within limits without smoothing, even with this setting enabled, invoke `reset_smoothing`.
- **limit_top**: Top scroll limit in pixels. The camera stops moving when reaching this value, but `offset` can push the view past the limit.
- **offset**: The camera's relative offset. Useful for looking around or camera shake animations. The offsetted camera can go past the limits defined in `limit_top`, `limit_bottom`, `limit_left` and `limit_right`.
- **position_smoothing_enabled**: If `true`, the camera's view smoothly moves towards its target position at `position_smoothing_speed`.
- **position_smoothing_speed**: Speed in pixels per second of the camera's smoothing effect when `position_smoothing_enabled` is `true`.
- **process_callback**: The camera's process callback.
- **rotation_smoothing_enabled**: If `true`, the camera's view smoothly rotates, via asymptotic smoothing, to align with its target rotation at `rotation_smoothing_speed`. **Note:** This property has no effect if `ignore_rotation` is `true`.
- **rotation_smoothing_speed**: The angular, asymptotic speed of the camera's rotation smoothing effect when `rotation_smoothing_enabled` is `true`.
- **zoom**: The camera's zoom. Higher values are more zoomed in. For example, a zoom of `Vector2(2.0, 2.0)` will be twice as zoomed in on each axis (the view covers an area four times smaller). In contrast, a zoom of `Vector2(0.5, 0.5)` will be twice as zoomed out on each axis (the view covers an area four times larger). The X and Y components should generally always be set to the same value, unless you wish to stretch the camera view. **Note:** `FontFile.oversampling` does *not* take Camera2D zoom into account. This means that zooming in/out will cause bitmap fonts and rasterized (non-MSDF) dynamic fonts to appear blurry or pixelated unless the font is part of a CanvasLayer that makes it ignore camera zoom. To ensure text remains crisp regardless of zoom, you can enable MSDF font rendering by enabling `ProjectSettings.gui/theme/default_font_multichannel_signed_distance_field` (applies to the default project font only), or enabling **Multichannel Signed Distance Field** in the import options of a DynamicFont for custom fonts. On system fonts, `SystemFont.multichannel_signed_distance_field` can be enabled in the inspector.

**Methods:**
- align() - Aligns the camera to the tracked node. **Note:** Calling `force_update_scroll` after this method is not required.
- force_update_scroll() - Forces the camera to update scroll immediately.
- get_drag_margin(margin: int) -> float - Returns the specified `Side`'s margin. See also `drag_bottom_margin`, `drag_top_margin`, `drag_left_margin`, and `drag_right_margin`.
- get_limit(margin: int) -> int - Returns the camera limit for the specified `Side`. See also `limit_bottom`, `limit_top`, `limit_left`, and `limit_right`.
- get_screen_center_position() -> Vector2 - Returns the center of the screen from this camera's point of view, in global coordinates. **Note:** The exact targeted position of the camera may be different. See `get_target_position`.
- get_screen_rotation() -> float - Returns the current screen rotation from this camera's point of view. **Note:** The screen rotation can be different from `Node2D.global_rotation` if the camera is rotating smoothly due to `rotation_smoothing_enabled`.
- get_target_position() -> Vector2 - Returns this camera's target position, in global coordinates. **Note:** The returned value is not the same as `Node2D.global_position`, as it is affected by the drag properties. It is also not the same as the current position if `position_smoothing_enabled` is `true` (see `get_screen_center_position`).
- is_current() -> bool - Returns `true` if this Camera2D is the active camera (see `Viewport.get_camera_2d`).
- make_current() - Forces this Camera2D to become the current active one. `enabled` must be `true`.
- reset_smoothing() - Sets the camera's position immediately to its current smoothing destination. This method has no effect if `position_smoothing_enabled` is `false`.
- set_drag_margin(margin: int, drag_margin: float) - Sets the specified `Side`'s margin. See also `drag_bottom_margin`, `drag_top_margin`, `drag_left_margin`, and `drag_right_margin`.
- set_limit(margin: int, limit: int) - Sets the camera limit for the specified `Side`. See also `limit_bottom`, `limit_top`, `limit_left`, and `limit_right`.

**Enums:**
**AnchorMode:** ANCHOR_MODE_FIXED_TOP_LEFT=0, ANCHOR_MODE_DRAG_CENTER=1
  - ANCHOR_MODE_FIXED_TOP_LEFT: The camera's position is fixed so that the top-left corner is always at the origin.
  - ANCHOR_MODE_DRAG_CENTER: The camera's position takes into account vertical/horizontal offsets and the screen size.
**Camera2DProcessCallback:** CAMERA2D_PROCESS_PHYSICS=0, CAMERA2D_PROCESS_IDLE=1
  - CAMERA2D_PROCESS_PHYSICS: The camera updates during physics frames (see `Node.NOTIFICATION_INTERNAL_PHYSICS_PROCESS`).
  - CAMERA2D_PROCESS_IDLE: The camera updates during process frames (see `Node.NOTIFICATION_INTERNAL_PROCESS`).

