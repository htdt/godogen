## Path3D <- Node3D

Can have PathFollow3D child nodes moving along the Curve3D. See PathFollow3D for more information on the usage. Note that the path is considered as relative to the moved nodes (children of PathFollow3D). As such, the curve should usually start with a zero vector `(0, 0, 0)`.

**Props:**
- curve: Curve3D
- debug_custom_color: Color = Color(0, 0, 0, 1)

- **curve**: A Curve3D describing the path.
- **debug_custom_color**: The custom color used to draw the path in the editor. If set to `Color.BLACK` (as by default), the color set in `ProjectSettings.debug/shapes/paths/geometry_color` is used.

**Signals:**
- curve_changed - Emitted when the `curve` changes.
- debug_color_changed - Emitted when the `debug_custom_color` changes.

