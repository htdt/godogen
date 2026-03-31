## StyleBoxLine <- StyleBox

A StyleBox that displays a single line of a given color and thickness. The line can be either horizontal or vertical. Useful for separators.

**Props:**
- color: Color = Color(0, 0, 0, 1)
- grow_begin: float = 1.0
- grow_end: float = 1.0
- thickness: int = 1
- vertical: bool = false

- **color**: The line's color.
- **grow_begin**: The number of pixels the line will extend before the StyleBoxLine's bounds. If set to a negative value, the line will begin inside the StyleBoxLine's bounds.
- **grow_end**: The number of pixels the line will extend past the StyleBoxLine's bounds. If set to a negative value, the line will end inside the StyleBoxLine's bounds.
- **thickness**: The line's thickness in pixels.
- **vertical**: If `true`, the line will be vertical. If `false`, the line will be horizontal.

